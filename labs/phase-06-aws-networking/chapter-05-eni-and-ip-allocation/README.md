# Lab 06/05 — ENI và giữ chỗ IP

Chapter: [06/05-eni-and-ip-allocation](../../../book/phase-06-aws-networking/05-eni-and-ip-allocation.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- **Phần A local.** **Phần B** chỉ dùng IP riêng: **không tạo instance, không tạo IP công khai/Elastic IP**, nên không tính phí riêng. Vẫn chỉ chạy trên **tài khoản sandbox riêng**, Region `ap-northeast-1`, tag `Project=net-handbook`, sau khi đặt budget alert.
- **Không** in/commit access key, token, `~/.aws/credentials`. Lệnh xóa chỉ chạy khi bạn chủ động đồng ý.

## Phần A — Mô phỏng cấp IP và giữ chỗ (local)
**1. Predict:** khi không giữ chỗ, các ENI do dịch vụ tạo lấy IP nào trước? `10.0.10.4` còn dùng được sau 3 ENI không?

**2. Run:**

```bash
python3 - <<'PY'
import ipaddress as i

net = i.ip_network('10.0.10.0/24')
reserved = {net.network_address + k for k in range(4)} | {net.broadcast_address}
used = {}

def allocate(owner, want=None):
    if want is not None:
        ip = i.ip_address(want)
        if ip in reserved or ip in used or ip not in net:
            return f"{owner}: TỪ CHỐI {ip}"
        used[ip] = owner
        return f"{owner}: {ip}"
    for ip in net:
        if ip not in reserved and ip not in used:
            used[ip] = owner
            return f"{owner}: {ip}"

print('--- không giữ chỗ (mô phỏng: lấy IP trống đầu tiên) ---')
for o in ('endpoint-ssm', 'endpoint-ec2messages', 'ecs-task'):
    print(allocate(o))
print(allocate('database-tuan-sau', '10.0.10.4'))

used.clear()
print('--- có giữ chỗ trước ---')
print(allocate('eni-giu-cho-db', '10.0.10.4'))
for o in ('endpoint-ssm', 'endpoint-ec2messages', 'ecs-task'):
    print(allocate(o))
print(allocate('xin-lai-ip-da-giu', '10.0.10.4'))
print(allocate('xin-ip-bi-giu-boi-aws', '10.0.10.3'))
PY
```

**3. Verify:** dự đoán phần "không giữ chỗ": endpoint-ssm lấy `.4`, endpoint-ec2messages `.5`, ecs-task `.6`, và `database-tuan-sau` xin `.4` bị **từ chối**; phần "có giữ chỗ": ENI giữ chỗ lấy `.4` trước, ba dịch vụ lấy `.5` `.6` `.7`, xin lại `.4` và xin `.3` đều bị từ chối. (Mô phỏng đơn giản; AWS có thể chọn IP theo cách khác.)

## Phần B — ENI giữ chỗ trong sandbox (không phí)
Thay `<...>` bằng giá trị của bạn (không commit chúng). Chạy bằng `bash`/WSL.

```bash
export AWS_REGION=ap-northeast-1
VPC=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query Vpc.VpcId --output text \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Project,Value=net-handbook}]')
SN=$(aws ec2 create-subnet --vpc-id "$VPC" --cidr-block 10.0.10.0/24 --availability-zone ap-northeast-1a \
  --query Subnet.SubnetId --output text --tag-specifications 'ResourceType=subnet,Tags=[{Key=Project,Value=net-handbook}]')
ENI1=$(aws ec2 create-network-interface --subnet-id "$SN" --private-ip-address 10.0.10.4 \
  --description "lab 06/05 giu cho" --query NetworkInterface.NetworkInterfaceId --output text \
  --tag-specifications 'ResourceType=network-interface,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 describe-network-interfaces --network-interface-ids "$ENI1" \
  --query "NetworkInterfaces[].{ip:PrivateIpAddress,status:Status,managed:RequesterManaged}"
aws ec2 describe-subnets --subnet-ids "$SN" --query "Subnets[].AvailableIpAddressCount"
```
Dự đoán: ENI có IP `10.0.10.4`, trạng thái `available` (chưa gắn), `managed = false`; `AvailableIpAddressCount` giảm 1 so với 251.

**Break it — IP đã giữ và IP bị AWS giữ:**

```bash
aws ec2 create-network-interface --subnet-id "$SN" --private-ip-address 10.0.10.4 --description "lab trung IP"
aws ec2 create-network-interface --subnet-id "$SN" --private-ip-address 10.0.10.3 --description "lab ip bi giu"
ENI2=$(aws ec2 create-network-interface --subnet-id "$SN" --description "lab tu cap" \
  --query NetworkInterface.NetworkInterfaceId --output text \
  --tag-specifications 'ResourceType=network-interface,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 describe-network-interfaces --network-interface-ids "$ENI2" --query "NetworkInterfaces[].PrivateIpAddress"
```
Dự đoán: hai lệnh đầu bị từ chối (IP đã dùng; IP nằm trong dải AWS giữ); ENI thứ hai không chỉ định IP nhận một IP trống do AWS chọn (ghi lại IP nào, không giả định thứ tự).

## Teardown (bắt buộc) và kiểm tra
```bash
aws ec2 delete-network-interface --network-interface-id "$ENI2"
aws ec2 delete-network-interface --network-interface-id "$ENI1"
aws ec2 delete-subnet --subnet-id "$SN"
aws ec2 delete-vpc --vpc-id "$VPC"
```
Kiểm tra (phải trả về rỗng):

```bash
aws ec2 describe-network-interfaces --filters Name=tag:Project,Values=net-handbook --query "NetworkInterfaces[].NetworkInterfaceId" --output text
aws ec2 describe-subnets --filters Name=tag:Project,Values=net-handbook --query "Subnets[].SubnetId" --output text
aws ec2 describe-vpcs --filters Name=tag:Project,Values=net-handbook --query "Vpcs[].VpcId" --output text
```

## Ghi kết quả (làm sạch trước khi commit)
Lưu output **đã che** mọi ID và account ID vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
