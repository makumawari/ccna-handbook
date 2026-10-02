# Lab 03/01 — DHCP

Chapter: [03/01-dhcp](../../../book/phase-03-core-services/01-dhcp.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Phần A chỉ **đọc** thông tin DHCP.
- Phần B (`ipconfig /release` và `/renew`) **tạm thời làm máy mất kết nối** trên card mạng được chọn. Không làm khi đang họp, đang dùng VPN, hoặc trên máy công ty có chính sách riêng; nếu không chắc, bỏ qua Phần B.
- Không có chi phí.

## Phần A — Đọc thông tin DHCP
**1. Predict:** máy có dùng DHCP không? DHCP server là địa chỉ nào, có trùng gateway không? Thời hạn thuê dài bao lâu?

**2. Run:**

```cmd
ipconfig /all
```

```powershell
Get-NetIPAddress -AddressFamily IPv4 | Select-Object IPAddress, PrefixOrigin, ValidLifetime
```

**3. Verify:** `PrefixOrigin` là `Dhcp` hay `Manual`? `Lease Obtained`/`Lease Expires` là khi nào?

## Phần B — Break it (tùy chọn, cẩn thận)
Thay `"Wi-Fi"` bằng tên card mạng của bạn (xem `ipconfig /all`).

```cmd
ipconfig /release "Wi-Fi"
ipconfig /all
ipconfig /renew "Wi-Fi"
ipconfig /all
```

Dự đoán: sau `/release` card mất địa chỉ IPv4 hợp lệ; sau `/renew` máy lấy lại địa chỉ và `Lease Obtained` được cập nhật.

## Khôi phục
Nếu `/renew` không có tác dụng: tắt/bật lại card mạng hoặc kết nối lại Wi-Fi.

## Ghi kết quả (làm sạch trước khi commit)
Thay IP thật, tên máy thật, MAC thật bằng dữ liệu giả; lưu vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
