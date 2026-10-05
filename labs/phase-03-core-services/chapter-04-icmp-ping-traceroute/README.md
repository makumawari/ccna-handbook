# Lab 03/04 — ICMP, ping and traceroute

Chapter: [03/04-icmp-ping-traceroute](../../../book/phase-03-core-services/04-icmp-ping-traceroute.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Phần A gửi vài gói ping/traceroute nhỏ tới default gateway và `example.com`. Không đổi cấu hình máy. Đừng chạy dồn dập vào hệ thống không phải của bạn.
- Phần B chạy trong container tạm thời (`--rm`, `--cap-add NET_ADMIN`); quy tắc `iptables` chỉ tồn tại trong container. Cần cài `iptables` trong container (`apk add`, cần Internet).
- Không tạo tài nguyên AWS, không có chi phí.

## Phần A — Đo và đọc ping/traceroute
**1. Predict:** RTT tới gateway? Ba kiểu traceroute (UDP, ICMP, TCP) có tới được đích không? MTU đường đi của bạn là bao nhiêu (1472/1473)?

**2. Run (Windows):**

```powershell
ping -n 4 <default gateway của bạn>
ping -n 4 example.com
tracert -d example.com
ping -f -l 1472 -n 2 example.com
ping -f -l 1473 -n 2 example.com
```

**Run (WSL2/Linux):**

```bash
traceroute -n example.com
traceroute -n -I example.com
traceroute -n -T -p 443 example.com
ping -M do -s 1472 -c 2 example.com
ping -M do -s 1473 -c 2 example.com
```

**3. Verify:** so sánh ba kiểu traceroute; 1472 qua được còn 1473 thất bại hay không.

## Phần B — Break it (ping thất bại nhưng dịch vụ vẫn sống)

```powershell
docker run --rm -it --cap-add NET_ADMIN alpine sh
```

Trong container:

```sh
apk add --no-cache iptables
ping -c 1 127.0.0.1
iptables -A INPUT -p icmp --icmp-type echo-request -j DROP
ping -c 1 -W 2 127.0.0.1
(nc -l -p 8080 >/dev/null &)
sleep 1
echo hi | nc -w 2 127.0.0.1 8080; echo "nc thoát với mã $?"
```

Dự đoán: ping đầu thành công; sau khi thêm quy tắc, ping hết thời gian (100% mất gói); kết nối TCP tới cổng 8080 vẫn thành công (mã thoát 0). Nếu `apk add`/`iptables` không chạy được, ghi lại lý do rồi bỏ qua. Thoát bằng `exit`.

## Dọn dẹp
Container `--rm` tự xóa.

## Ghi kết quả (làm sạch trước khi commit)
Thay IP thật (gateway, các router trên đường, IP của `example.com`) bằng IP giả; lưu vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
