# Lab 02/01 — Routing table basics

Chapter: [02/01-routing-table-basics](../../../book/phase-02-routing/01-routing-table-basics.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Phần A chỉ **đọc** bảng định tuyến của máy bạn.
- Phần B thay đổi route **bên trong container** tạm thời (`--rm`, `--cap-add NET_ADMIN`); không đổi route của máy thật.
- Không có chi phí.

## Phần A — Đọc bảng định tuyến
**1. Predict:** default route trỏ tới next hop nào? Một địa chỉ cùng mạng đi qua dòng nào? `203.0.113.10` đi qua dòng nào?

**2. Run (Windows PowerShell):**

```powershell
Get-NetRoute -AddressFamily IPv4
Find-NetRoute -RemoteIPAddress 203.0.113.10
```

**Run (WSL2/Linux hoặc container):**

```bash
ip route
ip route get 203.0.113.10
```

**3. Verify:** dòng được chọn có đúng dự đoán? Next hop có khớp default gateway?

## Phần B — Break it

```powershell
docker run --rm -it --cap-add NET_ADMIN alpine sh
```

Trong container:

```sh
ip route get 203.0.113.10
ip route add blackhole 203.0.113.10/32
ip route get 203.0.113.10
ping -c 1 -W 2 203.0.113.10
ip route del blackhole 203.0.113.10/32
ip route del default
ip route get 203.0.113.10
```

Dự đoán: ban đầu qua default route; sau `blackhole` gói bị loại bỏ và ping báo lỗi ngay; sau khi xóa cả blackhole và default thì "Network is unreachable". Thoát bằng `exit`.

## Dọn dẹp
Container `--rm` tự xóa.

## Ghi kết quả (làm sạch trước khi commit)
Thay IP thật bằng IP giả; lưu vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
