# Lab 01/01 — Packet journey

Chapter: [01/01-packet-journey](../../../book/phase-01-foundation/01-packet-journey.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`. Claude không tự viết output.

## An toàn và chi phí
- Phần A chỉ **đọc** thông tin mạng và gửi vài gói ICMP/UDP nhỏ. Không thay đổi cấu hình.
- Phần B chạy trong container tạm thời (`--rm`), không đụng cấu hình mạng thật.
- Không tạo tài nguyên AWS, **không có chi phí**. Teardown: thoát container (`exit`).
- Yêu cầu Phần B: Docker (WSL2 hoặc Docker Desktop). Phần A chạy được ngay trên Windows.

## Phần A — Trace hành trình

**1. Predict** — ghi ra giấy trước khi chạy:
- Default gateway của máy bạn là địa chỉ nào?
- Hop 1 của `tracert` đến `example.com` là địa chỉ nào?
- Số hop đến `example.com` thuộc khoảng nào (5–10, 10–20, > 20)?

**2. Run**

```powershell
Get-NetIPConfiguration
```

```cmd
tracert -d example.com
```

Trên Linux/WSL2 (cần có `traceroute`):

```bash
traceroute -n example.com
```

**3. Verify** — hop 1 có trùng default gateway? Có hop `*` không? Tổng số hop so với dự đoán?

## Phần B — Break it (hai kiểu thất bại)

```bash
docker run --rm -it --cap-add NET_ADMIN alpine sh
```

Trong container:

```sh
ip route
ping -c 1 -W 2 192.0.2.1
ip route del default
ping -c 1 -W 2 192.0.2.1
```

**Dự đoán:** lần 1 chờ rồi báo mất gói (có đường đi nhưng không ai trả lời); lần 2 báo ngay "Network is unreachable" (không có đường đi). Thoát bằng `exit`.

## Ghi kết quả (làm sạch trước khi commit)

Lưu output vào `expected-output.txt` trong thư mục này **sau khi** thay:
- IP thật → IP giả (`10.0.x.x`, `192.168.x.x`, `192.0.2.x`, `198.51.100.x`, `203.0.113.x`);
- tên máy/tên miền thật → `example.com` hoặc `shopnet.example`.

Chạy `python tools/lint_chapters.py` để bắt IP ngoài dải cho phép.
