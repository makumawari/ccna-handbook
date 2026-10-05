# Lab 04/03 — UDP: ba kết quả khi gửi datagram (lab rút gọn)

Chapter: [04/03-udp](../../../book/phase-04-transport-app/03-udp.md) · Importance: Should

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## Phạm vi
Chapter Should nên lab rút gọn: một script Python gửi UDP tới ba đích và so sánh kết quả phía người gửi.

## An toàn và chi phí
- Chạy trong WSL2/Linux (cần `python3`). Chỉ gửi tới `127.0.0.1` và `192.0.2.1` (dải tài liệu RFC 5737, không có máy thật).
- Hành vi `ConnectionRefusedError` ở trường hợp (b) là của **Linux**; Windows có thể cho kết quả khác.
- Không tạo tài nguyên AWS, không có chi phí.

## Phần A — Ba kết quả
**1. Predict:** (a) server đang chạy, (b) cổng đóng trên máy này, (c) địa chỉ không ai trả lời: mỗi trường hợp in ra gì?

**2. Run:**

```bash
python3 - <<'PY'
import socket, threading

def server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('127.0.0.1', port))
    data, addr = s.recvfrom(1024)
    s.sendto(b'pong: ' + data, addr)
    s.close()

threading.Thread(target=server, args=(9998,), daemon=True).start()

def ask(host, port, label):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2)
    s.connect((host, port))
    s.send(b'ping')
    try:
        print(label, '->', s.recv(100))
    except Exception as e:
        print(label, '->', type(e).__name__)
    finally:
        s.close()

ask('127.0.0.1', 9998, '(a) server đang chạy')
ask('127.0.0.1', 9, '(b) cổng đóng trên máy này')
ask('192.0.2.1', 9, '(c) địa chỉ không ai trả lời')
PY
```

**3. Verify:** dự đoán (Linux): (a) `b'pong: ping'`; (b) `ConnectionRefusedError`; (c) `timeout`.

> Server có thể chưa kịp bind khi client gửi lần đầu; nếu (a) cho `timeout`, chạy lại.

## Phần B — Quan sát bằng ss và bắt gói (tùy chọn)
Mở hai terminal WSL. Terminal 1: `nc -u -l 9999`. Terminal 2: `ss -ulpn | grep 9999`, rồi `echo hi | nc -u -w1 127.0.0.1 9999`. Quan sát: cổng UDP ở trạng thái `UNCONN` (không có kết nối) và gói tới nơi mà không có bắt tay.

Biến thể nâng cao: chạy `sudo tcpdump -i lo -n 'udp port 9999'` ở terminal 3 để thấy datagram và không có SYN/ACK (`00/03`).

## Dọn dẹp
Dừng `nc` bằng Ctrl+C. Không có thay đổi hệ thống.

## Ghi kết quả (làm sạch trước khi commit)
Lưu output (đã làm sạch) vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
