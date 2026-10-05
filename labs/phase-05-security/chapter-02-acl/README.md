# Lab 05/02 — ACL: thứ tự quy tắc và che khuất

Chapter: [05/02-acl](../../../book/phase-05-security/02-acl.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Phần A chỉ tính toán bằng Python.
- Phần B chạy trong container tạm thời (`--rm`, `--cap-add NET_ADMIN`); quy tắc `iptables` chỉ tồn tại trong container.
- Cần Internet để `apk add iptables`. Không tạo tài nguyên AWS, không có chi phí.

## Phần A — Mô phỏng "khớp đầu tiên"
**1. Predict:** với ACL của Story (100 ALLOW tcp 443 `0.0.0.0/0`; 110 DENY tcp 443 `203.0.113.0/24`; 120 ALLOW tcp 22 `192.0.2.0/24`; `*` DENY), kết quả cho 5 gói trong bảng của chapter; rồi sau khi đổi số 110 thành 90.

**2. Run:**

```bash
python3 - <<'PY'
import ipaddress as i

def evaluate(rules, proto, port, src):
    for num, action, r_proto, r_port, r_src in sorted(rules, key=lambda r: r[0]):
        if r_proto in ('any', proto) and r_port in ('any', port) and i.ip_address(src) in i.ip_network(r_src):
            return f"{action} (quy tắc {num})"
    return "DENY (từ chối ngầm *)"

story = [
    (100, 'ALLOW', 'tcp', 443, '0.0.0.0/0'),
    (110, 'DENY',  'tcp', 443, '203.0.113.0/24'),
    (120, 'ALLOW', 'tcp', 22,  '192.0.2.0/24'),
]
fixed = [(90 if r[0] == 110 else r[0],) + r[1:] for r in story]

packets = [('tcp', 443, '198.51.100.7'), ('tcp', 443, '203.0.113.5'),
           ('tcp', 22, '192.0.2.10'), ('tcp', 22, '198.51.100.7'), ('udp', 53, '198.51.100.7')]
for label, rules in (('GỐC (Story)', story), ('ĐÃ SỬA (110 -> 90)', fixed)):
    print('===', label)
    for p in packets:
        print(' ', p, '->', evaluate(rules, *p))
PY
```

**3. Verify:** so với dự đoán. Kết quả mong đợi (phép tính): chỉ gói `tcp 443 từ 203.0.113.5` đổi từ ALLOW (quy tắc 100) sang DENY (quy tắc 90) sau khi sửa.

## Phần B — Break it (quy tắc bị che khuất trong iptables)

```powershell
docker run --rm -it --cap-add NET_ADMIN alpine sh
```

```sh
apk add --no-cache iptables
(nc -l -p 8080 >/dev/null &)
iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
iptables -A INPUT -p tcp --dport 8080 -s 127.0.0.1 -j DROP
echo hi | nc -w 2 127.0.0.1 8080; echo "mã thoát (DROP bị che): $?"
iptables -L INPUT -n -v --line-numbers
iptables -D INPUT 2
iptables -I INPUT 1 -p tcp --dport 8080 -s 127.0.0.1 -j DROP
(nc -l -p 8080 >/dev/null &)
echo hi | nc -w 2 127.0.0.1 8080; echo "mã thoát (DROP đặt trước): $?"
iptables -L INPUT -n -v --line-numbers
```

Dự đoán: lần đầu thành công (ACCEPT khớp trước), `pkts` của quy tắc DROP bằng 0; sau khi đưa DROP lên đầu, kết nối bị chặn (hết thời gian) và quy tắc DROP có `pkts` lớn hơn 0. Thoát bằng `exit`.

## Dọn dẹp
Container `--rm` tự xóa (quy tắc `iptables` biến mất cùng container).

## Ghi kết quả (làm sạch trước khi commit)
Lưu output (đã làm sạch) vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
