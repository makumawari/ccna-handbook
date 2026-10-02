# Network Fundamentals Handbook (Infra / DevOps / Cloud)

Handbook tiếng Việt về mạng máy tính cho Infra/DevOps/Cloud: phần CCNA cần thiết, phần DevOps cần (TCP/TLS/HTTP, load balancing, công cụ Linux, container) và AWS networking, theo hướng *hiểu bản chất + troubleshoot-first*.

> **Trạng thái:** đang viết. Mỗi chapter có `Status` trong phần Metadata (`todo` / `draft` / `reviewed` / `done`). Nội dung lab chưa được chạy thật; mọi chỗ ghi `[CHƯA CHẠY]` hoặc `[CHƯA KIỂM CHỨNG]` là chưa xác nhận.

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `spec/` | Specification (Part 1–5, v1.0): tầm nhìn, chuẩn chapter, chuẩn toàn sách, roadmap, knowledge graph |
| `book/` | Nội dung handbook theo Phase → Chapter (nguồn của site MkDocs) |
| `labs/` | Lab của từng chapter (Predict → Run → Verify → Break it) |
| `tools/` | `lint_chapters.py` (kiểm tra template, link, Mermaid, thông tin nhạy cảm) |

## Chạy site cục bộ (Windows PowerShell)

```powershell
python -m venv .venv ; .venv\Scripts\pip install -r requirements.txt
.venv\Scripts\mkdocs serve -a 127.0.0.1:8005
.venv\Scripts\python tools\lint_chapters.py
```

## Lưu ý

- Ví dụ dùng hệ thống giả `shopnet` và các dải IP dành cho tài liệu (RFC 5737) hoặc private (RFC 1918); không có dữ liệu thật.
- Nội dung viết lại bằng lời riêng, ghi nguồn ở mục "Further reading" của từng chapter.
