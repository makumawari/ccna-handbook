# Lab 03/03 — DNS records, TTL and private DNS

Chapter: [03/03-dns-records-ttl-private-dns](../../../book/phase-03-core-services/03-dns-records-ttl-private-dns.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Phần A chỉ **hỏi** DNS (đọc) với `example.com`; không đổi cấu hình máy.
- Phần B chạy trong container tạm thời (`--rm`); `hosts` chỉ bị sửa **trong container**.
- Không tạo tài nguyên AWS, không có chi phí. (Private hosted zone trên AWS sẽ được thực hành ở Phase 06 với cảnh báo chi phí và teardown riêng.)

## Phần A — Đọc bản ghi và TTL
**1. Predict:** loại bản ghi nào có ở `example.com`? TTL của bản ghi A là bao nhiêu và có giảm khi chạy lại không? Tên không tồn tại có kèm SOA không?

**2. Run (WSL2/Linux):**

```bash
dig example.com A +noall +answer
dig example.com NS +noall +answer
dig example.com MX +noall +answer
dig example.com TXT +noall +answer
dig example.com SOA +noall +answer
dig chapter-test.example.com +noall +authority +comments
```

**Run (Windows PowerShell):**

```powershell
Resolve-DnsName example.com -Type A -DnsOnly
Resolve-DnsName example.com -Type NS -DnsOnly
Resolve-DnsName example.com -Type SOA -DnsOnly
```

**3. Verify:** ghi TTL từng loại; chạy lại lệnh `A` sau vài giây để xem TTL còn lại giảm dần; quan sát SOA trong phần authority khi hỏi tên không tồn tại.

## Phần B — Break it (bản ghi cũ còn nằm lại cục bộ)

```powershell
docker run --rm -it alpine sh
```

Trong container:

```sh
echo "192.0.2.10 www.shopnet.example" >> /etc/hosts
ping -c 1 -W 1 www.shopnet.example
nslookup www.shopnet.example
```

Dự đoán: `ping` phân giải tên thành `192.0.2.10` từ `hosts` rồi hết thời gian; `nslookup` hỏi DNS trực tiếp và báo tên không tồn tại. Thoát bằng `exit`.

## Dọn dẹp
Container `--rm` tự xóa; không có thay đổi nào trên máy thật.

## Ghi kết quả (làm sạch trước khi commit)
Thay IP thật (kể cả IP của `example.com` và tên máy chủ DNS thật) bằng IP/tên giả; lưu vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
