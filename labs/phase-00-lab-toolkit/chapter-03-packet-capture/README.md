# Lab 00/03 — Packet capture

Chapter: [00/03-packet-capture](../../../book/phase-00-lab-toolkit/03-packet-capture.md) · Importance: Should

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Chạy trong container tạm thời (`--rm`); chỉ bắt lưu lượng loopback bên trong container, không đụng mạng thật.
- Không lưu tệp `.pcap` vào repo (`.gitignore` đã loại `*.pcap`, `*.pcapng`).
- Cần Internet để `apk add tcpdump`. Không tạo tài nguyên AWS, không có chi phí.

## Các bước
**1. Predict:** khi client mở kết nối TCP tới server thử rồi gửi một dòng chữ, bạn thấy cờ nào theo thứ tự nào?

**2. Run:**

```powershell
docker run --rm -it alpine sh
```

Trong container:

```sh
apk add --no-cache tcpdump
(nc -l -p 8080 >/dev/null &)
(tcpdump -nn -i lo -c 10 'tcp port 8080' &)
sleep 1
echo hi | nc -w 2 127.0.0.1 8080
sleep 2
```

**3. Verify:** tìm `[S]`, `[S.]`, `[.]`, gói dữ liệu `[P.]`.

## Break it (bắt sai giao diện)

```sh
(tcpdump -nn -i eth0 -c 5 'tcp port 8080' &)
sleep 1
echo hi | nc -w 2 127.0.0.1 8080
sleep 3
```

Dự đoán: không bắt được gói nào (lưu lượng đi qua `lo`, không phải `eth0`). Chạy lại với `-i lo` hoặc `-i any` để thấy gói. Thoát bằng `exit`.

## Dọn dẹp
Container `--rm` tự xóa.

## Ghi kết quả (làm sạch trước khi commit)
Thay IP thật bằng IP giả; lưu vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
