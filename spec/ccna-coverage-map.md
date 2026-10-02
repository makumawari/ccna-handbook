# CCNA Coverage Map

> Quy trình: `spec/ccna-coverage-map-process.md`. Mỗi objective rơi vào đúng một trạng thái: **Mapped** / **Concept-only** / **Skipped** (Skipped bắt buộc ghi lý do).

## Trạng thái

- **Blueprint:** chưa có PDF trong `spec/sources/` → **chưa liệt kê objective nào**. Không dựng từ trí nhớ.
- **Phiên bản:** trang CCNA của Cisco, kiểm tra 2026-10-02 bằng WebFetch (tóm tắt tự động, `[CẦN ĐỐI CHIẾU VỚI PDF]`), ghi bài thi hiện hành là **v1.1**. Không thấy ngày hiệu lực của v2.0 trong kết quả; v2.0 chưa xác nhận.
- **Việc cần làm:** người dùng tải PDF exam topics vào `spec/sources/` và ghi phiên bản + ngày tải vào `spec/sources/README.md`; sau đó Claude liệt kê tên objective và phân loại.

| Trạng thái | Số lượng |
|---|---|
| Mapped | 0 |
| Concept-only | 0 |
| Skipped | 0 |
| **Chưa phân loại** | **chưa biết (chưa có blueprint)** |

## Objective CCNA

| Domain | Objective (tên) | Trạng thái | Chapter / mục | Lý do (nếu Skipped) |
|---|---|---|---|---|
| _(chờ blueprint)_ | | | | |

## Ngoài CCNA, bổ sung cho DevOps

| Phase | Nội dung | Chapter |
|---|---|---|
| 00 lab-toolkit | Môi trường lab, công cụ mạng Linux, bắt gói tin | `00/01`–`00/03` |
| 04 transport-app | TCP/UDP, HTTP, TLS, load balancing, reverse proxy | `04/01`–`04/08` |
| 06 aws-networking | VPC và dịch vụ mạng AWS | `06/01`–`06/13` |
| 07 linux-container | Namespace, Docker, ECS awsvpc, Kubernetes | `07/01`–`07/05` |
| 08 troubleshooting-interview | Methodology, case study, phỏng vấn | `08/01`–`08/05` |
