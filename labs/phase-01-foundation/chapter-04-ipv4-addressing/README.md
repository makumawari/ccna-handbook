# Lab 01/04 — IPv4 addressing

Chapter: [01/04-ipv4-addressing](../../../book/phase-01-foundation/04-ipv4-addressing.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Phần A chỉ tính toán. Phần B chạy trong container tạm thời (`--rm`, `--cap-add NET_ADMIN`) nên không đổi mạng của máy thật.
- Không có chi phí.

## Phần A — Tính địa chỉ
**1. Predict (tính tay trước):** network address, broadcast address, mask của `10.20.30.40/8`, `172.16.5.9/16`, `192.168.1.20/24`.

**2. Run:**

```bash
python3 -c "import ipaddress as i; [print(x, i.ip_interface(x).network, i.ip_interface(x).network.broadcast_address, i.ip_interface(x).netmask) for x in ('10.20.30.40/8','172.16.5.9/16','192.168.1.20/24')]"
```

```powershell
[Convert]::ToString(192,2).PadLeft(8,'0')
```

**3. Verify:** so với phép tính tay.

## Phần B — Break it (sai mask)

```powershell
docker run --rm -it --cap-add NET_ADMIN alpine sh
```

Trong container:

```sh
ip addr add 192.168.1.20/24 dev eth0
ip route get 192.168.1.50
ip addr del 192.168.1.20/24 dev eth0
ip addr add 192.168.1.20/32 dev eth0
ip route get 192.168.1.50
```

Dự đoán: với `/24` đích `192.168.1.50` được gửi thẳng ra `eth0`; với `/32` nó đi theo default route. Thoát bằng `exit`.

## Dọn dẹp
Container dùng `--rm` nên tự xóa.

## Ghi kết quả (làm sạch trước khi commit)
Lưu vào `expected-output.txt`; dùng IP giả. Chạy `python tools/lint_chapters.py`.
