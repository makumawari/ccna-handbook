# Lab 06/01 — VPC, subnet và AZ

Chapter: [06/01-vpc-subnet-az](../../../book/phase-06-aws-networking/01-vpc-subnet-az.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- **Phần A hoàn toàn local**, không cần AWS.
- **Phần B tạo tài nguyên AWS**: chỉ chạy trên **tài khoản sandbox riêng**, Region `ap-northeast-1`, gắn tag `Project=net-handbook`, sau khi đã đặt budget alert. VPC và subnet **không tính phí riêng**. Không tạo NAT gateway, endpoint hay instance trong lab này.
- **Không** in hay commit access key, token, `~/.aws/credentials`. Dùng profile/SSO đã cấu hình sẵn.
- Dùng `--dry-run` trước; chỉ chạy lệnh thật khi đã đọc kỹ từng lệnh. Teardown ở cuối là **bắt buộc**.
- Lệnh xóa (`delete-subnet`, `delete-vpc`) chỉ chạy khi bạn chủ động quyết định.

## Phần A — Tính IP dùng được và kiểm tra chồng lấn (local)
**1. Predict:** số IP dùng được của `/28`, `/26`, `/24`, `/20`; cặp CIDR nào chồng lấn?

**2. Run:**

```bash
python3 - <<'PY'
import ipaddress as i

for cidr in ('10.0.1.0/28', '10.0.1.0/26', '10.0.1.0/24', '10.0.16.0/20'):
    n = i.ip_network(cidr)
    print(cidr, 'tổng', n.num_addresses, 'dùng được (trừ 5)', n.num_addresses - 5)

pairs = [('10.0.1.0/24', '10.0.1.128/25'), ('10.0.0.0/16', '10.1.0.0/16'), ('10.0.0.0/24', '10.0.0.0/24')]
for a, b in pairs:
    print(a, b, 'chồng lấn:', i.ip_network(a).overlaps(i.ip_network(b)))

vpc = i.ip_network('10.0.0.0/16')
for sn in vpc.subnets(new_prefix=24):
    if sn.network_address.packed[2] in (0, 1, 10, 11):
        print('subnet kế hoạch:', sn)
PY
```

**3. Verify:** dự đoán `/28` → 11, `/26` → 59, `/24` → 251, `/20` → 4091; cặp 1 và 3 chồng lấn, cặp 2 không.

## Phần B — Tạo VPC và subnet trong sandbox (tùy chọn)
Thay `<vpc-id>` bằng giá trị trả về. Chạy bằng `bash`/WSL (hoặc đổi dấu nối dòng nếu dùng PowerShell).

```bash
export AWS_REGION=ap-northeast-1
aws ec2 create-vpc --cidr-block 10.0.0.0/16 --dry-run \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Project,Value=net-handbook}]'
# Dry-run thành công sẽ báo DryRunOperation; chạy thật khi đã sẵn sàng:
aws ec2 create-vpc --cidr-block 10.0.0.0/16 \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Project,Value=net-handbook}]' \
  --query Vpc.VpcId --output text
aws ec2 create-subnet --vpc-id <vpc-id> --cidr-block 10.0.1.0/28 --availability-zone ap-northeast-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Project,Value=net-handbook}]'
aws ec2 describe-subnets --filters Name=vpc-id,Values=<vpc-id> \
  --query "Subnets[].{az:AvailabilityZone,cidr:CidrBlock,free:AvailableIpAddressCount}" --output table
aws ec2 create-subnet --vpc-id <vpc-id> --cidr-block 10.0.1.0/25 --availability-zone ap-northeast-1c
```

Dự đoán: subnet `/28` mới tạo có `free = 11`; lệnh `create-subnet` cuối (`10.0.1.0/25` chồng lấn `10.0.1.0/28`) bị từ chối với lỗi chồng lấn CIDR.

## Teardown (bắt buộc) và kiểm tra
Chỉ chạy khi bạn đồng ý xóa đúng các tài nguyên mang tag của lab:

```bash
aws ec2 describe-subnets --filters Name=tag:Project,Values=net-handbook --query "Subnets[].SubnetId" --output text
aws ec2 delete-subnet --subnet-id <subnet-id>
aws ec2 delete-vpc --vpc-id <vpc-id>
# Kiểm tra đã xóa hết:
aws ec2 describe-vpcs --filters Name=tag:Project,Values=net-handbook --query "Vpcs[].VpcId" --output text
aws ec2 describe-subnets --filters Name=tag:Project,Values=net-handbook --query "Subnets[].SubnetId" --output text
```
Hai lệnh kiểm tra cuối phải trả về rỗng.

## Ghi kết quả (làm sạch trước khi commit)
Lưu output **đã che** VPC ID, subnet ID, account ID vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
