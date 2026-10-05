# Lab 04/05 — HTTP

Chapter: [04/05-http](../../../book/phase-04-transport-app/05-http.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Chạy trong WSL2/Linux. Server thử chỉ phục vụ một thư mục tạm; chạy ở thư mục trống và tắt (Ctrl+C) ngay sau lab (nó mở thư mục ra mạng).
- Không tạo tài nguyên AWS, không có chi phí.

## Phần A — Quan sát yêu cầu/phản hồi
**1. Predict:** `GET /` trả mã gì? Đường dẫn không tồn tại trả mã gì? `POST` tới server này trả mã gì? `curl -I` gửi phương thức nào?

**2. Run:**

```bash
mkdir -p /tmp/lab-http && cd /tmp/lab-http && echo "xin chao" > index.html
python3 -m http.server 8000
```

Cửa sổ thứ hai:

```bash
curl -v http://127.0.0.1:8000/
curl -i http://127.0.0.1:8000/khong-co
curl -I http://127.0.0.1:8000/
curl -i -X POST http://127.0.0.1:8000/
curl -s -o /dev/null -w "%{http_code} %{time_total}\n" http://127.0.0.1:8000/
```

**3. Verify:** ghi mã trạng thái, các header, kết nối có tái sử dụng không (`-v`).

## Phần B — Break it (ba kiểu "không được")
Server thử ở Phần A cần đang chạy cho lệnh thứ ba.

```bash
curl -s -o /dev/null -w "http=%{http_code}\n" http://127.0.0.1:9; echo "mã thoát curl: $?"
curl -s -o /dev/null --max-time 3 -w "http=%{http_code}\n" http://192.0.2.1/; echo "mã thoát curl: $?"
curl -s -o /dev/null -w "http=%{http_code}\n" http://127.0.0.1:8000/khong-co; echo "mã thoát curl: $?"
```

Dự đoán: cổng đóng → không có mã HTTP, thoát 7; địa chỉ không phản hồi → thoát 28; đường dẫn không có → `404`, thoát 0.

## Dọn dẹp
Tắt server bằng Ctrl+C; `rmdir /tmp/lab-http` sau khi xóa `index.html`.

## Ghi kết quả (làm sạch trước khi commit)
Thay IP/tên máy thật bằng giả; lưu vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
