# Lab 06/02 — Route table, Internet gateway và NAT gateway

Chapter: [06/02-route-table-igw-nat-gateway](../../../book/phase-06-aws-networking/02-route-table-igw-nat-gateway.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- **Phần A local.** **Phần B** tạo tài nguyên AWS **không tính phí riêng** (VPC, subnet, IGW, route table) nhưng chỉ chạy trên **tài khoản sandbox riêng**, Region `ap-northeast-1`, tag `Project=net-handbook`, sau khi đặt budget alert.
- **Phần C (NAT gateway) TÍNH PHÍ theo giờ và theo GB**, kèm Elastic IP. **Chỉ chạy khi đã kiểm tra giá hiện hành** trên trang pricing của AWS và chấp nhận chi phí; teardown ngay.
- **Không** in/commit access key, token, `~/.aws/credentials`.
- Chạy `--dry-run` khi lệnh hỗ trợ; lệnh xóa chỉ chạy khi bạn chủ động đồng ý.
- Giả định bạn đã có VPC từ lab `06/01` hoặc tạo mới ở Phần B (thay `<...>` bằng giá trị thật của bạn, không commit chúng).

## Phần A — Mô phỏng chọn route (local)
**1. Predict:** `10.0.5.9`, `172.16.0.5`, `198.51.100.8` chọn route nào ở bảng `rt-private-a` (`10.0.0.0/16 → local`, `0.0.0.0/0 → nat`)?

**2. Run:**

```bash
python3 - <<'PY'
import ipaddress as i

table = [('10.0.0.0/16', 'local'), ('172.31.0.0/16', 'pcx-peering'), ('0.0.0.0/0', 'nat-gateway')]

def route(dst):
    ip = i.ip_address(dst)
    best = max((i.ip_network(c) for c, _ in table if ip in i.ip_network(c)), key=lambda n: n.prefixlen)
    return best, dict((i.ip_network(c), t) for c, t in table)[best]

for d in ('10.0.5.9', '172.31.0.5', '172.16.0.5', '198.51.100.8'):
    print(d, '->', *route(d))
PY
```

**3. Verify:** `10.0.5.9 → local`, `172.31.0.5 → pcx-peering` (cụ thể hơn `0.0.0.0/0`), `172.16.0.5` và `198.51.100.8 → nat-gateway`.

## Phần B — IGW, hai route table và bẫy main route table (AWS, không phí)
```bash
export AWS_REGION=ap-northeast-1
VPC=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query Vpc.VpcId --output text \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Project,Value=net-handbook}]')
IGW=$(aws ec2 create-internet-gateway --query InternetGateway.InternetGatewayId --output text \
  --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 attach-internet-gateway --vpc-id "$VPC" --internet-gateway-id "$IGW"
RT_PUB=$(aws ec2 create-route-table --vpc-id "$VPC" --query RouteTable.RouteTableId --output text \
  --tag-specifications 'ResourceType=route-table,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 create-route --route-table-id "$RT_PUB" --destination-cidr-block 0.0.0.0/0 --gateway-id "$IGW"
S_PUB=$(aws ec2 create-subnet --vpc-id "$VPC" --cidr-block 10.0.0.0/24 --availability-zone ap-northeast-1a \
  --query Subnet.SubnetId --output text --tag-specifications 'ResourceType=subnet,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 associate-route-table --route-table-id "$RT_PUB" --subnet-id "$S_PUB"
S_NEW=$(aws ec2 create-subnet --vpc-id "$VPC" --cidr-block 10.0.9.0/24 --availability-zone ap-northeast-1a \
  --query Subnet.SubnetId --output text --tag-specifications 'ResourceType=subnet,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 describe-route-tables --filters Name=vpc-id,Values="$VPC" \
  --query "RouteTables[].{id:RouteTableId,assoc:Associations[].[SubnetId,Main],routes:Routes[].[DestinationCidrBlock,GatewayId]}"
```
Dự đoán: `S_PUB` gắn `RT_PUB` (có route IGW) nên public; `S_NEW` **không** có association riêng, nên dùng main route table (chỉ có `local`) và là private.

**Break it:** thêm route IGW vào main route table, rồi đọc lại:

```bash
MAIN=$(aws ec2 describe-route-tables --filters Name=vpc-id,Values="$VPC" Name=association.main,Values=true \
  --query "RouteTables[0].RouteTableId" --output text)
aws ec2 create-route --route-table-id "$MAIN" --destination-cidr-block 0.0.0.0/0 --gateway-id "$IGW"
aws ec2 describe-route-tables --route-table-ids "$MAIN" --query "RouteTables[].Routes[].[DestinationCidrBlock,GatewayId]"
```
Dự đoán: `S_NEW` (không gắn bảng riêng) giờ dùng main nên có route tới IGW, tức là public. Khôi phục: `aws ec2 delete-route --route-table-id "$MAIN" --destination-cidr-block 0.0.0.0/0`.

## Phần C — NAT gateway (TÍNH PHÍ, tùy chọn)
Chỉ chạy khi đã kiểm tra giá hiện hành và chấp nhận chi phí. Tạo trong **public** subnet `S_PUB`:

```bash
EIP=$(aws ec2 allocate-address --domain vpc --query AllocationId --output text \
  --tag-specifications 'ResourceType=elastic-ip,Tags=[{Key=Project,Value=net-handbook}]')
NAT=$(aws ec2 create-nat-gateway --subnet-id "$S_PUB" --allocation-id "$EIP" \
  --query NatGateway.NatGatewayId --output text \
  --tag-specifications 'ResourceType=natgateway,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 wait nat-gateway-available --nat-gateway-ids "$NAT"
aws ec2 describe-nat-gateways --nat-gateway-ids "$NAT" --query "NatGateways[].{state:State,subnet:SubnetId}"
```
Dự đoán: trạng thái `available`; để một subnet private dùng NAT cần route `0.0.0.0/0 → $NAT` trong route table của subnet đó. **Xóa NAT ngay khi xong** (xem Teardown).

## Teardown (bắt buộc) và kiểm tra
Chỉ chạy khi bạn đồng ý xóa đúng các tài nguyên mang tag của lab. Thứ tự: NAT (nếu có) → chờ xóa xong → giải phóng Elastic IP → route/association → route table → subnet → detach + xóa IGW → xóa VPC.

```bash
aws ec2 delete-nat-gateway --nat-gateway-id "$NAT"      # nếu đã tạo
aws ec2 wait nat-gateway-deleted --nat-gateway-ids "$NAT"
aws ec2 release-address --allocation-id "$EIP"           # nếu đã tạo
aws ec2 delete-route-table --route-table-id "$RT_PUB"    # có thể cần disassociate trước (AssociationId trong describe-route-tables)
aws ec2 delete-subnet --subnet-id "$S_PUB"
aws ec2 delete-subnet --subnet-id "$S_NEW"
aws ec2 detach-internet-gateway --internet-gateway-id "$IGW" --vpc-id "$VPC"
aws ec2 delete-internet-gateway --internet-gateway-id "$IGW"
aws ec2 delete-vpc --vpc-id "$VPC"
```

Kiểm tra đã xóa hết (mọi lệnh phải trả về rỗng):

```bash
aws ec2 describe-vpcs --filters Name=tag:Project,Values=net-handbook --query "Vpcs[].VpcId" --output text
aws ec2 describe-nat-gateways --filter Name=tag:Project,Values=net-handbook Name=state,Values=available,pending --query "NatGateways[].NatGatewayId" --output text
aws ec2 describe-addresses --filters Name=tag:Project,Values=net-handbook --query "Addresses[].AllocationId" --output text
aws ec2 describe-internet-gateways --filters Name=tag:Project,Values=net-handbook --query "InternetGateways[].InternetGatewayId" --output text
```

## Ghi kết quả (làm sạch trước khi commit)
Lưu output **đã che** mọi ID và account ID vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
