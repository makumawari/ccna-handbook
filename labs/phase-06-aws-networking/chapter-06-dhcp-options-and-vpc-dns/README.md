# Lab 06/06 — DHCP option set và DNS của VPC (lab rút gọn)

Chapter: [06/06-dhcp-options-and-vpc-dns](../../../book/phase-06-aws-networking/06-dhcp-options-and-vpc-dns.md) · Importance: Should

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Lab chỉ đọc cấu hình và tạo VPC trống, DHCP option set: **không tính phí**. Chạy trên **tài khoản sandbox riêng**, Region `ap-northeast-1`, tag `Project=net-handbook`, sau khi đặt budget alert.
- **Không gắn option set tùy chỉnh vào VPC đang dùng thật** (ảnh hưởng DNS mọi instance); chỉ thao tác trên VPC lab trống.
- **Không** in/commit access key, token, `~/.aws/credentials`. Lệnh xóa chỉ chạy khi bạn chủ động đồng ý.

## Phần A — Thuộc tính DNS của VPC
**1. Predict:** VPC mới tạo bằng CLI có `enableDnsSupport` và `enableDnsHostnames` bằng gì?

**2. Run:** (thay `<...>` bằng giá trị của bạn, không commit)

```bash
export AWS_REGION=ap-northeast-1
VPC=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query Vpc.VpcId --output text \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Project,Value=net-handbook}]')
aws ec2 describe-vpc-attribute --vpc-id "$VPC" --attribute enableDnsSupport --query EnableDnsSupport.Value
aws ec2 describe-vpc-attribute --vpc-id "$VPC" --attribute enableDnsHostnames --query EnableDnsHostnames.Value
aws ec2 modify-vpc-attribute --vpc-id "$VPC" --enable-dns-hostnames '{"Value":true}'
aws ec2 describe-vpc-attribute --vpc-id "$VPC" --attribute enableDnsHostnames --query EnableDnsHostnames.Value
```

**3. Verify:** dự đoán `true` cho `enableDnsSupport`, `false` cho `enableDnsHostnames` (VPC không mặc định), rồi `true` sau khi bật.

## Phần B — DHCP option set không sửa được
```bash
DHCP=$(aws ec2 create-dhcp-options --dhcp-configurations \
  "Key=domain-name,Values=lab.example.com" "Key=domain-name-servers,Values=AmazonProvidedDNS" \
  --tag-specifications 'ResourceType=dhcp-options,Tags=[{Key=Project,Value=net-handbook}]' \
  --query DhcpOptions.DhcpOptionsId --output text)
aws ec2 describe-dhcp-options --dhcp-options-ids "$DHCP" --query "DhcpOptions[].DhcpConfigurations"
aws ec2 associate-dhcp-options --dhcp-options-id "$DHCP" --vpc-id "$VPC"
aws ec2 describe-vpcs --vpc-ids "$VPC" --query "Vpcs[].DhcpOptionsId"
```
Dự đoán: option set có hai cấu hình; sau khi gắn, VPC báo đúng `DhcpOptionsId`. CLI không có lệnh "sửa" option set: muốn đổi phải `create-dhcp-options` mới rồi `associate-dhcp-options` lại. (Domain `lab.example.com` là tên tài liệu, không phải domain thật.)

**Break it (khái niệm, không thao tác trên VPC dùng thật):** nêu bằng lời điều gì xảy ra nếu bạn đặt `domain-name-servers` chỉ là một DNS riêng không biết miền AWS, và cần cấu hình gì để sửa.

## Teardown (bắt buộc) và kiểm tra
```bash
aws ec2 delete-vpc --vpc-id "$VPC"
aws ec2 delete-dhcp-options --dhcp-options-id "$DHCP"
```
(Xóa VPC trước để option set không còn được dùng; nếu lệnh xóa option set báo đang dùng, kiểm tra association.) Kiểm tra (phải trả về rỗng):

```bash
aws ec2 describe-vpcs --filters Name=tag:Project,Values=net-handbook --query "Vpcs[].VpcId" --output text
aws ec2 describe-dhcp-options --filters Name=tag:Project,Values=net-handbook --query "DhcpOptions[].DhcpOptionsId" --output text
```

## Ghi kết quả (làm sạch trước khi commit)
Lưu output **đã che** mọi ID và account ID vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
