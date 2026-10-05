# CLAUDE.md — Network Fundamentals Handbook (Infra / DevOps / Cloud)

Handbook tiếng Việt về mạng máy tính cho Infra/DevOps/Cloud (phần CCNA cần thiết + phần DevOps cần, gắn với AWS và troubleshooting). Repo "anh em" của `java-backend-interview-handbook` (chỉ đọc, không sửa).

## 0. Nguồn chuẩn và thứ tự ưu tiên
**`spec/` (v1.0, đã duyệt 2026-10-02) là nguồn chuẩn** cho nội dung sách. File này chỉ giữ quy tắc làm việc và quy tắc an toàn.

| Cần biết | Đọc |
|---|---|
| Tầm nhìn, đối tượng, phạm vi | `spec/part-1-vision.md` |
| Template 18 mục, metadata, Importance, Definition of Done, interview collapse | `spec/part-2-chapter-standard.md` |
| Markdown, callout, Mermaid, lệnh/output, `shopnet`, dải IP, nguồn, MkDocs | `spec/part-3-book-wide-standard.md` |
| 59 chapter, Prerequisites, thứ tự viết | `spec/part-4-roadmap.md` |
| Graph, các bảng mapping, tag, glossary/playbook | `spec/part-5-knowledge-graph.md` |
| Story/Break it seeds (chưa kiểm chứng) · quy trình coverage map · lịch sử | `spec/story-seeds.md` · `spec/ccna-coverage-map-process.md` · `spec/CHANGELOG.md` |

Đọc file spec liên quan **trước khi** viết/review/scaffold chapter; không dựa vào trí nhớ về nội dung spec. Thứ tự ưu tiên khi xung đột: (1) mục 3 và 4 của file này → (2) yêu cầu trực tiếp của người dùng → (3) `spec/` → (4) file này. Repo Java chỉ để tham khảo ý tưởng, không ràng buộc. Mâu thuẫn không giải quyết được: ghi vào mục 9 và hỏi, không tự chọn. Đổi spec → ghi `spec/CHANGELOG.md`.

## 1. Người học
Kỹ sư IT người Việt chuyển sang DevOps, hướng tới Cloud Architect; hands-on hạ tầng còn yếu; **không** giả định hiểu sâu AWS; tiếng Anh trung bình nên **không** giả định hiểu thuật ngữ. Môi trường: Windows (PowerShell/CMD) + có thể WSL2.

## 2. Quy tắc nội dung cốt lõi (chi tiết ở spec)
- **Packet journey first; WHY → HOW; troubleshoot-first; thực hành bắt buộc (Predict → Run → Verify → Break it); 20/80.** Concept (Phase 01–05) tách khỏi AWS (Phase 06); không dạy lại, dùng `> Xem lại:`.
- **Thuật ngữ lần đầu trong chapter:** `Term (bản dịch — giải thích ngắn)`; JA: `日本語 (romaji — nghĩa)`; không giải thích thuật ngữ bằng thuật ngữ chưa giải thích; đã giải thích ở chapter trước thì link glossary; mọi thuật ngữ mới vào `book/glossary.md`.
- **Template 18 mục, không tự đổi tên/thứ tự:** Story · Objectives · Prerequisites · Why it exists · Mental model · How it works · Key settings · AWS mapping · Hands-on lab · Break it · Troubleshooting · Security & cost · Misconceptions · Interview questions · Exercises · Cheat sheet · Glossary terms · Further reading. Mức bắt buộc theo Must/Should/Nice: Part 2 §7.
- **Ngoài phạm vi** (trừ khi người dùng yêu cầu): cú pháp Cisco IOS chi tiết, STP/EtherChannel, wireless, QoS, cáp vật lý.
- File **UTF-8, LF**. Lệnh shell ghi rõ `bash`/`powershell`/`cmd`.

## 3. An toàn khi chạy lệnh (ưu tiên cao nhất)
- **Không** tạo/sửa/xóa tài nguyên AWS và **không** chạy lệnh phá hủy (`rm -rf`, `docker system prune`, `aws ... delete-*`, `cloudformation delete-stack`, `terraform destroy`, `git push --force`, `git reset --hard`) nếu người dùng chưa đồng ý **đúng lệnh đó, đúng lúc đó**. Hiển thị lệnh + giải thích trước; ưu tiên `--dry-run`, `--no-execute-changeset`.
- **Không bao giờ** đọc, in, commit credentials, access key, token, `~/.aws/credentials`, private key.
- AWS lab chỉ trên **tài khoản sandbox riêng**, Region `ap-northeast-1`, tag `Project=net-handbook`, người dùng đã đặt budget alert; mỗi lab có teardown + lệnh kiểm tra đã xóa hết. Cảnh báo chi phí **trước** khi chạy tài nguyên tính phí theo giờ/GB (NAT Gateway, Interface endpoint, TGW attachment, ALB/NLB, VPN, Direct Connect); không ghi số tiền trong sách.
- Lab local ưu tiên Docker Compose (kiểm tra hiện trạng image trước khi dùng); cần namespace/`NET_ADMIN` thì ghi rõ WSL2/Linux.
- `.claude/settings.json` có deny rules (đã thử toàn bộ rule 2026-10-02) nhưng chỉ khớp theo tiền tố lệnh, **không thay thế** các quy tắc trên.

## 4. Bảo mật và bản quyền
**Repo có thể public.** Không đưa vào repo (nội dung, ví dụ, commit, tên file, comment, sơ đồ): tên hệ thống/công ty/khách hàng/dự án thật; IP, CIDR, hostname, domain nội bộ thật; AWS account ID, ARN, tên bucket/stack thật; nội dung tài liệu thiết kế/ticket thật (kể cả diễn đạt lại); ảnh chụp console chưa che.
- Bài học từ dự án thật → viết lại bằng dữ liệu giả (`shopnet`; dải IP ở `spec/part-3` §5: private RFC 1918, public giả RFC 5737; **không** dùng `172.32.x.x` như private). Dữ liệu thật người dùng dán vào chat chỉ dùng để phân tích, không đưa vào file.
- `tools/forbidden-terms.local.txt` do **người dùng** điền (sao chép từ `tools/forbidden-terms.example.txt`), nằm trong `.gitignore` và bị deny rule chặn đọc/ghi; Claude không tạo hay đọc file này.
- Không chép nguyên văn Cisco, khóa học, sách, blog; viết bằng lời người học, ghi nguồn ở mục 18 chapter; trích trực tiếp tối đa vài từ, có ngoặc kép + nguồn; không sao chép sơ đồ nguồn khác. Coverage map chỉ liệt kê tên objective.
- Sự thật AWS có thể đổi phải kiểm chứng với docs hiện tại và ghi `<!-- verified: YYYY-MM-DD <url> -->`; chưa kiểm chứng → `[CHƯA KIỂM CHỨNG]`. **Không bịa** số liệu, giá, tên khóa học, URL. Người học chạy lab và dán output; Claude **không bao giờ tự viết `expected-output.txt`** (chưa có → `[CHƯA CHẠY]`).

## 5. Chế độ làm việc
**Mặc định: REVIEWER.** Người học tự viết bằng lời mình; Claude review, không viết hộ cả chapter. Claude được tự làm: khung chapter, bảng, Mermaid (khi được nhờ), cheat sheet, lint, script, cấu hình MkDocs. Yêu cầu mơ hồ ("viết chapter 05") → trả lời bằng outline + câu hỏi dẫn dắt, không viết thân bài.
- **SCAFFOLD** (chỉ khi người dùng nói "scaffold"): tạo thư mục/file chapter theo template với `TODO` + metadata theo `spec/part-4-roadmap.md`; chạy lint sau đó; không viết nội dung.
- **DRAFT** (chỉ khi được nhờ soạn một mục cụ thể): từng phần nhỏ, giải thích cách tiếp cận trước, đánh dấu `<!-- DRAFT: người học cần viết lại bằng lời mình -->`.
- **EXPLAIN** (người dùng hỏi khái niệm): big picture → WHY → HOW → sai/hỏng thì sao → debug; giữ quy tắc thuật ngữ ở mục 2.

**Review chapter:** báo cáo ngắn theo nhóm, không khen cho có, cuối cùng **tối đa 5 việc cần sửa** theo ưu tiên. Kiểm tra: (1) đúng template/metadata/Importance (Part 2); (2) đúng kỹ thuật — chỉ câu sai/mơ hồ, nêu bản đúng + nguồn; (3) thuật ngữ đúng quy tắc, đã vào glossary; (4) WHY trước HOW, có "sai thì sao"; (5) lab có Predict/Run/Verify/Break it + output thật; (6) troubleshooting đủ triệu chứng → thứ tự kiểm tra → công cụ; (7) AWS facts có `verified` + ngày; (8) không lọt dữ liệu thật; (9) `> Xem lại:` đúng, không dạy lại, cross-reference cập nhật; (10) dễ hiểu với người đọc tiếng Anh trung bình.

Sau mỗi chapter hoàn thành: cập nhật `ccna-coverage-map.md`, `glossary.md`, `cross-reference-index.md`, `troubleshooting-playbook.md` (nếu có). Chapter chỉ `done` khi đạt Definition of Done ở `spec/part-2` §8.

## 6. Git
Nhánh `chapter/phase-NN-<slug>`; commit nhỏ, một ý một commit: `docs(phase-02): draft chapter 05-nat-pat`, `spec: ...`, `tools: ...`. Không commit `forbidden-terms.local.txt`, credential, `site/`. **Không** `git push/merge/rebase/reset` nếu người dùng không yêu cầu rõ.

## 7. Commands (cập nhật khi có `requirements.txt`/`mkdocs.yml`)
```powershell
python -m venv .venv ; .venv\Scripts\pip install -r requirements.txt   # powershell
.venv\Scripts\mkdocs serve -a 127.0.0.1:8005                            # powershell; mở /ccna-handbook/ (site_url có tiền tố); WSL/bash: .venv/bin/mkdocs
.venv\Scripts\mkdocs build --strict                                     # powershell, kiểm tra build
.venv\Scripts\python tools/lint_chapters.py                             # powershell; thêm --sensitive-only khi chỉ cần quét nhạy cảm
```
`tools/lint_chapters.py`: tên mục + thứ tự, metadata, slug Prerequisites/Used Later, chapter Must `done` không còn `TODO`, Mermaid hợp lệ, link nội bộ, thuật ngữ mục 17 có trong glossary, UTF-8/LF, quét thông tin nhạy cảm (account ID 12 số, `AKIA`/`ASIA`, ARN, IP ngoài dải cho phép, từ cấm). Bỏ qua một dòng: `lint:allow-ip`, `lint:allow-id`, `lint:allow-arn`, `lint:allow-todo`; cả file: `lint:allow-ip-file` (chỉ khi file cố ý nêu ví dụ sai). Thoát mã 1 nếu có lỗi (dùng được làm pre-commit/CI).

## 8. Trạng thái
- **Bước 0 và Bước 1 đã xong:** `spec/part-1`…`part-5` v1.0.
- **Giai đoạn 0 đã xong (2026-10-02):** `mkdocs.yml`, `requirements.txt` (ghim `mkdocs<2`), `.gitignore`, `.gitattributes` (LF), `.claude/launch.json`, `tools/lint_chapters.py`, `tools/forbidden-terms.example.txt`, `book/index.md`, `spec/ccna-coverage-map.md` (khung), `spec/sources/README.md`, `spec/raw-interview-questions.md` (khung).
- **Đã scaffold (2026-10-02):** 59 chapter `Status: todo` + `book/phase-08-.../00-resolved-gap-log.md`, sinh từ bảng `spec/part-4-roadmap.md` (metadata, 18 mục, `> Xem lại:` ở mục 3, comment mức bắt buộc theo Importance). H1 hiện là `# TODO — tiêu đề dạng câu hỏi`; người học đặt Title khi viết.
- **Chapter đã soạn (DRAFT theo yêu cầu người dùng; người dùng duyệt 2026-10-02):** `01/01-packet-journey` (`Status: reviewed`, chưa `done` vì lab `[CHƯA CHẠY]`; thuật ngữ đã vào `book/glossary.md`; lab ở `labs/phase-01-foundation/chapter-01-packet-journey/`).
- **Đã soạn nháp (`Status: draft`, chờ review):** `00/01`, `00/02`, `01/02`, `01/03`, `01/04`, `01/05`, `01/06`, `02/01`, `02/02`, `02/03`, `02/05`, `03/01`, `03/02` (mỗi chapter có lab README ở `labs/`, lab `[CHƯA CHẠY]`; sơ đồ Mermaid kiểm tra bằng `mermaid.parse` trên trình duyệt). Chuỗi tiền đề của lát cắt giai đoạn 2 đã đủ.
- **Deploy:** `.github/workflows/deploy.yml` build và đưa lên GitHub Pages khi push vào `main`; cần người dùng đặt Pages source = "GitHub Actions" trong cài đặt repo.
- **Chờ người dùng:** PDF blueprint vào `spec/sources/`; câu hỏi phỏng vấn thô; tạo `tools/forbidden-terms.local.txt`. Chưa scaffold: `book/glossary.md`, `cross-reference-index.md`, `troubleshooting-playbook.md` (tạo khi có nội dung đầu tiên).

## 9. Quyết định đang mở
| Quyết định | Mặc định đề xuất |
|---|---|
| Phiên bản blueprint CCNA | Chưa xác định — kiểm tra Cisco (WebFetch), người dùng đặt PDF vào `spec/sources/` |
| Repo public hay private | Người dùng chọn đưa lên `github.com/makumawari/ccna-handbook` (2026-10-02); mức công khai chưa xác nhận, cứ giả định public (mục 4). GitHub Pages cho repo private có thể cần gói trả phí `[CHƯA KIỂM CHỨNG]` |
| Đường dẫn repo tham chiếu | `../java-backend-interview-handbook` |
