# Lab 06/04 — VPC endpoint: Gateway, Interface

Chapter: [06/04-vpc-endpoints-gateway-interface-gwlb](../../../book/phase-06-aws-networking/04-vpc-endpoints-gateway-interface-gwlb.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- **Phần A local.** **Phần B** (Gateway endpoint cho S3) **không tính phí thêm**.
- **Phần C (Interface endpoint) TÍNH PHÍ theo giờ (mỗi endpoint, mỗi AZ) và theo GB.** Chỉ chạy khi đã **kiểm tra giá hiện hành** (trang PrivateLink pricing) và chấp nhận chi phí; teardown ngay sau khi xong.
- Chỉ chạy trên **tài khoản sandbox riêng**, Region `ap-northeast-1`, tag `Project=net-handbook`, sau khi đặt budget alert.
- **Không** in/commit access key, token, `~/.aws/credentials`. Lệnh xóa chỉ chạy khi bạn chủ động đồng ý.
- Tạo/sửa Gateway endpoint làm đổi route và có thể cắt kết nối TCP đang mở tới S3; chạy trên VPC lab trống, không phải VPC đang dùng thật.

## Phần A — Kế hoạch IP cho ENI endpoint (local)
**1. Predict:** subnet `10.0.10.0/24`, bạn định gán `10.0.10.4` cho một server về sau. Endpoint tạo ENI tự cấp IP: IP đầu tiên còn trống là gì? Bạn tránh va chạm bằng cách nào?

**2. Run:**

```bash
python3 - <<'PY'
import ipaddress as i

net = i.ip_network('10.0.10.0/24')
# AWS giữ 4 địa chỉ đầu (.0 .1 .2 .3) và địa chỉ cuối
reserved = {net.network_address + k for k in range(4)} | {net.broadcast_address}
planned = {i.ip_address('10.0.10.4')}      # IP định gán cho server về sau
used = set()                               # ENI/instance đã tồn tại

def first_free(excluded):
    for ip in net:
        if ip not in excluded:
            return ip

print('IP đầu tiên endpoint có thể lấy (chưa giữ chỗ):', first_free(reserved | used))
print('Va chạm với IP định gán?', first_free(reserved | used) in planned)
used.add(first_free(reserved | used))
print('Sau khi tạo endpoint thứ hai:', first_free(reserved | used))
PY
```

**3. Verify:** dự đoán IP đầu tiên là `10.0.10.4` (sau 4 địa chỉ bị giữ) và **va chạm** với IP định gán; sau khi một endpoint lấy `.4`, endpoint tiếp theo lấy `.5`. (Mô phỏng đơn giản; AWS có thể chọn IP theo cách khác, hãy chỉ định IP hoặc giữ chỗ trước.)

## Phần B — Gateway endpoint cho S3 (không phí thêm)
Thay `<...>` bằng giá trị của bạn (không commit chúng). Chạy bằng `bash`/WSL.

```bash
export AWS_REGION=ap-northeast-1
VPC=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query Vpc.VpcId --output text \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Project,Value=net-handbook}]')
RT=$(aws ec2 create-route-table --vpc-id "$VPC" --query RouteTable.RouteTableId --output text \
  --tag-specifications 'ResourceType=route-table,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 describe-route-tables --route-table-ids "$RT" --query "RouteTables[].Routes[].[DestinationCidrBlock,DestinationPrefixListId,GatewayId]"
VPCE=$(aws ec2 create-vpc-endpoint --vpc-id "$VPC" --vpc-endpoint-type Gateway \
  --service-name com.amazonaws.ap-northeast-1.s3 --route-table-ids "$RT" \
  --query VpcEndpoint.VpcEndpointId --output text \
  --tag-specifications 'ResourceType=vpc-endpoint,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 describe-route-tables --route-table-ids "$RT" --query "RouteTables[].Routes[].[DestinationCidrBlock,DestinationPrefixListId,GatewayId]"
```
Dự đoán: trước khi tạo endpoint chỉ có route `local`; sau đó có thêm một route với **đích là prefix list** của S3 (`pl-...`) và target là `vpce-...`.

**Break it:** gỡ route table khỏi endpoint rồi đọc lại:

```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id "$VPCE" --remove-route-table-ids "$RT"
aws ec2 describe-route-tables --route-table-ids "$RT" --query "RouteTables[].Routes[].[DestinationPrefixListId,GatewayId]"
```
Dự đoán: route prefix list biến mất; endpoint vẫn tồn tại nhưng subnet gắn bảng này không còn dùng nó.

## Phần C — Interface endpoint (TÍNH PHÍ, tùy chọn)
Chỉ chạy khi đã kiểm tra giá hiện hành. Cần subnet và security group (cho phép HTTPS 443 vào từ CIDR của VPC):

```bash
S=$(aws ec2 create-subnet --vpc-id "$VPC" --cidr-block 10.0.10.0/24 --availability-zone ap-northeast-1a \
  --query Subnet.SubnetId --output text --tag-specifications 'ResourceType=subnet,Tags=[{Key=Project,Value=net-handbook}]')
SG=$(aws ec2 create-security-group --group-name lab-vpce-sg --description "lab 06/04" --vpc-id "$VPC" \
  --query GroupId --output text --tag-specifications 'ResourceType=security-group,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 authorize-security-group-ingress --group-id "$SG" --protocol tcp --port 443 --cidr 10.0.0.0/16
aws ec2 modify-vpc-attribute --vpc-id "$VPC" --enable-dns-support '{"Value":true}'
aws ec2 modify-vpc-attribute --vpc-id "$VPC" --enable-dns-hostnames '{"Value":true}'
IVPCE=$(aws ec2 create-vpc-endpoint --vpc-id "$VPC" --vpc-endpoint-type Interface \
  --service-name com.amazonaws.ap-northeast-1.ssm --subnet-ids "$S" --security-group-ids "$SG" \
  --private-dns-enabled --query VpcEndpoint.VpcEndpointId --output text \
  --tag-specifications 'ResourceType=vpc-endpoint,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 describe-vpc-endpoints --vpc-endpoint-ids "$IVPCE" --query "VpcEndpoints[].{state:State,privDns:PrivateDnsEnabled}"
aws ec2 describe-network-interfaces --filters Name=requester-managed,Values=true Name=subnet-id,Values="$S" \
  --query "NetworkInterfaces[].{ip:PrivateIpAddress,desc:Description}"
```
Dự đoán: endpoint chuyển từ `pending` sang `available`; có một ENI loại endpoint trong subnet với IP riêng (không trùng 4 địa chỉ đầu); không có instance nên chưa kiểm tra DNS/`nc` từ trong VPC (cần một instance, ngoài phạm vi lab này).

## Teardown (bắt buộc) và kiểm tra
Chỉ chạy khi bạn đồng ý xóa đúng các tài nguyên mang tag của lab. **Xóa Interface endpoint trước** để dừng tính phí.

```bash
aws ec2 delete-vpc-endpoints --vpc-endpoint-ids "$IVPCE"      # nếu đã tạo (Phần C)
aws ec2 delete-vpc-endpoints --vpc-endpoint-ids "$VPCE"
aws ec2 delete-security-group --group-id "$SG"                 # nếu đã tạo
aws ec2 delete-subnet --subnet-id "$S"                         # nếu đã tạo
aws ec2 delete-route-table --route-table-id "$RT"
aws ec2 delete-vpc --vpc-id "$VPC"
```
Kiểm tra (mọi lệnh phải trả về rỗng, có thể cần chờ endpoint chuyển `deleted`):

```bash
aws ec2 describe-vpc-endpoints --filters Name=tag:Project,Values=net-handbook --query "VpcEndpoints[?State!='deleted'].VpcEndpointId" --output text
aws ec2 describe-vpcs --filters Name=tag:Project,Values=net-handbook --query "Vpcs[].VpcId" --output text
aws ec2 describe-network-interfaces --filters Name=requester-managed,Values=true --query "NetworkInterfaces[].NetworkInterfaceId" --output text
```

## Ghi kết quả (làm sạch trước khi commit)
Lưu output **đã che** mọi ID, IP thật và account ID vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
