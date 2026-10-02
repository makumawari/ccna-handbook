# Lab 01/06 — Private and public addresses

Chapter: [01/06-private-public-ip-rfc1918](../../../book/phase-01-foundation/06-private-public-ip-rfc1918.md) · Importance: Must

<!-- lint:allow-ip-file — lab cố ý dùng 172.32.x.x làm ví dụ sai -->

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Phần A chỉ tính toán bằng Python.
- Phần B chạy trong container tạm thời (`--rm`, `--cap-add NET_ADMIN`); route thêm vào chỉ tồn tại trong container.
- Không có chi phí.

## Phần A — Phân loại địa chỉ
**1. Predict:** địa chỉ nào là private (RFC 1918)? `10.255.255.254`, `172.15.255.255`, `172.16.0.1`, `172.31.255.255`, `172.32.0.1`, `192.167.1.1`, `192.168.200.5`. <!-- lint:allow-ip -->

**2. Run:**

```bash
python3 - <<'PY'
import ipaddress as i
PRIVATE = [i.ip_network(n) for n in ('10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16')]
for a in ('10.255.255.254', '172.15.255.255', '172.16.0.1', '172.31.255.255', '172.32.0.1', '192.167.1.1', '192.168.200.5'):  # lint:allow-ip
    print(a, any(i.ip_address(a) in n for n in PRIVATE))
PY
```

**3. Verify:** so với dự đoán.

## Phần B — Break it (một mạng "nuốt" dải công khai)

```powershell
docker run --rm -it --cap-add NET_ADMIN alpine sh
```

Trong container:

```sh
ip route get 172.32.0.1
ip route add blackhole 172.32.0.0/16
ip route get 172.32.0.1
```

<!-- lint:allow-ip -->
Dự đoán: lần đầu đi theo default route; sau khi thêm `blackhole`, mọi gói tới dải `172.32.0.0/16` bị loại bỏ. Thoát bằng `exit`.

## Dọn dẹp
Container `--rm` tự xóa.

## Ghi kết quả
Lưu vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
