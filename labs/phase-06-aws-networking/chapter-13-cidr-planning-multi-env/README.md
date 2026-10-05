# Lab 06/13 — Kiểm tra bảng kế hoạch CIDR (local, chỉ đọc)

Chapter: [06/13-cidr-planning-multi-env](../../../book/phase-06-aws-networking/13-cidr-planning-multi-env.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Lab **hoàn toàn local**, **không tạo tài nguyên AWS**, không có chi phí. Bảng kế hoạch dùng dữ liệu giả.
- Phần tùy chọn đối chiếu với tài khoản thật chỉ dùng lệnh **chỉ đọc** (`describe-vpcs`, `describe-subnets`) trên **tài khoản sandbox riêng**. **Không dán kết quả thật** (CIDR, ID) vào repo; che hết trước khi lưu.
- **Không** in/commit access key, token, `~/.aws/credentials`.

## Phần A — Kiểm tra bảng kế hoạch lỗi (Story)
**1. Predict:** bảng Story có những lỗi nào (chồng lấn, không phải RFC 1918, văn phòng lọt trong VPC, subnet quá nhỏ cho LB)?

**2. Run:**

```bash
python3 - <<'PY'
import ipaddress as i
from itertools import combinations

RFC1918 = [i.ip_network(n) for n in ('10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16')]

def check(plan, subnets=()):
    problems = []
    nets = {name: i.ip_network(cidr) for name, cidr in plan.items()}
    for name, n in nets.items():
        if not any(n.subnet_of(r) for r in RFC1918):
            problems.append(f"{name} {n}: KHÔNG thuộc RFC 1918")
        if n.prefixlen > 28 or (name.startswith('vpc') and n.prefixlen < 16):
            problems.append(f"{name} {n}: kích thước VPC ngoài /16–/28")
    for (a, na), (b, nb) in combinations(nets.items(), 2):
        if na.overlaps(nb):
            problems.append(f"CHỒNG: {a} {na} <-> {b} {nb}")
    for name, cidr in subnets:
        n = i.ip_network(cidr)
        usable = n.num_addresses - 5
        if name.startswith('alb') and (n.prefixlen > 27 or usable - 8 < 0):
            problems.append(f"{name} {n}: nhỏ hơn /27 hoặc thiếu 8 IP trống cho ALB")
    return problems or ['không có vấn đề']

story = {'vpc-stg': '10.0.0.0/16', 'vpc-prd': '10.0.0.0/16', 'vpc-shared': '172.32.0.0/16', 'office': '10.0.5.0/24'}  # lint:allow-ip
print('--- Bảng Story ---')
for p in check(story, [('alb-a', '10.0.1.0/28')]):
    print(' ', p)

fixed = {'vpc-prd': '10.0.0.0/16', 'vpc-stg': '10.1.0.0/16', 'vpc-shared': '10.2.0.0/16', 'office': '192.168.10.0/24'}
print('--- Bảng đã sửa ---')
for p in check(fixed, [('alb-a', '10.0.0.0/24'), ('alb-c', '10.0.1.0/24')]):
    print(' ', p)
PY
```

**3. Verify:** dự đoán bảng Story: `vpc-stg` chồng `vpc-prd`; `vpc-shared` không thuộc RFC 1918; `office` chồng cả `vpc-stg` và `vpc-prd`; `alb-a /28` nhỏ hơn `/27`. Bảng đã sửa: không có vấn đề.

## Phần B — Cấp phát tự động và dự trù IP
**1. Predict:** từ khối `10.0.0.0/8`, cấp `/16` cho 3 VPC còn bao nhiêu `/16` trống? Subnet `/24` đủ cho 2 NAT, 1 ALB (8 IP trống), 4 endpoint, 40 task ECS `awsvpc` không?

**2. Run:**

```bash
python3 - <<'PY'
import ipaddress as i

pool = i.ip_network('10.0.0.0/8')
all16 = list(pool.subnets(new_prefix=16))
allocated = {'prd': all16[0], 'stg': all16[1], 'shared': all16[2]}
print('Đã cấp:', {k: str(v) for k, v in allocated.items()})
print('Số /16 còn trống trong 10.0.0.0/8:', len(all16) - len(allocated))

# Chia /24 trong VPC prd theo vai trò (chỉ số khớp template ở 06/12)
prd = allocated['prd']
subs = list(prd.subnets(new_prefix=24))
plan = {'public-a': subs[0], 'public-c': subs[1], 'app-a': subs[10], 'app-c': subs[11], 'data-a': subs[20], 'data-c': subs[21]}
for k, v in plan.items():
    print(' ', k, v)

usable = 256 - 5
need = {'NAT': 2, 'ALB (chừa >= 8 trống)': 1 + 8, 'interface endpoint': 4, 'ECS awsvpc task': 40}
total = sum(need.values())
print('Cần xấp xỉ:', total, '| dùng được:', usable, '| còn lại:', usable - total)
PY
```

**3. Verify:** dự đoán: khối `10.0.0.0/8` có `256` đoạn `/16`, đã cấp 3 nên còn **253**; cần xấp xỉ **55** IP (2 + 9 + 4 + 40), dùng được **251**, còn lại khoảng **196** trong `/24`.

## Phần C — Đối chiếu với tài khoản thật (TÙY CHỌN, chỉ đọc)
Chạy trên sandbox riêng, **không commit** output thật:

```bash
export AWS_REGION=ap-northeast-1
aws ec2 describe-vpcs --query "Vpcs[].{cidr:CidrBlock,all:CidrBlockAssociationSet[].CidrBlock}" --output json
aws ec2 describe-subnets --query "Subnets[].{cidr:CidrBlock,free:AvailableIpAddressCount}" --output table
```
Dự đoán: nếu bạn dùng default VPC của Region, nó có CIDR do AWS gán sẵn (ghi lại, không giả định giá trị); hãy kiểm tra nó **không chồng** với bảng kế hoạch của bạn trước khi nối bất kỳ thứ gì.

## Dọn dẹp
Không có tài nguyên để dọn.

## Ghi kết quả (làm sạch trước khi commit)
Chỉ lưu output của Phần A và B (dữ liệu giả) vào `expected-output.txt`; **không lưu** output Phần C. Chạy `python tools/lint_chapters.py`.
