# Lab 06/03 — Security group và network ACL

Chapter: [06/03-security-group-and-nacl](../../../book/phase-06-aws-networking/03-security-group-and-nacl.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- **Phần A hoàn toàn local.**
- **Phần B** tạo VPC, security group, network ACL: **không tính phí riêng**. Chỉ chạy trên **tài khoản sandbox riêng**, Region `ap-northeast-1`, tag `Project=net-handbook`, sau khi đặt budget alert. **Không tạo instance** trong lab này.
- Reachability Analyzer (phần tùy chọn) có thể tính phí theo mỗi lần phân tích: **kiểm tra giá hiện hành** trước khi chạy.
- **Không** in/commit access key, token, `~/.aws/credentials`. Lệnh xóa chỉ chạy khi bạn chủ động đồng ý.

## Phần A — Mô phỏng NACL (stateless) và SG (allow-only, stateful)
**1. Predict:** gói `tcp 8080` từ `10.0.1.10` tới `10.0.1.20` (cùng `sg-app`, SG không có quy tắc tự tham chiếu) được hay bị chặn? Sau khi thêm quy tắc tự tham chiếu? Chiều trả lời qua NACL chỉ cho 443 vào có qua không?

**2. Run:**

```bash
python3 - <<'PY'
import ipaddress as i

def sg_allows(rules, proto, port, src_ip, src_groups):
    for r in rules:
        if r['proto'] in ('any', proto) and r['lo'] <= port <= r['hi']:
            if 'cidr' in r and i.ip_address(src_ip) in i.ip_network(r['cidr']):
                return True
            if 'sg' in r and r['sg'] in src_groups:
                return True
    return False

def nacl_allows(rules, proto, port, ip):
    for num, action, r_proto, lo, hi, cidr in sorted(rules):
        if r_proto in ('any', proto) and lo <= port <= hi and i.ip_address(ip) in i.ip_network(cidr):
            return action == 'ALLOW'
    return False

# Phần 1: cùng SG, chưa có quy tắc tự tham chiếu
sg_app = []
print('cùng SG, chưa quy tắc:', sg_allows(sg_app, 'tcp', 8080, '10.0.1.10', {'sg-app'}))
sg_app = [{'proto': 'tcp', 'lo': 8080, 'hi': 8080, 'sg': 'sg-app'}]
print('cùng SG, có tự tham chiếu:', sg_allows(sg_app, 'tcp', 8080, '10.0.1.10', {'sg-app'}))

# Phần 2: NACL chỉ cho 443 vào; chiều trả lời tới cổng tạm 50000
nacl_in = [(100, 'ALLOW', 'tcp', 443, 443, '0.0.0.0/0')]
nacl_out_missing = [(100, 'ALLOW', 'tcp', 443, 443, '0.0.0.0/0')]
nacl_out_ok = nacl_out_missing + [(110, 'ALLOW', 'tcp', 1024, 65535, '0.0.0.0/0')]
print('vào 443:', nacl_allows(nacl_in, 'tcp', 443, '198.51.100.7'))
print('trả lời cổng tạm 50000 (thiếu quy tắc):', nacl_allows(nacl_out_missing, 'tcp', 50000, '198.51.100.7'))
print('trả lời cổng tạm 50000 (đã thêm 1024-65535):', nacl_allows(nacl_out_ok, 'tcp', 50000, '198.51.100.7'))
PY
```

**3. Verify:** dự đoán `False`, `True`; `True`, `False`, `True`.

## Phần B — SG và NACL trong sandbox (không phí)
Thay `<...>` bằng giá trị của bạn (không commit chúng). Chạy bằng `bash`/WSL.

```bash
export AWS_REGION=ap-northeast-1
VPC=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query Vpc.VpcId --output text \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Project,Value=net-handbook}]')
SG=$(aws ec2 create-security-group --group-name lab-sg-app --description "lab 06/03" --vpc-id "$VPC" \
  --query GroupId --output text --tag-specifications 'ResourceType=security-group,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 describe-security-groups --group-ids "$SG" --query "SecurityGroups[].{in:IpPermissions,out:IpPermissionsEgress}"
```
Dự đoán: SG mới có `in = []` (không có quy tắc vào) và `out` gồm một quy tắc cho phép mọi lưu lượng ra.

Thêm quy tắc tự tham chiếu và kiểm tra:

```bash
aws ec2 authorize-security-group-ingress --group-id "$SG" --ip-permissions \
  "IpProtocol=tcp,FromPort=8080,ToPort=8080,UserIdGroupPairs=[{GroupId=$SG,Description='lab self reference'}]"
aws ec2 describe-security-groups --group-ids "$SG" --query "SecurityGroups[].IpPermissions"
```

NACL tùy chỉnh (chưa gắn subnet, chỉ để đọc quy tắc mặc định):

```bash
NACL=$(aws ec2 create-network-acl --vpc-id "$VPC" --query NetworkAcl.NetworkAclId --output text \
  --tag-specifications 'ResourceType=network-acl,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 describe-network-acls --network-acl-ids "$NACL" --query "NetworkAcls[].Entries[].[RuleNumber,Egress,RuleAction,CidrBlock]" --output table
```
Dự đoán: NACL tùy chỉnh chỉ có hai quy tắc `*` (số 32767) `deny` cho IPv4, một chiều vào và một chiều ra, tức chặn mọi thứ.

**Break it (đọc, không gắn vào subnet đang dùng):** thêm quy tắc cho phép vào 443 nhưng **không** thêm chiều ra, rồi nêu bằng lời gói trả lời của một kết nối tới cổng tạm sẽ bị gì khi NACL này gắn vào subnet.

## Teardown (bắt buộc) và kiểm tra
```bash
aws ec2 delete-network-acl --network-acl-id "$NACL"
aws ec2 delete-security-group --group-id "$SG"
aws ec2 delete-vpc --vpc-id "$VPC"
```
Kiểm tra (phải trả về rỗng):

```bash
aws ec2 describe-vpcs --filters Name=tag:Project,Values=net-handbook --query "Vpcs[].VpcId" --output text
aws ec2 describe-security-groups --filters Name=tag:Project,Values=net-handbook --query "SecurityGroups[].GroupId" --output text
aws ec2 describe-network-acls --filters Name=tag:Project,Values=net-handbook --query "NetworkAcls[].NetworkAclId" --output text
```

## Ghi kết quả (làm sạch trước khi commit)
Lưu output **đã che** mọi ID và account ID vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
