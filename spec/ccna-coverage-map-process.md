# Quy trình coverage map CCNA (chuyển từ CLAUDE.md; sẽ thành phần đầu của `ccna-coverage-map.md`)

1. Người dùng đặt PDF blueprint CCNA 200-301 vào `spec/sources/` và ghi **phiên bản + ngày tải**. Chưa có → hỏi người dùng; **không** dựng blueprint từ trí nhớ.
2. Phiên bản: **chưa chốt**. Kiểm tra trang Cisco hiện hành (WebFetch) xem v1.1 hay v2.0 đang hiệu lực và ngày hiệu lực; ghi ngày kiểm tra. Đối chiếu thêm phiên bản còn lại.
3. Mỗi objective rơi vào **đúng một** trạng thái:

| Trạng thái | Ý nghĩa |
|---|---|
| **Mapped** | Có chapter dạy đầy đủ → ghi đường dẫn chapter |
| **Concept-only** | Chỉ giới thiệu khái niệm trong một mục của chapter → ghi chapter + mục |
| **Skipped** | Bỏ qua có chủ đích → **bắt buộc ghi lý do** (vd: "không dùng trên AWS") |

4. Kiểm tra cuối: không còn objective chưa phân loại; ghi tóm tắt số lượng ở đầu file.
5. Phần ngoài CCNA (Phase 00, 04, 07, 08) ghi ở mục riêng "Ngoài CCNA, bổ sung cho DevOps".
6. Chỉ liệt kê **tên objective**; không chép phần giải thích của Cisco.
