# Lab 05/01 — Firewall có trạng thái và bảng theo dõi kết nối

Chapter: [05/01-firewall-stateful-vs-stateless](../../../book/phase-05-security/01-firewall-stateful-vs-stateless.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Chạy trong container tạm thời (`--rm`, `--cap-add NET_ADMIN`); quy tắc `iptables` và bảng theo dõi chỉ tồn tại trong container. Mô phỏng này **không giống hệt** security group của AWS.
- Cần Internet để `apk add iptables conntrack-tools` (tên gói `conntrack-tools` có thể khác theo bản phân phối) và kernel của Docker có `iptables` + `conntrack`.
- Không tạo tài nguyên AWS, không có chi phí.

## Phần A — Xóa quy tắc không cắt kết nối cũ
**1. Predict:** quy tắc mặc định chặn mọi thứ vào; chỉ cho phép gói thuộc kết nối đang có và kết nối MỚI tới cổng 8080. Sau khi xóa quy tắc cho kết nối mới: kết nối cũ còn gửi được không? kết nối mới thì sao?

**2. Run:**

```powershell
docker run --rm -it --cap-add NET_ADMIN alpine sh
```

```sh
apk add --no-cache iptables conntrack-tools
(nc -l -p 8080 >/tmp/recv.txt &)
iptables -P INPUT DROP
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -i lo -p tcp --dport 8080 -m conntrack --ctstate NEW -j ACCEPT
( sleep 8; echo "tin nhan tu ket noi cu" ) | nc 127.0.0.1 8080 &
sleep 2
echo "--- bảng theo dõi kết nối:"
conntrack -L 2>/dev/null | grep 8080
iptables -D INPUT -i lo -p tcp --dport 8080 -m conntrack --ctstate NEW -j ACCEPT
echo "--- kết nối MỚI sau khi xóa quy tắc:"
echo hi | nc -w 2 127.0.0.1 8080; echo "mã thoát: $?"
sleep 8
echo "--- nội dung server nhận được từ kết nối cũ:"
cat /tmp/recv.txt
```

**3. Verify:** có mục `ESTABLISHED` trong bảng; kết nối mới bị chặn (mã thoát khác 0); tin nhắn từ kết nối cũ **vẫn** tới server.

## Phần B — Break it (mất mục theo dõi)
Trong cùng container (hoặc container mới sau khi thiết lập lại):

```sh
(nc -l -p 8081 >/tmp/recv2.txt &)
iptables -A INPUT -i lo -p tcp --dport 8081 -m conntrack --ctstate NEW -j ACCEPT
( sleep 8; echo "tin nhan sau khi xoa bang" ) | nc 127.0.0.1 8081 &
sleep 2
iptables -D INPUT -i lo -p tcp --dport 8081 -m conntrack --ctstate NEW -j ACCEPT
conntrack -F 2>/dev/null
sleep 8
echo "--- server nhận được gì:"
cat /tmp/recv2.txt
```

Dự đoán: sau khi vừa xóa quy tắc vừa xóa bảng theo dõi, gói của kết nối cũ không còn khớp mục nào nên bị chặn; tin nhắn không tới server (tệp rỗng). Lưu ý: cách nhân Linux xử lý gói TCP giữa chừng có thể khác tùy cấu hình; nếu khác dự đoán, ghi lại quan sát. Thoát bằng `exit`.

## Dọn dẹp
Container `--rm` tự xóa (quy tắc và bảng theo dõi biến mất cùng container).

## Ghi kết quả (làm sạch trước khi commit)
Lưu output (đã làm sạch) vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
