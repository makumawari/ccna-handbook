# Lab 00/02 — Linux network tools

Chapter: [00/02-linux-network-tools](../../../book/phase-00-lab-toolkit/02-linux-network-tools.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Chạy trong WSL2 hoặc container. Chỉ thử trên máy của bạn (`127.0.0.1`) hoặc địa chỉ tài liệu `192.0.2.1`; không quét máy người khác.
- `python3 -m http.server` mở thư mục hiện tại ra mạng: chạy ở một thư mục trống và tắt (Ctrl+C) ngay sau lab.
- Không có chi phí.

## Chuẩn bị
Công cụ cần có: `ip`, `ss`, `curl`, `dig`, `python3` (tên gói tùy distro; xem mục 7 của chapter).

## Các bước
**1. Predict:** `ip -br addr` liệt kê giao diện nào? `ss -ltn` sẽ thêm dòng nào khi bật server cổng 8000? `curl -I` trả mã gì?

**2. Run** (hai cửa sổ shell):

```bash
ip -br addr
ip route
mkdir -p /tmp/lab-http && cd /tmp/lab-http
python3 -m http.server 8000
```

Cửa sổ thứ hai:

```bash
ss -ltn
curl -I http://127.0.0.1:8000
dig +short example.com
```

**3. Verify:** cổng 8000 có ở trạng thái lắng nghe? `curl` có mã 200? 

**4. Break it:** dừng server (Ctrl+C) rồi:

```bash
curl -I --max-time 5 http://127.0.0.1:8000
curl -I --max-time 5 http://192.0.2.1:8000
```

Dự đoán: lệnh 1 báo ngay "Connection refused"; lệnh 2 chờ đến hết 5 giây.

## Dọn dẹp
Server đã dừng; xóa thư mục thử: `rmdir /tmp/lab-http`.

## Ghi kết quả (làm sạch trước khi commit)
Thay IP thật (kể cả kết quả `dig`) bằng IP giả, đổi tên máy thật; lưu vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
