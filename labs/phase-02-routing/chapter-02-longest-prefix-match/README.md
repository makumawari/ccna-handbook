# Lab 02/02 — Longest prefix match

Chapter: [02/02-longest-prefix-match](../../../book/phase-02-routing/02-longest-prefix-match.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Phần A chỉ tính toán bằng Python.
- Phần B chạy trong container tạm thời (`--rm`, `--cap-add NET_ADMIN`); route thêm vào chỉ tồn tại trong container.
- Không có chi phí.

## Phần A — Mô phỏng chọn route
**1. Predict:** với bảng R1–R5 (xem chapter, mục 6), dòng nào thắng cho `198.51.100.5`, `10.9.9.9`, `10.0.9.9`, `10.0.5.7`, `10.0.5.20`?

**2. Run:**

```bash
python3 - <<'PY'
import ipaddress as i

routes = {
    '0.0.0.0/0': 'R1 default',
    '10.0.0.0/8': 'R2',
    '10.0.0.0/16': 'R3',
    '10.0.5.0/24': 'R4',
    '10.0.5.20/32': 'R5 blackhole',
}

def lookup(dst):
    addr = i.ip_address(dst)
    matches = [(i.ip_network(p), name) for p, name in routes.items() if addr in i.ip_network(p)]
    return max(matches, key=lambda m: m[0].prefixlen)

for d in ('198.51.100.5', '10.9.9.9', '10.0.9.9', '10.0.5.7', '10.0.5.20'):
    net, name = lookup(d)
    print(d, '->', name, net)
PY
```

**3. Verify:** so với dự đoán và bảng trong chapter.

## Phần B — Break it (route /32 "bị quên")

```powershell
docker run --rm -it --cap-add NET_ADMIN alpine sh
```

Trong container:

```sh
GW=$(ip route show default | awk '{print $3}')
ip route add 10.0.0.0/16 via $GW
ip route add 10.0.5.0/24 dev eth0
ip route get 10.0.5.20
ip route get 10.0.9.9
ip route add blackhole 10.0.5.20/32
ip route get 10.0.5.20
ip route get 10.0.5.21
ip route del blackhole 10.0.5.20/32
ip route get 10.0.5.20
```

Dự đoán: `10.0.5.20` ban đầu đi thẳng ra `eth0`; `10.0.9.9` qua gateway; sau khi thêm blackhole thì `10.0.5.20` bị loại bỏ nhưng `10.0.5.21` vẫn bình thường; sau khi xóa blackhole thì `10.0.5.20` trở lại bình thường. Thoát bằng `exit`.

## Dọn dẹp
Container `--rm` tự xóa.

## Ghi kết quả (làm sạch trước khi commit)
Thay IP thật bằng IP giả; lưu vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
