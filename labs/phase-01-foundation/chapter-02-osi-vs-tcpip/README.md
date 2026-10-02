# Lab 01/02 — OSI vs TCP/IP

Chapter: [01/02-osi-vs-tcpip](../../../book/phase-01-foundation/02-osi-vs-tcpip.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Phần A chỉ gửi vài gói ping/kết nối/HTTP HEAD tới `example.com`.
- Phần B chạy trong container tạm thời (`--rm`, `--cap-add NET_ADMIN`), không đổi mạng máy thật.
- Không có chi phí.

## Phần A — Một đích, nhiều tầng
**1. Predict:** xếp `ping`, `Test-NetConnection -Port 443`, `curl -I` vào tầng 3, 4 hay 7; dự đoán kết quả.

**2. Run:**

```powershell
ping -n 2 example.com
Test-NetConnection example.com -Port 443
```

```bash
curl -sI https://example.com
```

**3. Verify:** nếu cả ba thành công thì tầng 3–7 đều ổn với đích đó.

## Phần B — Break it (ba tầng, ba kiểu lỗi)

```powershell
docker run --rm -it --cap-add NET_ADMIN alpine sh
```

Trong container, theo thứ tự:

```sh
nslookup chapter-test.shopnet.example
wget -q -T 2 -O - http://127.0.0.1:9
ip route del default
ping -c 1 -W 2 192.0.2.1
```

Dự đoán: lệnh 1 (tầng 7) không phân giải được tên; lệnh 2 (tầng 4) "Connection refused"; lệnh 4 (tầng 3) "Network is unreachable". Thoát bằng `exit`.

## Dọn dẹp
Container `--rm` tự xóa.

## Ghi kết quả (làm sạch trước khi commit)
Thay IP thật (kể cả IP của `example.com`) bằng IP giả; lưu vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
