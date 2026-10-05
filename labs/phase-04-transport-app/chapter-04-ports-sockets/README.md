# Lab 04/04 — Cổng và socket: ai đang nghe ở đâu

Chapter: [04/04-ports-sockets](../../../book/phase-04-transport-app/04-ports-sockets.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Chạy trong WSL2/Linux (cần `python3`, `ss`, `curl`, `nc`). Chỉ dùng loopback và `192.0.2.1` (RFC 5737).
- Server thử chạy nền; dọn dẹp ở cuối. Không tạo tài nguyên AWS, không có chi phí.

## Phần A — Nghe loopback và nghe mọi địa chỉ
**1. Predict:** `ss -tlnp` cho hai server hiển thị Local Address thế nào?

**2. Run:**

```bash
mkdir -p /tmp/lab-ports && cd /tmp/lab-ports
python3 -m http.server 9000 --bind 127.0.0.1 >/dev/null 2>&1 &
S1=$!
python3 -m http.server 9001 --bind 0.0.0.0 >/dev/null 2>&1 &
S2=$!
sleep 1
ss -tlnp | grep -E ':(9000|9001)\b'
curl -s -o /dev/null -w "9000 loopback: %{http_code}\n" http://127.0.0.1:9000/
curl -s -o /dev/null -w "9001 loopback: %{http_code}\n" http://127.0.0.1:9001/
```

**3. Verify:** dự đoán: `127.0.0.1:9000` và `0.0.0.0:9001` (hoặc `*:9001`); cả hai trả `200` khi gọi từ loopback.

Tùy chọn: lấy IP khác của WSL (`ip -4 addr show eth0`) rồi `curl` tới IP đó ở cổng 9000 (dự đoán: refused) và 9001 (dự đoán: thành công). Không dán IP thật vào repo.

## Phần B — Break it: trùng cổng
```bash
python3 -m http.server 9000 --bind 127.0.0.1; echo "mã thoát: $?"
```
Dự đoán: báo `OSError: [Errno 98] Address already in use` (Linux) và thoát với mã khác 0.

## Phần C — Break it: refused và timeout
```bash
time nc -zv 127.0.0.1 9      ; echo "mã thoát: $?"
time nc -zv -w 3 192.0.2.1 9 ; echo "mã thoát: $?"
```
Dự đoán: lệnh đầu thất bại **ngay** (refused: cổng 9 không ai nghe); lệnh sau **treo ~3 giây** rồi hết thời gian (không ai trả lời). Dùng `time` để thấy sự khác biệt.

## Phần D — Cổng tạm
```bash
cat /proc/sys/net/ipv4/ip_local_port_range
curl -s -o /dev/null http://127.0.0.1:9001/ &
sleep 0.2; ss -tan | grep ':9001' | head
```
Dự đoán: dải cổng tạm mặc định `32768 60999` (có thể khác trên bản phân phối); cổng nguồn của kết nối nằm trong dải đó.

## Dọn dẹp
```bash
kill "$S1" "$S2"
rm -rf /tmp/lab-ports
```

## Ghi kết quả (làm sạch trước khi commit)
Lưu output (đã làm sạch) vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
