# Lab 06/07 — Route 53 private hosted zone và NXDOMAIN

Chapter: [06/07-route53](../../../book/phase-06-aws-networking/07-route53.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- **Phần A local.**
- **Phần B tạo một private hosted zone: Route 53 tính phí theo tháng cho mỗi hosted zone.** Kiểm tra bảng giá hiện hành trước khi chạy và **xóa zone ngay sau lab**. Không tạo public hosted zone, health check hay Resolver endpoint trong lab này.
- Chỉ chạy trên **tài khoản sandbox riêng**, Region `ap-northeast-1`, tag `Project=net-handbook`, sau khi đặt budget alert.
- Tên miền dùng là `lab.shopnet.example` (miền tài liệu, không phải domain thật). **Không dùng domain thật của bạn hay của công ty.**
- **Không** in/commit access key, token, `~/.aws/credentials`. Lệnh xóa chỉ chạy khi bạn chủ động đồng ý.

## Phần A — Mô phỏng khớp tên PHZ (local)
**1. Predict:** PHZ `lab.shopnet.example` chỉ có `db`. Truy vấn `db.lab.shopnet.example`, `www.lab.shopnet.example`, `example.org` cho kết quả gì?

**2. Run:**

```bash
python3 - <<'PY'
zones = {'lab.shopnet.example': {('db.lab.shopnet.example', 'A'): '10.0.10.4'}}

def resolve(name, rtype='A'):
    matches = [z for z in zones if name == z or name.endswith('.' + z)]
    if not matches:
        return 'chuyển lên DNS công khai (không có PHZ khớp)'
    zone = max(matches, key=len)          # PHZ cụ thể nhất
    rec = zones[zone].get((name, rtype))
    return rec if rec else 'NXDOMAIN (có PHZ khớp nhưng thiếu bản ghi, KHÔNG quay lại DNS công khai)'

for n in ('db.lab.shopnet.example', 'www.lab.shopnet.example', 'example.org'):
    print(n, '->', resolve(n))
PY
```

**3. Verify:** dự đoán `db → 10.0.10.4`; `www → NXDOMAIN`; `example.org → chuyển lên DNS công khai`.

## Phần B — Private hosted zone gắn VPC (CÓ PHÍ nhỏ, xóa ngay)
Thay `<...>` bằng giá trị của bạn (không commit chúng). Chạy bằng `bash`/WSL.

```bash
export AWS_REGION=ap-northeast-1
VPC=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query Vpc.VpcId --output text \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 modify-vpc-attribute --vpc-id "$VPC" --enable-dns-support '{"Value":true}'
aws ec2 modify-vpc-attribute --vpc-id "$VPC" --enable-dns-hostnames '{"Value":true}'
ZONE=$(aws route53 create-hosted-zone --name lab.shopnet.example \
  --caller-reference "lab0607-$(date +%s)" \
  --vpc VPCRegion=ap-northeast-1,VPCId="$VPC" \
  --hosted-zone-config Comment="lab 06/07 net-handbook",PrivateZone=true \
  --query HostedZone.Id --output text)
aws route53 change-resource-record-sets --hosted-zone-id "$ZONE" --change-batch '{
  "Changes":[{"Action":"CREATE","ResourceRecordSet":{"Name":"db.lab.shopnet.example","Type":"A","TTL":60,
  "ResourceRecords":[{"Value":"10.0.10.4"}]}}]}'
aws route53 list-resource-record-sets --hosted-zone-id "$ZONE" \
  --query "ResourceRecordSets[].{name:Name,type:Type,ttl:TTL}" --output table
```
Dự đoán: zone có bản ghi NS, SOA (tự tạo) và `db` kiểu `A` TTL 60. Không có instance trong VPC nên không dùng `dig` trong lab này; việc kiểm tra NXDOMAIN từ trong VPC cần một instance (ngoài phạm vi lab, có thể tính phí).

**Break it (đọc):** liệt kê lại bản ghi và xác nhận **không có** `www`; nêu bằng lời một instance trong VPC hỏi `www.lab.shopnet.example` sẽ nhận gì và vì sao.

## Teardown (bắt buộc) và kiểm tra
Phải xóa bản ghi do bạn tạo trước (NS và SOA mặc định do dịch vụ quản lý), rồi xóa zone, rồi VPC:

```bash
aws route53 change-resource-record-sets --hosted-zone-id "$ZONE" --change-batch '{
  "Changes":[{"Action":"DELETE","ResourceRecordSet":{"Name":"db.lab.shopnet.example","Type":"A","TTL":60,
  "ResourceRecords":[{"Value":"10.0.10.4"}]}}]}'
aws route53 delete-hosted-zone --id "$ZONE"
aws ec2 delete-vpc --vpc-id "$VPC"
```
Kiểm tra (phải trả về rỗng):

```bash
aws route53 list-hosted-zones --query "HostedZones[?Name=='lab.shopnet.example.'].Id" --output text
aws ec2 describe-vpcs --filters Name=tag:Project,Values=net-handbook --query "Vpcs[].VpcId" --output text
```

## Ghi kết quả (làm sạch trước khi commit)
Lưu output **đã che** zone ID, VPC ID và account ID vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
