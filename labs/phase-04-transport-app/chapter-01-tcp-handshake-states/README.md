# Lab 04/01 — TCP handshake and states

Chapter: [04/01-tcp-handshake-states](../../../book/phase-04-transport-app/01-tcp-handshake-states.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Chạy trong container tạm thời (`--rm`). Phần iptables (`--cap-add NET_ADMIN`) chỉ tồn tại trong container.
- Cần Internet để `apk add`. Không tạo tài nguyên AWS, không có chi phí.

## Phần A — Quan sát bắt tay và đóng kết nối
**1. Predict:** cờ nào theo thứ tự nào, từ `[S]` đến `[F.]`? Sau khi đóng, trạng thái nào còn lại?

**2. Run:**

```powershell
docker run --rm -it alpine sh
```

```sh
apk add --no-cache tcpdump
(nc -l -p 8080 >/dev/null &)
(tcpdump -nn -i lo -c 12 'tcp port 8080' &)
sleep 1
echo hi | nc -w 2 127.0.0.1 8080
sleep 2
netstat -tan | grep 8080
```

**3. Verify:** `[S]`, `[S.]`, `[.]`, `[P.]`, `[F.]`; trạng thái còn lại trong `netstat` (ví dụ `TIME_WAIT`).

## Phần B — Break it (refused so với im lặng)

```powershell
docker run --rm -it --cap-add NET_ADMIN alpine sh
```

```sh
apk add --no-cache tcpdump iptables
(tcpdump -nn -i lo -c 10 'tcp port 9' &)
sleep 1
nc -w 2 127.0.0.1 9; echo "mã thoát (cổng đóng): $?"
sleep 1
(nc -l -p 8080 >/dev/null &)
iptables -A INPUT -p tcp --dport 8080 -j DROP
(tcpdump -nn -i lo -c 6 'tcp port 8080' &)
sleep 1
nc -w 3 127.0.0.1 8080; echo "mã thoát (SYN bị loại bỏ): $?"
sleep 2
```

Dự đoán: cổng 9 → `[S]` rồi `[R.]` ngay (refused); cổng 8080 sau khi DROP → chỉ có `[S]` lặp lại, không có `[S.]`, `nc` hết thời gian. Nếu `iptables` không chạy được, chỉ làm phần cổng 9. Thoát bằng `exit`.

## Dọn dẹp
Container `--rm` tự xóa (quy tắc iptables biến mất cùng container).

## Ghi kết quả (làm sạch trước khi commit)
Thay IP/cổng thật bằng giả; lưu vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
