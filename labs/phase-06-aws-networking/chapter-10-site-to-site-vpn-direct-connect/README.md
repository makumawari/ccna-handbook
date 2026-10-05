# Lab 06/10 — Site-to-Site VPN và Direct Connect (lab rút gọn)

Chapter: [06/10-site-to-site-vpn-direct-connect](../../../book/phase-06-aws-networking/10-site-to-site-vpn-direct-connect.md) · Importance: Should

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- **Phần A local.** **Phần B** chỉ tạo **customer gateway** và **virtual private gateway** (không tạo VPN connection, không tạo Direct Connect). Chi phí riêng của hai tài nguyên này `[CHƯA KIỂM CHỨNG]`: kiểm tra bảng giá hiện hành trước khi chạy. **VPN connection TÍNH PHÍ THEO GIỜ** nên **không tạo** trong lab này.
- Địa chỉ customer gateway dùng IP tài liệu `203.0.113.10` (RFC 5737), **không** dùng IP thật của văn phòng hay thiết bị.
- Chỉ chạy trên **tài khoản sandbox riêng**, Region `ap-northeast-1`, tag `Project=net-handbook`, sau khi đặt budget alert.
- **Không** in/commit access key, token, pre-shared key, `~/.aws/credentials`. Lệnh xóa chỉ chạy khi bạn chủ động đồng ý.

## Phần A — Mô phỏng ưu tiên route (local)
**1. Predict:** `10.0.5.9` đi qua route nào khi VPC là `10.0.0.0/16` và có route lan truyền `10.0.5.0/24` từ VPN? Cùng prefix, route nào thắng giữa BGP Direct Connect, static VPN, BGP VPN?

**2. Run:**

```bash
python3 - <<'PY'
import ipaddress as i

# route: (cidr, origin)
vpc_cidr = i.ip_network('10.0.0.0/16')
routes = [('10.0.0.0/16', 'local'), ('10.0.5.0/24', 'vpn-propagated'), ('0.0.0.0/0', 'igw-static')]

def choose(dst):
    ip = i.ip_address(dst)
    if ip in vpc_cidr:
        return 'local (luôn thắng route lan truyền chồng CIDR VPC)'
    matches = [(i.ip_network(c), o) for c, o in routes if ip in i.ip_network(c)]
    best = max(matches, key=lambda m: m[0].prefixlen)
    return f"{best[0]} -> {best[1]}"

for d in ('10.0.5.9', '198.51.100.20'):
    print(d, '->', choose(d))

order = ['BGP từ Direct Connect', 'Static của VPN', 'BGP từ VPN']
print('Thứ tự ưu tiên cùng prefix (cao -> thấp):', ' > '.join(order))
PY
```

**3. Verify:** dự đoán `10.0.5.9 → local`; `198.51.100.20 → 0.0.0.0/0 → igw-static`; thứ tự `DX BGP > static VPN > BGP VPN`.

## Phần B — Customer gateway và virtual private gateway (không tạo VPN connection)
Thay `<...>` bằng giá trị của bạn (không commit chúng). Chạy bằng `bash`/WSL.

```bash
export AWS_REGION=ap-northeast-1
VPC=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query Vpc.VpcId --output text \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Project,Value=net-handbook}]')
CGW=$(aws ec2 create-customer-gateway --type ipsec.1 --bgp-asn 65010 --public-ip 203.0.113.10 \
  --query CustomerGateway.CustomerGatewayId --output text \
  --tag-specifications 'ResourceType=customer-gateway,Tags=[{Key=Project,Value=net-handbook}]')
VGW=$(aws ec2 create-vpn-gateway --type ipsec.1 --query VpnGateway.VpnGatewayId --output text \
  --tag-specifications 'ResourceType=vpn-gateway,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 attach-vpn-gateway --vpn-gateway-id "$VGW" --vpc-id "$VPC"
aws ec2 describe-vpn-gateways --vpn-gateway-ids "$VGW" --query "VpnGateways[].{asn:AmazonSideAsn,state:State,att:VpcAttachments[].State}"
RT=$(aws ec2 describe-route-tables --filters Name=vpc-id,Values="$VPC" Name=association.main,Values=true \
  --query "RouteTables[0].RouteTableId" --output text)
aws ec2 enable-vgw-route-propagation --route-table-id "$RT" --gateway-id "$VGW"
aws ec2 describe-route-tables --route-table-ids "$RT" --query "RouteTables[].PropagatingVgws"
```
Dự đoán: VGW có ASN phía Amazon mặc định `64512` (không đổi được sau khi tạo), trạng thái `available` và attachment `attached`; sau khi bật propagation, route table liệt kê VGW trong `PropagatingVgws`; chưa có route nào được lan truyền vì chưa có VPN connection.

**Break it (đọc):** nêu bằng lời vì sao chỉ có VGW và CGW mà VPC vẫn chưa có đường tới dải on-premise, và bước nào còn thiếu (tạo VPN connection và cấu hình thiết bị).

## Teardown (bắt buộc) và kiểm tra
```bash
aws ec2 disable-vgw-route-propagation --route-table-id "$RT" --gateway-id "$VGW"
aws ec2 detach-vpn-gateway --vpn-gateway-id "$VGW" --vpc-id "$VPC"
sleep 30   # chờ VGW gỡ khỏi VPC
aws ec2 delete-vpn-gateway --vpn-gateway-id "$VGW"
aws ec2 delete-customer-gateway --customer-gateway-id "$CGW"
aws ec2 delete-vpc --vpc-id "$VPC"
```
(Nếu `delete-vpn-gateway` báo còn attachment, chờ vài chục giây rồi chạy lại.) Kiểm tra (phải trả về rỗng):

```bash
aws ec2 describe-vpn-gateways --filters Name=tag:Project,Values=net-handbook Name=state,Values=available,pending --query "VpnGateways[].VpnGatewayId" --output text
aws ec2 describe-customer-gateways --filters Name=tag:Project,Values=net-handbook Name=state,Values=available,pending --query "CustomerGateways[].CustomerGatewayId" --output text
aws ec2 describe-vpcs --filters Name=tag:Project,Values=net-handbook --query "Vpcs[].VpcId" --output text
```

## Ghi kết quả (làm sạch trước khi commit)
Lưu output **đã che** mọi ID và account ID vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
