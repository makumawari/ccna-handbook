# Lab 02/03 — Default route and gateway

Chapter: [02/03-default-route-gateway](../../../book/phase-02-routing/03-default-route-gateway.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Phần A chỉ **đọc** default route và ping gateway.
- Phần B chạy trong container tạm thời (`--rm`, `--cap-add NET_ADMIN`); chỉ sửa route trong container.
- Không có chi phí.

## Phần A — Đọc default route
**1. Predict:** gateway của máy bạn là địa chỉ nào? Có cùng mạng với địa chỉ của bạn không? Ping gateway có thành công không?

**2. Run (Windows PowerShell):**

```powershell
Get-NetRoute -DestinationPrefix 0.0.0.0/0
ping -n 2 <gateway>
```

**Run (Linux/WSL2/container):**

```bash
ip route show default
```

**3. Verify:** gateway và địa chỉ của bạn có cùng network address không? Có mấy default route?

## Phần B — Break it

```powershell
docker run --rm -it --cap-add NET_ADMIN alpine sh
```

Trong container:

```sh
GW=$(ip route show default | awk '{print $3}')
ip route del default
ping -c 1 -W 2 $GW
ping -c 1 -W 2 192.0.2.1
ip route add default via 192.0.2.254
ip route add default via $GW
ping -c 1 -W 2 192.0.2.1
```

Dự đoán: sau khi xóa default route, ping gateway vẫn thành công, ping `192.0.2.1` báo ngay "Network is unreachable"; thêm default qua `192.0.2.254` bị từ chối (off-link); thêm lại đúng gateway thì ping `192.0.2.1` hết thời gian (có route nhưng không ai trả lời).

## Dọn dẹp
Thoát bằng `exit`; container `--rm` tự xóa.

## Ghi kết quả (làm sạch trước khi commit)
Thay IP thật bằng IP giả; lưu vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
