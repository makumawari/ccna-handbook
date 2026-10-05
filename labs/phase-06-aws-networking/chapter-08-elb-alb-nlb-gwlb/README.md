# Lab 06/08 — ALB, subnet và health check

Chapter: [06/08-elb-alb-nlb-gwlb](../../../book/phase-06-aws-networking/08-elb-alb-nlb-gwlb.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- **Phần A hoàn toàn local.**
- **Phần B tạo một Application Load Balancer: ALB TÍNH PHÍ THEO GIỜ (và theo dung lượng).** Chỉ chạy khi đã **kiểm tra giá hiện hành** (Elastic Load Balancing pricing) và chấp nhận chi phí; dùng **scheme `internal`** để tránh IPv4 công khai; **teardown ngay** sau khi quan sát. Một ALB bị bỏ quên là nguồn tốn tiền kinh điển.
- Chỉ chạy trên **tài khoản sandbox riêng**, Region `ap-northeast-1`, tag `Project=net-handbook`, sau khi đặt budget alert.
- **Không** in/commit access key, token, `~/.aws/credentials`. Lệnh xóa chỉ chạy khi bạn chủ động đồng ý.
- Không tạo target hay instance trong lab này.

## Phần A — Kích thước subnet và thời gian health check (local)
**1. Predict:** với `/27`, `/28` có bao nhiêu IP dùng được? Mặc định health check (chu kỳ 30 giây, hỏng 2, khỏe 5) phát hiện hỏng và phục hồi mất bao lâu?

**2. Run:**

```bash
python3 - <<'PY'
import ipaddress as i

for cidr in ('10.0.0.0/28', '10.0.0.0/27', '10.0.0.0/26'):
    n = i.ip_network(cidr)
    usable = n.num_addresses - 5
    print(cidr, 'dùng được', usable, '| sau khi chừa 8 IP cho LB mở rộng:', usable - 8)

interval, unhealthy, healthy = 30, 2, 5
print('phát hiện hỏng (xấp xỉ):', interval * unhealthy, 'giây')
print('phục hồi (xấp xỉ):', interval * healthy, 'giây')
PY
```

**3. Verify:** dự đoán `/28` → 11 (còn 3 sau khi chừa 8), `/27` → 27 (còn 19), `/26` → 59 (còn 51); phát hiện hỏng ≈ 60 giây, phục hồi ≈ 150 giây.

## Phần B — ALB internal không target (TÍNH PHÍ, tùy chọn)
Thay `<...>` bằng giá trị của bạn (không commit chúng). Chạy bằng `bash`/WSL.

```bash
export AWS_REGION=ap-northeast-1
VPC=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query Vpc.VpcId --output text \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Project,Value=net-handbook}]')
SA=$(aws ec2 create-subnet --vpc-id "$VPC" --cidr-block 10.0.0.0/27 --availability-zone ap-northeast-1a \
  --query Subnet.SubnetId --output text --tag-specifications 'ResourceType=subnet,Tags=[{Key=Project,Value=net-handbook}]')
SC=$(aws ec2 create-subnet --vpc-id "$VPC" --cidr-block 10.0.0.32/27 --availability-zone ap-northeast-1c \
  --query Subnet.SubnetId --output text --tag-specifications 'ResourceType=subnet,Tags=[{Key=Project,Value=net-handbook}]')
SG=$(aws ec2 create-security-group --group-name lab-alb-sg --description "lab 06/08" --vpc-id "$VPC" \
  --query GroupId --output text --tag-specifications 'ResourceType=security-group,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 describe-subnets --subnet-ids "$SA" "$SC" --query "Subnets[].AvailableIpAddressCount"
ALB=$(aws elbv2 create-load-balancer --name lab-alb-0608 --type application --scheme internal \
  --subnets "$SA" "$SC" --security-groups "$SG" --tags Key=Project,Value=net-handbook \
  --query "LoadBalancers[0].LoadBalancerArn" --output text)
aws elbv2 wait load-balancer-available --load-balancer-arns "$ALB"
aws elbv2 describe-load-balancers --load-balancer-arns "$ALB" --query "LoadBalancers[].State.Code"
aws ec2 describe-subnets --subnet-ids "$SA" "$SC" --query "Subnets[].AvailableIpAddressCount"
aws ec2 describe-network-interfaces --filters Name=subnet-id,Values="$SA" \
  --query "NetworkInterfaces[].{ip:PrivateIpAddress,desc:Description,managed:RequesterManaged}" --output table
```
Dự đoán: ban đầu mỗi subnet `27` địa chỉ trống; sau khi tạo ALB, trạng thái `active` và số IP trống **giảm** (mỗi nút dùng IP; ghi lại mức giảm thực tế, không giả định); trong subnet có ENI mô tả liên quan ELB do dịch vụ quản lý (`managed = true`), gồm ENI giữ chỗ "ENI reserved by ELB for subnet".

**Break it (đọc):** nêu bằng lời điều gì xảy ra với ALB nếu hai subnet này là `/28` và bị lấp đầy bởi các ENI khác (xem `06/05`), và chỉ số nào bạn sẽ theo dõi.

## Teardown (bắt buộc, làm ngay) và kiểm tra
Xóa ALB trước để dừng tính phí:

```bash
aws elbv2 delete-load-balancer --load-balancer-arn "$ALB"
aws elbv2 wait load-balancers-deleted --load-balancer-arns "$ALB"
aws ec2 delete-security-group --group-id "$SG"
aws ec2 delete-subnet --subnet-id "$SA"
aws ec2 delete-subnet --subnet-id "$SC"
aws ec2 delete-vpc --vpc-id "$VPC"
```
(ENI do ELB tạo có thể mất ít phút để được dọn; nếu xóa subnet/SG báo đang dùng, chờ rồi thử lại.) Kiểm tra (phải trả về rỗng):

```bash
aws elbv2 describe-load-balancers --query "LoadBalancers[?LoadBalancerName=='lab-alb-0608'].LoadBalancerArn" --output text
aws ec2 describe-vpcs --filters Name=tag:Project,Values=net-handbook --query "Vpcs[].VpcId" --output text
aws ec2 describe-network-interfaces --filters Name=tag:Project,Values=net-handbook --query "NetworkInterfaces[].NetworkInterfaceId" --output text
```

## Ghi kết quả (làm sạch trước khi commit)
Lưu output **đã che** ARN, ID và account ID vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
