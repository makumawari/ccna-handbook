# Network Fundamentals Handbook (Infra / DevOps / Cloud)

## Project Specification

Version: 1.0 (đã duyệt 2026-10-02)

# PART 3 — Quy chuẩn toàn bộ Handbook

> Part 2 định nghĩa **một chapter** viết thế nào. Part 3 định nghĩa **cả cuốn sách** thống nhất ra sao: markdown, callout, sơ đồ, lệnh, domain ví dụ, nguồn, cấu hình MkDocs.
> Mâu thuẫn với `CLAUDE.md` §0 thì ưu tiên theo CLAUDE.md.

---

# 1. Handbook là một hệ thống

Phase sau kế thừa Phase trước; không dạy lại, luôn tham chiếu ngược.

```
Lab toolkit → Foundation → Routing → Core services → Transport/App → Security → AWS networking → Linux/Container → Troubleshooting/Interview
```

- Chapter khái niệm (Phase 01–05) trung lập vendor; chapter AWS (Phase 06) áp dụng, không dạy lại khái niệm.
- Cố ý xuất hiện **hai lần** ở hai góc nhìn: NAT, firewall/ACL, DNS, DHCP, load balancer, routing, VPN. Chapter AWS dùng `> Xem lại: ...` rồi chỉ nói phần riêng của AWS.
- Mỗi sự thật chỉ định nghĩa **một nơi**; nơi khác dẫn link.

---

# 2. Markdown

- Chỉ dùng heading `#` đến `####`; không dùng cấp 5–6.
- Một `#` (H1) mỗi file; H1 là Title dạng câu hỏi (Part 2 §2.1).
- Ưu tiên danh sách gạch đầu dòng; không lạm dụng đánh số (chỉ dùng cho **các bước có thứ tự**).
- **Bảng** chỉ dùng để so sánh hoặc tra cứu, không dùng thay đoạn văn.
- Mỗi file chapter đặt tên theo Part 2 §2.1; chỉ ASCII không dấu, chữ thường, nối bằng `-`.
- Link nội bộ dùng đường dẫn tương đối; link nguồn ngoài ghi ngày kiểm tra ở mục 18.

## 2.1 Callout

Dùng admonition của MkDocs (`!!!`), bốn loại chuẩn:

| Loại | Cú pháp | Dùng cho |
|---|---|---|
| Note | `!!! note` | Thông tin bổ sung |
| Tip | `!!! tip` | Kinh nghiệm thực tế |
| Warning | `!!! warning` | Điều dễ gây lỗi hoặc sự cố |
| Production | `!!! info "Production"` | Điều chỉ gặp khi hệ thống chạy thật |

Block thu gọn (đáp án Interview, gợi ý mở rộng) dùng `???`, mặc định đóng (Part 2 §3.2). Không đặt thông tin an toàn quan trọng **chỉ** trong block thu gọn.

## 2.2 Đánh số

- Heading **không** đánh số thủ công (mục 1–18 của chapter đã cố định theo template; TOC do MkDocs sinh).
- Hình, bảng, listing **không** đánh số (khác repo Java). Tham chiếu bằng tiêu đề đoạn hoặc link neo.
- Số mục chỉ xuất hiện ở tên heading của 18 mục template, ví dụ `## 6. How it works`.

---

# 3. Sơ đồ

- **Mermaid là mặc định** cho luồng gói tin, dependency, deployment, state; luồng rất đơn giản dùng text (`User → ALB → App → DB`).
- Loại Mermaid được dùng: `flowchart` (mặc định `LR`, phân cấp `TD`), `sequenceDiagram` (handshake, request/response), `stateDiagram` (trạng thái TCP), `erDiagram` hiếm khi, `mindmap` cho tổng hợp. Không dùng Mermaid để trang trí.
- Mỗi sơ đồ **một ý**; hệ thống phức tạp tách thành Business / Network / Security / Monitoring flow.
- Nhãn có ký tự đặc biệt đặt trong dấu nháy kép.
- **Sau mỗi sơ đồ phải có đoạn giải thích** quan hệ chính và vì sao mỗi thành phần tồn tại.
- Không chèn ảnh nếu diễn đạt được bằng Mermaid hoặc text; ảnh chụp console/tài liệu thật bị cấm trừ khi đã che mọi định danh (CLAUDE.md §4).
- Sơ đồ text/ASCII phải đọc được khi copy sang nơi khác.

---

# 4. Lệnh, code và output

- Mỗi block lệnh ghi rõ ngôn ngữ: `bash`, `powershell`, `cmd` (không để trống), và nói rõ nếu cần **WSL2**.
- Nối dòng: bash `\`, cmd `^`, PowerShell backtick.
- Một lệnh mỗi block khi lệnh có thể được chạy riêng; **không** có prompt `$` đầu dòng; **không** trộn output vào block lệnh. Output nằm trong block riêng đặt tên `text`.
- Lệnh phá hủy hoặc tạo tài nguyên có phí phải có cảnh báo `!!! warning` ngay trước và lệnh teardown tương ứng (CLAUDE.md §3).
- Output trong sách là output **người học đã chạy thật**; chưa có thì `[CHƯA CHẠY]`. Không tự bịa output.
- File trong repo: **UTF-8, LF** (Windows PowerShell 5.1 có thể ghi UTF-16 với `>`; dùng `Out-File -Encoding utf8` hoặc Python).
- Script của repo ưu tiên Python hoặc bash chạy được trong WSL.
- Phiên bản công cụ/OS (Linux distro, Docker, AWS CLI) ghi ở lab README khi hành vi có thể khác nhau.

---

# 5. Domain và dữ liệu ví dụ

Domain xuyên suốt: hệ thống **E-Commerce giả** tên `shopnet`.

```
User → ALB → App (ECS/EC2) → DB (RDS)       môi trường: prd, stg
```

- **Quy tắc đặt tên resource ví dụ:** `shopnet-<env>-<thành phần>`, ví dụ `shopnet-prd-vpc`, `shopnet-stg-app-sg`. `<env>` là `prd` hoặc `stg`.
- **Region ví dụ:** `ap-northeast-1`. **Tag lab:** `Project=net-handbook`.
- **Dải IP:**
  - Private RFC 1918: `10.0.0.0/8`, `172.16.0.0/12` (`172.16`–`172.31`), `192.168.0.0/16`. Ví dụ ưu tiên `10.0.0.0/16` cho `prd`, `10.1.0.0/16` cho `stg`. Không dùng `172.32.x.x` như private.
  - Public giả RFC 5737: `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`.
- **Cấm** trong ví dụ: tên công ty/dự án/khách hàng thật; IP, CIDR, hostname, domain nội bộ thật; AWS account ID, ARN, tên bucket/stack thật. Dùng placeholder như `<account-id>`, `<region>` khi cần mô tả cấu trúc.
- Với tên miền ví dụ dùng `example.com`, `example.org` (dành riêng cho tài liệu) hoặc `shopnet.example`.

---

# 6. Liên kết giữa các chapter và thuật ngữ

- Chapter A dùng kiến thức chapter B: **không giải thích lại**, viết `> Xem lại: [Tên chapter](đường-dẫn)`.
- Thuật ngữ lần đầu trong chapter: `Term (bản dịch — giải thích)`; thuật ngữ đã giải thích trước đó → link glossary. Chi tiết ở Part 2 §4.
- **`book/glossary.md`** là bảng: `English | Viết tắt | Tiếng Việt | 日本語 | Giải thích đơn giản | Chapter`, sắp theo alphabet; cột Chapter là link.
- **`book/cross-reference-index.md`** là bảng: `Concept → Chapter khái niệm → Chapter AWS → AWS resource → CloudFormation type → CLI kiểm tra`.
- **`book/troubleshooting-playbook.md`** là bảng: `Triệu chứng → Tầng nghi ngờ → Kiểm tra theo thứ tự → Công cụ → Chapter liên quan`.

---

# 7. Nguồn tham khảo và kiểm chứng

Thứ tự ưu tiên khi đưa khẳng định kỹ thuật:

1. RFC và tiêu chuẩn của IETF/IEEE.
2. Tài liệu chính thức của AWS (User Guide, API/CLI reference, Pricing page).
3. Tài liệu chính thức của Linux (man pages, kernel docs) và của công cụ (Docker, Wireshark, …).
4. Blueprint CCNA chính thức — **chỉ để liệt kê tên objective** trong coverage map.
5. Sách và khóa học: chỉ làm tài liệu tham khảo thêm, ghi nguồn, **không** làm cơ sở duy nhất cho khẳng định kỹ thuật, **không** chép nguyên văn.

Quy tắc kiểm chứng:

- Sự thật AWS có thể đổi (giới hạn, giá, hành vi mặc định, tên dịch vụ, yêu cầu tối thiểu) phải kiểm tra tài liệu AWS hiện tại rồi ghi `<!-- verified: YYYY-MM-DD <url> -->` ngay dưới nội dung.
- Chưa kiểm chứng: ghi `[CHƯA KIỂM CHỨNG]` và đưa vào danh sách việc cần làm; không viết như chắc chắn.
- Giá và quota: **không ghi số cố định** trong sách, chỉ trỏ trang chính thức.
- **Không bịa** số liệu, tên khóa học, URL.
- Nội dung có thể lỗi thời (ví dụ tính năng AWS thay đổi): ghi rõ phiên bản/ngày áp dụng.

---

# 8. Độ sâu theo Importance

Không phải chapter nào cũng dài như nhau. Mức bắt buộc theo Must/Should/Nice ở Part 2 §7 quyết định độ sâu: Must có lab, Break it và troubleshooting đầy đủ; Should rút gọn; Nice chỉ giới thiệu khái niệm. Phân loại Importance cho từng chapter nằm ở `spec/part-4-roadmap.md`.

---

# 9. Cấu hình MkDocs bắt buộc

Cấu hình tối thiểu để các quy tắc ở trên render đúng (chi tiết file `mkdocs.yml` sẽ tạo sau):

```yaml
docs_dir: book
theme:
  name: material
  language: vi
plugins:
  - search
  - tags
  - awesome-pages
markdown_extensions:
  - admonition               # !!! note / warning
  - pymdownx.details         # ??? block thu gọn
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - tables
  - attr_list
  - md_in_html
  - toc:
      permalink: true
```

- `requirements.txt` ghim tối thiểu: `mkdocs`, `mkdocs-material`, `mkdocs-awesome-pages-plugin`.
- `site_url`, `repo_url`, `repo_name` đặt theo repo thật khi người dùng đã quyết định đưa lên GitHub (v1.0 ban đầu để trống vì repo có thể public; xem `spec/CHANGELOG.md`). `navigation.instant` của Material cần `site_url`.
- Deploy bằng GitHub Actions (`.github/workflows/deploy.yml`): chạy lint và `mkdocs build --strict` trước khi lên GitHub Pages.
- `.claude/launch.json` dùng `.venv/Scripts/mkdocs.exe` trên Windows (khác `.venv/bin/mkdocs` của repo Java).
- Dự án cần Mermaid render: kiểm tra bằng `mkdocs serve` trước khi dựa vào sơ đồ.

---

# 10. Cập nhật handbook

- Ghi thay đổi spec vào `spec/CHANGELOG.md` (phiên bản + ngày + lý do).
- Khi hành vi AWS đổi, cập nhật chapter và đổi dấu `verified` kèm ngày mới.
- Khi chapter `done` bị phát hiện sai sự thật: hạ `Status` về `draft`, ghi vào `CHANGELOG.md`, sửa, review lại.

---

Đây là **Part 3** của Specification (v1.0).
