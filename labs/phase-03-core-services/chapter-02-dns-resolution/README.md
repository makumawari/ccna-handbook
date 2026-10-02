# Lab 03/02 — DNS resolution

Chapter: [03/02-dns-resolution](../../../book/phase-03-core-services/02-dns-resolution.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
Chỉ **hỏi** DNS (đọc). Không thay đổi cấu hình máy. Không có chi phí.

## Các bước
**1. Predict:** DNS server máy bạn dùng là địa chỉ nào, có trùng gateway không? `example.com` có mấy địa chỉ IPv4 và TTL khoảng bao nhiêu? `dig +trace` đi qua những tầng nào?

**2. Run (Windows PowerShell):**

```powershell
Get-DnsClientServerAddress -AddressFamily IPv4
Resolve-DnsName example.com -Type A -DnsOnly
```

**Run (WSL2/Linux):**

```bash
dig example.com
dig +trace example.com
```

**3. Verify:** server nào trả lời? TTL là bao nhiêu? Chạy lại ngay: TTL còn lại có giảm không (cache)?

**4. Break it (hai kiểu thất bại):**

```powershell
Resolve-DnsName chapter-test.shopnet.example -DnsOnly
Resolve-DnsName example.com -Server 192.0.2.53 -DnsOnly
```

Dự đoán: lệnh 1 báo nhanh "tên không tồn tại" (server có trả lời); lệnh 2 chờ rồi hết thời gian (không có trả lời từ `192.0.2.53`, địa chỉ thuộc dải tài liệu).

## Dọn dẹp
Không có thay đổi cần dọn. Nếu muốn, xóa cache: `Clear-DnsClientCache`.

## Ghi kết quả (làm sạch trước khi commit)
Thay IP thật (kể cả IP DNS server) bằng IP giả; lưu vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
