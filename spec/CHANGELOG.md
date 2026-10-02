# CHANGELOG — Specification

## v1.0 — 2026-10-02

Bước 1 hoàn tất: `part-1` … `part-5` được người dùng duyệt (chuyển thể từ repo tham chiếu `java-backend-interview-handbook`, viết lại cho mạng).

Quyết định đã chốt ở Bước 0:

- H1 chapter dạng câu hỏi + slug ngắn ASCII (Part 2 §2.1).
- Metadata YAML trong mỗi chapter (Part 2 §2.2); bỏ `Difficulty` và `Interview Frequency %`.
- Mermaid là sơ đồ mặc định (Part 3 §3).
- Glossary dạng bảng (Part 3 §6).
- Template 18 mục là chuẩn của repo này; Importance dùng Must/Should/Nice (Part 2 §3, §7).
- Interview questions: "gợi ý ý chính" hiển thị sẵn, đáp án mẫu trong block collapse (Part 2 §3.2).
- Không đánh số hình/bảng/listing (Part 3 §2.2).
- Roadmap 59 chapter + dependency (Part 4); Part 5: DAG phụ thuộc, các bảng mapping, tiêu chí hoàn thành toàn sách.

Chưa chốt: phiên bản blueprint CCNA (v1.1 hay v2.0) — chờ PDF trong `spec/sources/` (xem `spec/ccna-coverage-map-process.md`).

`.claude/settings.json` (deny rules) đã tạo và thử toàn bộ rule ngày 2026-10-02.

Deploy (2026-10-02): người dùng quyết định đưa repo lên `github.com/makumawari/ccna-handbook`; đặt `site_url`/`repo_url` trong `mkdocs.yml`, thêm `.github/workflows/deploy.yml` (lint + `mkdocs build --strict` + GitHub Pages) và `README.md`; cập nhật Part 3 §9. Lint thêm `100.64.0.0/10` vào dải IP được phép và dấu `lint:allow-ip-file`.

Scaffold (2026-10-02): tạo 59 chapter `todo` + `00-resolved-gap-log.md` từ bảng Part 4. Sửa Part 4 §3: `08/04` Prerequisites từ "06/* (chọn lọc)" thành `06/02, 06/03, 06/04, 06/08, 06/11` để metadata khớp roadmap.

Giai đoạn 0 (2026-10-02): `mkdocs.yml`, `requirements.txt`, `.gitignore`, `.gitattributes`, `.claude/launch.json`, `tools/lint_chapters.py`, `tools/forbidden-terms.example.txt`, khung `ccna-coverage-map.md` / `raw-interview-questions.md` / `sources/README.md`. Phát hiện khi kiểm chứng: file ghi trên Windows mặc định CRLF → chuẩn hóa về LF và thêm `.gitattributes`; Material cảnh báo MkDocs 2.0 phá plugin → ghim `mkdocs<2`.
