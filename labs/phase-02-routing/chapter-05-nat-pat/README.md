# Lab 02/05 — NAT and PAT

Chapter: [02/05-nat-pat](../../../book/phase-02-routing/05-nat-pat.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Phần A chỉ đọc thông tin và gửi vài gói ping nhỏ.
- Phần B tạo một mạng Docker tạm thời rồi **xóa đi** ở bước dọn dẹp. Lệnh `docker network rm` chỉ xóa mạng `net-lab-internal` do lab tạo.
- Không tạo tài nguyên AWS, không có chi phí.

## Phần A — Quan sát NAT trong môi trường của bạn
**1. Predict:** IP của WSL2 có giống Windows không? Container mặc định ở dải nào, có ra Internet được không? Default gateway của WSL2 là gì?

**2. Run:**

```powershell
ipconfig
wsl hostname -I
wsl ip route show default
docker run --rm alpine ip addr
docker run --rm alpine ping -c 2 example.com
```

**3. Verify:** các nơi dùng địa chỉ private nhưng vẫn ra Internet được. Nơi nào đổi địa chỉ nguồn?

## Phần B — Break it (mất đường ra)

```powershell
docker network create --internal net-lab-internal
docker run --rm --network net-lab-internal alpine ping -c 1 -W 2 example.com
```

Dự đoán: ping thất bại (container trong mạng nội bộ không ra được mạng ngoài).

## Dọn dẹp (teardown)

```powershell
docker network rm net-lab-internal
docker network ls
```

Kiểm tra `net-lab-internal` đã biến mất khỏi danh sách.

## Ghi kết quả (làm sạch trước khi commit)
Thay IP thật bằng IP giả, tên miền thật bằng `example.com`; lưu vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
