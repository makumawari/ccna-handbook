# Lab 05/04 — VPN IPsec site-to-site (lab rút gọn)

Chapter: [05/04-vpn-ipsec-site-to-site](../../../book/phase-05-security/04-vpn-ipsec-site-to-site.md) · Importance: Should

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## Phạm vi
Chapter Should nên lab rút gọn. Dựng đường hầm IPsec thật cần hai thiết bị VPN và **không** nằm trong lab này. Lab luyện hai điểm hay hỏng nhất: **CIDR chồng lấn** và **MTU**.

## An toàn và chi phí
- Phần A chỉ tính toán. Phần B/C chạy trong container tạm thời (`--rm`, `--cap-add NET_ADMIN`); thay đổi MTU/route chỉ trong container.
- Cần Internet để `apk add iputils` (ping hỗ trợ `-M`).
- Không tạo tài nguyên AWS, không có chi phí.

## Phần A — Kiểm tra CIDR chồng lấn
**1. Predict:** `10.0.0.0/16` & `10.0.5.0/24`? `10.1.0.0/16` & `10.2.0.0/16`? `192.168.0.0/16` & `192.168.1.0/24`?

**2. Run:**

```bash
python3 - <<'PY'
import ipaddress as i
pairs = [('10.0.0.0/16', '10.0.5.0/24'), ('10.1.0.0/16', '10.2.0.0/16'), ('192.168.0.0/16', '192.168.1.0/24')]
for a, b in pairs:
    print(a, b, 'chồng lấn:', i.ip_network(a).overlaps(i.ip_network(b)))
PY
```

## Phần B — MTU giảm sau đóng gói

```powershell
docker run --rm -it --cap-add NET_ADMIN alpine sh
```

```sh
apk add --no-cache iputils
GW=$(ip route show default | awk '{print $3}')
ip link set dev eth0 mtu 1400
ping -M do -s 1372 -c 1 -W 2 $GW
ping -M do -s 1373 -c 1 -W 2 $GW
```

Dự đoán: 1372 (= 1400 − 28) qua được; 1373 báo lỗi kích thước (tin quá dài so với MTU) ngay tại máy.

## Phần C — Break it (chồng lấn trên bảng route)
Trong cùng container:

```sh
ip addr add 10.0.0.1/16 dev lo
ip route add 10.0.7.0/24 via $GW
ip route get 10.0.7.9
ip route get 10.0.8.9
```

Dự đoán: `10.0.7.9` đi qua `$GW` (route cụ thể hơn thắng, "cướp" các máy văn phòng cùng dải); `10.0.8.9` không đi qua `$GW`, rơi vào mạng cục bộ `10.0.0.0/16`. Thoát bằng `exit`.

## Dọn dẹp
Container `--rm` tự xóa.

## Ghi kết quả
Lưu output (đã làm sạch) vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
