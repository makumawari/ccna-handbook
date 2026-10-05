# Lab 04/02 — Timeout, gửi lại và keepalive

Chapter: [04/02-tcp-timeouts-retransmission-keepalive](../../../book/phase-04-transport-app/02-tcp-timeouts-retransmission-keepalive.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Phần A, B chạy trong WSL2/Linux (chỉ đọc cấu hình, `curl`). Phần C chạy trong container tạm thời (`--rm`, `--cap-add NET_ADMIN`); quy tắc `iptables` chỉ tồn tại trong container.
- Cần Internet để `apk add`. Chỉ gửi tới `127.0.0.1` và `192.0.2.1` (RFC 5737).
- Không tạo tài nguyên AWS, không có chi phí.

## Phần A — Xem mặc định hệ điều hành
**1. Predict:** giá trị `tcp_keepalive_*`, `tcp_syn_retries`, `tcp_retries2` trên máy bạn là bao nhiêu (so với bảng chapter)?

**2. Run:**

```bash
sysctl net.ipv4.tcp_keepalive_time net.ipv4.tcp_keepalive_intvl net.ipv4.tcp_keepalive_probes
sysctl net.ipv4.tcp_syn_retries net.ipv4.tcp_retries2
```

**3. Verify:** mặc định thường là `7200 / 75 / 9`, `6`, `15` (WSL có thể khác).

## Phần B — Timeout kết nối ở ứng dụng
```bash
time curl -sS --connect-timeout 5 -o /dev/null http://192.0.2.1/ ; echo "mã thoát: $?"
```
Dự đoán: thất bại sau khoảng 5 giây (mã thoát 28) vì bạn đặt timeout. Thử bỏ `--connect-timeout` và dùng `--max-time 20` để giới hạn: không đặt kết nối riêng thì phụ thuộc mặc định hệ điều hành (hàng chục giây). Ghi lại thời gian thực tế.

## Phần C — Break it: DROP và gửi lại
```powershell
docker run --rm -it --cap-add NET_ADMIN alpine sh
```

```sh
apk add --no-cache iptables iproute2 busybox-extras
(nc -l -p 9000 >/dev/null &)
sleep 1
(nc 127.0.0.1 9000 &)
sleep 1
ss -tno state established '( dport = :9000 or sport = :9000 )'
iptables -I INPUT -p tcp --dport 9000 -j DROP
iptables -I OUTPUT -p tcp --dport 9000 -j DROP
echo "gui du lieu" | nc -w 1 127.0.0.1 9000
ss -tno
```
Dự đoán: sau khi chặn, kết nối mới tới cổng 9000 treo; kết nối đang tồn tại nếu bị gửi dữ liệu sẽ hiện `timer:(on,...)` và số lần gửi lại tăng dần. Dùng quy tắc `REJECT --reject-with tcp-reset` thay cho `DROP` để thấy khác biệt: kết nối thất bại ngay.

> Cú pháp `ss`/`nc` trong Alpine có thể khác bản đầy đủ; nếu một lệnh không chạy, điều chỉnh và ghi lại ghi chú. `[CHƯA KIỂM CHỨNG]` về tên gói cần cài.

Thoát bằng `exit`.

## Dọn dẹp
Container `--rm` tự xóa (quy tắc `iptables` biến mất cùng container).

## Ghi kết quả (làm sạch trước khi commit)
Lưu output (đã làm sạch) vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
