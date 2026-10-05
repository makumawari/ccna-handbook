# Lab 06/09 — VPC peering (lab rút gọn)

Chapter: [06/09-vpc-peering-transit-gateway](../../../book/phase-06-aws-networking/09-vpc-peering-transit-gateway.md) · Importance: Should

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- **Phần A local.** **Phần B** tạo hai VPC trống và một peering cùng tài khoản/cùng Region: **không phí tạo**, không có instance nên không có lưu lượng. **Không tạo Transit Gateway trong lab này** (TGW tính phí theo giờ mỗi attachment và theo GB).
- Chỉ chạy trên **tài khoản sandbox riêng**, Region `ap-northeast-1`, tag `Project=net-handbook`, sau khi đặt budget alert.
- **Không** in/commit access key, token, `~/.aws/credentials`. Lệnh xóa chỉ chạy khi bạn chủ động đồng ý.

## Phần A — Kiểm tra CIDR và "không bắc cầu" (local)
**1. Predict:** peering giữa `10.0.0.0/16` và `10.0.0.0/24` được không? Với A–B, A–C peering, đường B→C qua A có tồn tại không?

**2. Run:**

```bash
python3 - <<'PY'
import ipaddress as i

pairs = [('10.0.0.0/16', '10.0.0.0/24'), ('10.0.0.0/16', '10.1.0.0/16'), ('10.1.0.0/16', '10.2.0.0/16')]
for a, b in pairs:
    print(a, b, 'peering được:', not i.ip_network(a).overlaps(i.ip_network(b)))

peerings = {frozenset(('A', 'B')), frozenset(('A', 'C'))}
def reachable(src, dst):
    return frozenset((src, dst)) in peerings        # peering KHÔNG bắc cầu: chỉ nối trực tiếp
for s, d in (('A', 'B'), ('A', 'C'), ('B', 'C')):
    print(s, '->', d, 'qua peering trực tiếp:', reachable(s, d))
PY
```

**3. Verify:** dự đoán cặp 1 không peering được (chồng), cặp 2 và 3 được; `A→B` và `A→C` đúng, `B→C` sai.

## Phần B — Hai VPC và một peering (AWS, không phí tạo)
Thay `<...>` bằng giá trị của bạn (không commit chúng). Chạy bằng `bash`/WSL.

```bash
export AWS_REGION=ap-northeast-1
VPC_A=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query Vpc.VpcId --output text \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Project,Value=net-handbook}]')
VPC_B=$(aws ec2 create-vpc --cidr-block 10.1.0.0/16 --query Vpc.VpcId --output text \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Project,Value=net-handbook}]')
PCX=$(aws ec2 create-vpc-peering-connection --vpc-id "$VPC_A" --peer-vpc-id "$VPC_B" \
  --query VpcPeeringConnection.VpcPeeringConnectionId --output text \
  --tag-specifications 'ResourceType=vpc-peering-connection,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 describe-vpc-peering-connections --vpc-peering-connection-ids "$PCX" --query "VpcPeeringConnections[].Status.Code"
aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id "$PCX" --query "VpcPeeringConnection.Status.Code"
RT_A=$(aws ec2 describe-route-tables --filters Name=vpc-id,Values="$VPC_A" Name=association.main,Values=true \
  --query "RouteTables[0].RouteTableId" --output text)
RT_B=$(aws ec2 describe-route-tables --filters Name=vpc-id,Values="$VPC_B" Name=association.main,Values=true \
  --query "RouteTables[0].RouteTableId" --output text)
aws ec2 create-route --route-table-id "$RT_A" --destination-cidr-block 10.1.0.0/16 --vpc-peering-connection-id "$PCX"
aws ec2 describe-route-tables --route-table-ids "$RT_A" "$RT_B" \
  --query "RouteTables[].{rt:RouteTableId,routes:Routes[].[DestinationCidrBlock,VpcPeeringConnectionId]}"
```
Dự đoán: trạng thái `pending-acceptance` rồi `provisioning`/`active` sau khi chấp nhận; route table của A có route `10.1.0.0/16 → pcx-...` còn của B **chưa** có route về A (một chiều).

**Break it:** thử tạo peering với một VPC chồng CIDR:

```bash
VPC_C=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query Vpc.VpcId --output text \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 create-vpc-peering-connection --vpc-id "$VPC_A" --peer-vpc-id "$VPC_C"
```
Dự đoán: lệnh bị từ chối (CIDR chồng). Sau đó thêm route `10.0.0.0/16 → $PCX` ở B và nêu bằng lời vì sao đó là route hợp lệ đối với peering A–B.

## Teardown (bắt buộc) và kiểm tra
```bash
aws ec2 delete-route --route-table-id "$RT_A" --destination-cidr-block 10.1.0.0/16
aws ec2 delete-vpc-peering-connection --vpc-peering-connection-id "$PCX"
aws ec2 delete-vpc --vpc-id "$VPC_C"
aws ec2 delete-vpc --vpc-id "$VPC_B"
aws ec2 delete-vpc --vpc-id "$VPC_A"
```
Kiểm tra (phải trả về rỗng; peering đã xóa có thể còn hiện trạng thái `deleted` một thời gian):

```bash
aws ec2 describe-vpcs --filters Name=tag:Project,Values=net-handbook --query "Vpcs[].VpcId" --output text
aws ec2 describe-vpc-peering-connections --filters Name=tag:Project,Values=net-handbook Name=status-code,Values=active,pending-acceptance,provisioning --query "VpcPeeringConnections[].VpcPeeringConnectionId" --output text
```

## Ghi kết quả (làm sạch trước khi commit)
Lưu output **đã che** mọi ID và account ID vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
