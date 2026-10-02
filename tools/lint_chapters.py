#!/usr/bin/env python3
"""Lint cho Network Fundamentals Handbook.

Kiểm tra (xem spec/part-2, spec/part-3, CLAUDE.md mục 4 và 7):
  - Chapter: front matter, H1, khối Metadata, 18 mục đúng tên + thứ tự,
    Importance/Status hợp lệ, chapter Must `done` không còn TODO,
    Prerequisites/Used Later là slug có thật, thuật ngữ mục 17 có trong glossary.
  - Mermaid: fence đóng đủ, loại sơ đồ hợp lệ.
  - Link nội bộ không gãy.
  - Encoding: UTF-8 (không BOM), xuống dòng LF.
  - Thông tin nhạy cảm: AWS account ID, access key, ARN, IP ngoài dải cho phép,
    từ trong tools/forbidden-terms.local.txt.

Chạy:  python tools/lint_chapters.py [--root DIR] [--sensitive-only] [--no-sensitive]
Thoát mã 1 nếu có lỗi. Một dòng có thể bỏ qua quét IP bằng comment `lint:allow-ip`;
cả file bằng comment `lint:allow-ip-file` (dùng khi file cố ý nêu ví dụ sai).
"""
from __future__ import annotations

import argparse
import ipaddress
import re
import sys
from dataclasses import dataclass
from pathlib import Path

SECTIONS = [
    "Story", "Objectives", "Prerequisites", "Why it exists", "Mental model",
    "How it works", "Key settings", "AWS mapping", "Hands-on lab", "Break it",
    "Troubleshooting", "Security & cost", "Misconceptions", "Interview questions",
    "Exercises", "Cheat sheet", "Glossary terms", "Further reading",
]
IMPORTANCE = {"Must", "Should", "Nice"}
STATUS = {"todo", "draft", "reviewed", "done"}
REQUIRED_META = ["Chapter", "Phase", "Importance", "Status", "Prerequisites", "Used Later"]
MERMAID_TYPES = (
    "flowchart", "graph", "sequenceDiagram", "stateDiagram", "stateDiagram-v2",
    "classDiagram", "erDiagram", "journey", "gitGraph", "mindmap", "timeline",
)
# Chapter nằm ở book/phase-NN-<slug>/NN-<slug>.md; các file này không phải chapter.
NON_CHAPTER_NAMES = {"index.md", "glossary.md", "cross-reference-index.md",
                     "troubleshooting-playbook.md", "tags.md", "00-resolved-gap-log.md"}
SCAN_DIRS = ["book", "labs", "spec"]
SCAN_FILES = ["README.md", "CLAUDE.md"]
TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".txt", ".json", ".py", ".sh", ".ps1", ".toml", ".cfg"}
SKIP_DIR_NAMES = {".venv", "site", ".git", "__pycache__", "node_modules", "sources"}
FORBIDDEN_FILE = Path("tools") / "forbidden-terms.local.txt"

ALLOWED_NETS = [ipaddress.ip_network(n) for n in (
    "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16",           # RFC 1918
    "192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24",       # RFC 5737
    "100.64.0.0/10",                                           # RFC 6598 shared address space (CGNAT)
    "0.0.0.0/8", "127.0.0.0/8", "169.254.0.0/16",              # đặc biệt: unspecified, loopback, link-local
    "224.0.0.0/4", "240.0.0.0/4",                              # multicast, mặt nạ/broadcast (255.x)
)]
IP_RE = re.compile(r"(?<![\d.])(\d{1,3}(?:\.\d{1,3}){3})(?![\d.])")
ACCOUNT_RE = re.compile(r"(?<![\d.\-])\d{12}(?![\d.\-])")
ACCESS_KEY_RE = re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")
ARN_RE = re.compile(r"\barn:aws[a-z\-]*:")


@dataclass
class Problem:
    path: Path
    line: int
    msg: str

    def render(self, root: Path) -> str:
        try:
            rel = self.path.relative_to(root)
        except ValueError:
            rel = self.path
        where = f"{rel}:{self.line}" if self.line else str(rel)
        return f"{where}: {self.msg}"


def read_text(path: Path, problems: list[Problem]) -> str | None:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        problems.append(Problem(path, 1, "có BOM UTF-8 (cần UTF-8 không BOM)"))
        raw = raw[3:]
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        problems.append(Problem(path, 1, "file là UTF-16 (cần UTF-8)"))
        return None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        problems.append(Problem(path, 1, f"không giải mã được UTF-8: {exc}"))
        return None
    if "\r" in text:
        line = text[: text.index("\r")].count("\n") + 1
        problems.append(Problem(path, line, "có CRLF (cần xuống dòng LF)"))
    return text


def iter_text_files(root: Path):
    for d in SCAN_DIRS:
        base = root / d
        if base.is_dir():
            for p in sorted(base.rglob("*")):
                if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES and not (SKIP_DIR_NAMES & set(p.relative_to(root).parts)):
                    yield p
    for f in SCAN_FILES:
        p = root / f
        if p.is_file():
            yield p


def chapter_files(root: Path):
    book = root / "book"
    if not book.is_dir():
        return
    for p in sorted(book.glob("phase-*/*.md")):
        if p.name not in NON_CHAPTER_NAMES:
            yield p


def chapter_slug(path: Path) -> str:
    return f"{path.parent.name.split('-')[1]}/{path.stem}"  # phase-02-routing -> 02/01-x


def parse_front_matter(text: str):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5:]


def parse_meta_block(body: str):
    """Trả về (dict key -> list|str, line_of_block) từ khối ```yaml sau '## Metadata'."""
    m = re.search(r"^## Metadata\s*\n+```yaml\n(.*?)\n```", body, re.S | re.M)
    if not m:
        return None
    data: dict[str, object] = {}
    key = None
    for raw in m.group(1).splitlines():
        line = raw.split("#", 1)[0].rstrip() if not raw.lstrip().startswith("-") else raw.rstrip()
        if not line.strip():
            continue
        if line.lstrip().startswith("- "):
            if key is not None and isinstance(data.get(key), list):
                data[key].append(line.lstrip()[2:].strip())
            continue
        k, _, v = line.partition(":")
        key = k.strip()
        v = v.strip()
        data[key] = v if v else []
    return data


def strip_code(text: str) -> str:
    no_fence = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", no_fence)  # bỏ cả inline code (link mẫu, ví dụ)


def check_mermaid(path: Path, text: str, problems: list[Problem]):
    lines = text.split("\n")
    in_fence = False
    fence_lang = ""
    start = 0
    buf: list[str] = []
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("```"):
            if not in_fence:
                in_fence, fence_lang, start, buf = True, s[3:].strip().lower(), i, []
            else:
                if fence_lang == "mermaid":
                    first = next((b.strip() for b in buf if b.strip() and not b.strip().startswith("%%")), "")
                    if not first.startswith(MERMAID_TYPES):
                        problems.append(Problem(path, start, f"Mermaid không bắt đầu bằng loại sơ đồ hợp lệ: '{first[:30]}'"))
                    if first.startswith("sequenceDiagram"):  # ';' là dấu tách câu lệnh, làm hỏng nhãn thông điệp
                        for off, b in enumerate(buf):
                            if ";" in b:
                                problems.append(Problem(path, start + 1 + off, "sequenceDiagram: dấu ';' trong dòng (dùng ',' thay thế)"))
                in_fence = False
        elif in_fence:
            buf.append(line)
    if in_fence:
        problems.append(Problem(path, start, "khối ``` không được đóng"))


def check_links(path: Path, text: str, root: Path, problems: list[Problem]):
    plain = strip_code(text)
    for m in re.finditer(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", plain):
        target = m.group(1)
        if re.match(r"^(https?:|mailto:|#|tel:)", target):
            continue
        file_part = target.split("#", 1)[0]
        if not file_part:
            continue
        resolved = (path.parent / file_part).resolve()
        if not resolved.exists():
            line = plain[: m.start()].count("\n") + 1
            problems.append(Problem(path, line, f"link nội bộ gãy: {target}"))


def glossary_terms(root: Path) -> str:
    g = root / "book" / "glossary.md"
    return g.read_text(encoding="utf-8", errors="ignore").lower() if g.is_file() else ""


def check_chapter(path: Path, text: str, root: Path, slugs: set[str], problems: list[Problem]):
    fm, body = parse_front_matter(text)
    if fm is None:
        problems.append(Problem(path, 1, "thiếu YAML front matter (tags)"))
        body = text
    elif "tags:" not in fm:
        problems.append(Problem(path, 1, "front matter thiếu `tags:`"))
    h1 = [m for m in re.finditer(r"^# (.+)$", strip_code(body), re.M)]
    if len(h1) != 1:
        problems.append(Problem(path, 1, f"cần đúng 1 H1, tìm thấy {len(h1)}"))

    meta = parse_meta_block(body)
    importance = status = None
    if meta is None:
        problems.append(Problem(path, 1, "thiếu khối `## Metadata` với ```yaml"))
    else:
        for k in REQUIRED_META:
            if k not in meta:
                problems.append(Problem(path, 1, f"Metadata thiếu trường `{k}`"))
        importance, status = meta.get("Importance"), meta.get("Status")
        if importance not in IMPORTANCE:
            problems.append(Problem(path, 1, f"Importance phải thuộc {sorted(IMPORTANCE)}, đang là {importance!r}"))
        if status not in STATUS:
            problems.append(Problem(path, 1, f"Status phải thuộc {sorted(STATUS)}, đang là {status!r}"))
        for key in ("Prerequisites", "Used Later"):
            for item in meta.get(key, []) or []:
                m = re.search(r"\b(\d{2})\s*/\s*(\d{2}-[a-z0-9\-]+)", item)  # "01/06-x" hoặc "Phase 01 / 06-x"
                if m and f"{m.group(1)}/{m.group(2)}" not in slugs:
                    problems.append(Problem(path, 1, f"{key}: slug không tồn tại: {m.group(1)}/{m.group(2)}"))

    # 18 mục đúng tên + thứ tự
    heads = [(m.group(1), m.group(2).strip(), strip_code(body)[: m.start()].count("\n") + 1)
             for m in re.finditer(r"^## (\d+)\. (.+)$", strip_code(body), re.M)]
    expected = [f"{i}. {n}" for i, n in enumerate(SECTIONS, 1)]
    actual = [f"{n}. {t}" for n, t, _ in heads]
    if actual != expected:
        missing = [e for e in expected if e not in actual]
        extra = [a for a in actual if a not in expected]
        detail = []
        if missing:
            detail.append("thiếu: " + "; ".join(missing))
        if extra:
            detail.append("thừa/sai tên: " + "; ".join(extra))
        if not missing and not extra:
            detail.append("sai thứ tự")
        problems.append(Problem(path, heads[0][2] if heads else 1, "18 mục không đúng template — " + " | ".join(detail)))

    if importance == "Must" and status == "done":
        for i, line in enumerate(text.split("\n"), 1):
            if re.search(r"\bTODO\b", line) and "lint:allow-todo" not in line:
                problems.append(Problem(path, i, "chapter Must `done` còn TODO"))

    # thuật ngữ mục 17 phải có trong glossary
    sec17 = re.search(r"^## 17\. Glossary terms\s*\n(.*?)(?=^## \d+\. |\Z)", body, re.M | re.S)
    if sec17 and status not in (None, "todo"):
        gloss = glossary_terms(root)
        for line in sec17.group(1).splitlines():
            m = re.match(r"^\s*[-*]\s+(.+)$", line) or re.match(r"^\|\s*([^|]+?)\s*\|", line)
            if not m:
                continue
            term = re.split(r"\s+[/—–|]\s+|\s*/\s*", m.group(1).strip().strip("*`"))[0].strip().strip("*`").lower()
            if not term or term in ("english", "term", "---", "-") or set(term) <= {"-", ":"} or "todo" in term:
                continue
            if term not in gloss:
                problems.append(Problem(path, 1, f"thuật ngữ mục 17 chưa có trong glossary.md: {term}"))


def load_forbidden(root: Path) -> list[str]:
    f = root / FORBIDDEN_FILE
    if not f.is_file():
        return []
    terms = []
    for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = line.strip()
        if s and not s.startswith("#"):
            terms.append(s.lower())
    return terms


def ip_allowed(ip: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return True  # không phải IP hợp lệ (vd 999.1.1.1) -> bỏ qua
    return any(addr in net for net in ALLOWED_NETS)


def check_sensitive(path: Path, text: str, forbidden: list[str], problems: list[Problem]):
    is_py = path.suffix == ".py"
    allow_ip_file = "lint:allow-ip-file" in text  # file cố ý nêu ví dụ sai (vd 172.32.x.x ở 01/06)
    for i, line in enumerate(text.split("\n"), 1):
        if is_py and path.name == "lint_chapters.py":
            continue
        if ACCESS_KEY_RE.search(line):
            problems.append(Problem(path, i, "nghi ngờ AWS access key (AKIA/ASIA...)"))
        if ARN_RE.search(line) and "lint:allow-arn" not in line:
            problems.append(Problem(path, i, "chuỗi ARN (dùng placeholder, không dùng ARN thật)"))
        if ACCOUNT_RE.search(line) and "lint:allow-id" not in line:
            problems.append(Problem(path, i, "chuỗi 12 chữ số (nghi AWS account ID)"))
        if "lint:allow-ip" not in line and not allow_ip_file:
            for m in IP_RE.finditer(line):
                if not ip_allowed(m.group(1)):
                    problems.append(Problem(path, i, f"IP ngoài dải cho phép: {m.group(1)}"))
        low = line.lower()
        for term in forbidden:
            if term in low:
                problems.append(Problem(path, i, "chứa từ trong forbidden-terms.local.txt"))
                break


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", help="thư mục gốc repo (mặc định: thư mục hiện tại)")
    ap.add_argument("--sensitive-only", action="store_true", help="chỉ quét thông tin nhạy cảm + encoding")
    ap.add_argument("--no-sensitive", action="store_true", help="bỏ quét thông tin nhạy cảm")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    problems: list[Problem] = []
    forbidden = load_forbidden(root)
    chapters = list(chapter_files(root))
    slugs = {chapter_slug(p) for p in chapters}

    texts: dict[Path, str] = {}
    for p in iter_text_files(root):
        t = read_text(p, problems)
        if t is not None:
            texts[p] = t

    if not args.sensitive_only:
        for p in chapters:
            t = texts.get(p) or read_text(p, problems)
            if t is None:
                continue
            check_chapter(p, t, root, slugs, problems)
        for p, t in texts.items():
            if p.suffix == ".md":
                check_mermaid(p, t, problems)
                check_links(p, t, root, problems)

    if not args.no_sensitive:
        for p, t in texts.items():
            check_sensitive(p, t, forbidden, problems)

    seen = set()
    unique = []
    for pr in problems:
        key = (str(pr.path), pr.line, pr.msg)
        if key not in seen:
            seen.add(key)
            unique.append(pr)
    for pr in sorted(unique, key=lambda x: (str(x.path), x.line)):
        print(pr.render(root))
    print(f"\n{len(chapters)} chapter, {len(texts)} file đã quét, {len(unique)} vấn đề.")
    return 1 if unique else 0


if __name__ == "__main__":
    sys.exit(main())
