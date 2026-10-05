# Lab 05/03 — Stateful và stateless (mô phỏng SG vs NACL)

Chapter: [05/03-sg-vs-nacl-concept](../../../book/phase-05-security/03-sg-vs-nacl-concept.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Lab chạy trong container tạm thời (`--rm`, `--cap-add NET_ADMIN`) và **mô phỏng** ý tưởng bằng `iptables`; quy tắc chỉ tồn tại trong container. `iptables` không giống hệt security group/network ACL của AWS.
- Cần Internet để `apk add iptables`; cần kernel của Docker có hỗ trợ `iptables` và `conntrack`.
- Không tạo tài nguyên AWS, không có chi phí.

## Các bước
**1. Predict:** (a) chỉ cho phép gói đến cổng 8080, kết nối có thành công không? (b) thêm quy tắc "gói thuộc kết nối đã được phép thì cho qua"? (c) bỏ quy tắc đó, mở dải cổng `1024:65535`?

**2. Run:**

```powershell
docker run --rm -it --cap-add NET_ADMIN alpine sh
```

```sh
apk add --no-cache iptables
(nc -l -p 8080 >/dev/null &)
iptables -P INPUT DROP
iptables -A INPUT -i lo -p tcp --dport 8080 -j ACCEPT
echo "--- 1. chỉ cho phép đích 8080 (stateless thiếu chiều trả lời)"
echo hi | nc -w 3 127.0.0.1 8080; echo "mã thoát: $?"
iptables -I INPUT 1 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
echo "--- 2. thêm quy tắc stateful"
echo hi | nc -w 3 127.0.0.1 8080; echo "mã thoát: $?"
iptables -D INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -i lo -p tcp --dport 1024:65535 -j ACCEPT
echo "--- 3. bỏ stateful, mở dải cổng tạm thời (stateless đúng)"
echo hi | nc -w 3 127.0.0.1 8080; echo "mã thoát: $?"
```

**3. Verify / Break it:** dự đoán: bước 1 treo rồi thất bại (SYN-ACK có cổng đích tạm thời bị chặn); bước 2 thành công; bước 3 thành công. Thoát bằng `exit`.

## Dọn dẹp
Container `--rm` tự xóa (quy tắc `iptables` biến mất cùng container).

## Ghi kết quả
Lưu output (đã làm sạch) vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
