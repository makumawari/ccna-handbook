# Lab 06/11 — Flow Logs và Reachability Analyzer

Chapter: [06/11-flow-logs-reachability-analyzer](../../../book/phase-06-aws-networking/11-flow-logs-reachability-analyzer.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- **Phần A hoàn toàn local**, dùng dữ liệu giả (IP RFC 5737, ENI ID giả).
- **Phần B** dùng **Reachability Analyzer, TÍNH PHÍ THEO MỖI LẦN PHÂN TÍCH**: kiểm tra giá hiện hành (Amazon VPC Pricing, mục Network Analysis) và chỉ chạy số lần tối thiểu (2 lần). Không tạo Flow Logs thật trong lab này (cần IAM role, log group và tính phí lưu trữ).
- Chỉ chạy trên **tài khoản sandbox riêng**, Region `ap-northeast-1`, tag `Project=net-handbook`, sau khi đặt budget alert.
- **Không** in/commit access key, token, `~/.aws/credentials`. Lệnh xóa chỉ chạy khi bạn chủ động đồng ý.
- `[CHƯA KIỂM CHỨNG]`: Reachability Analyzer có phân tích được giữa hai ENI chưa gắn instance hay không; nếu lệnh báo lỗi, ghi lại thông báo và dừng phần B (không tạo instance để "sửa" lỗi vì sẽ phát sinh chi phí).

## Phần A — Phân loại log mẫu (local)
**1. Predict:** trong tệp mẫu, luồng nào là cặp ACCEPT/REJECT nghi NACL? Luồng nào nghi SG?

**2. Run:**

```bash
python3 - <<'PY'
sample = """
2 ACCOUNT-ID eni-aaaa1111 203.0.113.12 10.0.1.20 49152 443 6 20 4249 1750000000 1750000060 ACCEPT OK
2 ACCOUNT-ID eni-aaaa1111 10.0.1.20 203.0.113.12 443 49152 6 18 3900 1750000000 1750000060 REJECT OK
2 ACCOUNT-ID eni-aaaa1111 198.51.100.7 10.0.1.20 40000 3389 6 3 180 1750000100 1750000160 REJECT OK
2 ACCOUNT-ID eni-aaaa1111 10.0.1.20 192.0.2.50 51000 8080 6 12 2500 1750000200 1750000260 ACCEPT OK
2 ACCOUNT-ID eni-aaaa1111 192.0.2.50 10.0.1.20 8080 51000 6 10 2400 1750000200 1750000260 ACCEPT OK
2 ACCOUNT-ID eni-aaaa1111 - - - - - - - 1750000300 1750000360 - NODATA
"""
fields = "version account interface src dst srcport dstport proto packets bytes start end action status".split()
rows = [dict(zip(fields, l.split())) for l in sample.strip().splitlines()]
flows = {}
for r in rows:
    if r['status'] != 'OK':
        print('bỏ qua:', r['status'])
        continue
    key = frozenset(((r['src'], r['srcport']), (r['dst'], r['dstport'])))
    flows.setdefault(key, []).append(r)
for key, rs in flows.items():
    actions = [r['action'] for r in rs]
    if actions == ['ACCEPT', 'REJECT']:
        verdict = 'ACCEPT vào + REJECT ra -> nghi NACL thiếu chiều trả lời'
    elif actions == ['REJECT']:
        verdict = 'chỉ REJECT -> nghi SG hoặc NACL chiều vào'
    elif all(a == 'ACCEPT' for a in actions):
        verdict = 'bình thường (ACCEPT cả hai chiều)'
    else:
        verdict = 'cần xem thêm'
    r0 = rs[0]
    print(f"{r0['src']}:{r0['srcport']} <-> {r0['dst']}:{r0['dstport']}: {actions} => {verdict}")
PY
```

**3. Verify:** dự đoán: luồng `203.0.113.12 <-> 10.0.1.20:443` là cặp ACCEPT+REJECT (nghi NACL); luồng `198.51.100.7 -> :3389` chỉ REJECT (nghi SG); luồng `8080` bình thường; dòng `NODATA` bị bỏ qua.

## Phần B — Reachability Analyzer giữa hai ENI (TÍNH PHÍ theo lần, tùy chọn)
Thay `<...>` bằng giá trị của bạn (không commit chúng). Chạy bằng `bash`/WSL.

```bash
export AWS_REGION=ap-northeast-1
VPC=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query Vpc.VpcId --output text \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Project,Value=net-handbook}]')
SN=$(aws ec2 create-subnet --vpc-id "$VPC" --cidr-block 10.0.10.0/24 --availability-zone ap-northeast-1a \
  --query Subnet.SubnetId --output text --tag-specifications 'ResourceType=subnet,Tags=[{Key=Project,Value=net-handbook}]')
SG=$(aws ec2 create-security-group --group-name lab-ra-sg --description "lab 06/11" --vpc-id "$VPC" \
  --query GroupId --output text --tag-specifications 'ResourceType=security-group,Tags=[{Key=Project,Value=net-handbook}]')
ENI_A=$(aws ec2 create-network-interface --subnet-id "$SN" --groups "$SG" --description "lab ra a" \
  --query NetworkInterface.NetworkInterfaceId --output text \
  --tag-specifications 'ResourceType=network-interface,Tags=[{Key=Project,Value=net-handbook}]')
ENI_B=$(aws ec2 create-network-interface --subnet-id "$SN" --groups "$SG" --description "lab ra b" \
  --query NetworkInterface.NetworkInterfaceId --output text \
  --tag-specifications 'ResourceType=network-interface,Tags=[{Key=Project,Value=net-handbook}]')
PATH_ID=$(aws ec2 create-network-insights-path --source "$ENI_A" --destination "$ENI_B" \
  --protocol tcp --destination-port 8080 --query NetworkInsightsPath.NetworkInsightsPathId --output text \
  --tag-specifications 'ResourceType=network-insights-path,Tags=[{Key=Project,Value=net-handbook}]')
AN1=$(aws ec2 start-network-insights-analysis --network-insights-path-id "$PATH_ID" \
  --query NetworkInsightsAnalysis.NetworkInsightsAnalysisId --output text)
sleep 30
aws ec2 describe-network-insights-analyses --network-insights-analysis-ids "$AN1" \
  --query "NetworkInsightsAnalyses[].{status:Status,reachable:NetworkPathFound,explain:Explanations[].ExplanationCode}"
```
Dự đoán: SG không có quy tắc vào nên `reachable = false` và có mã giải thích liên quan SG (ghi lại mã thực tế).

**Break it / Fix:** thêm quy tắc tự tham chiếu rồi phân tích lại (lần phân tích thứ hai, tính phí):

```bash
aws ec2 authorize-security-group-ingress --group-id "$SG" --ip-permissions \
  "IpProtocol=tcp,FromPort=8080,ToPort=8080,UserIdGroupPairs=[{GroupId=$SG,Description='lab self ref'}]"
AN2=$(aws ec2 start-network-insights-analysis --network-insights-path-id "$PATH_ID" \
  --query NetworkInsightsAnalysis.NetworkInsightsAnalysisId --output text)
sleep 30
aws ec2 describe-network-insights-analyses --network-insights-analysis-ids "$AN2" \
  --query "NetworkInsightsAnalyses[].{status:Status,reachable:NetworkPathFound}"
```
Dự đoán: `reachable = true` sau khi thêm quy tắc (nếu công cụ phân tích được ENI chưa gắn instance; ghi lại kết quả thật và so với dự đoán).

## Teardown (bắt buộc) và kiểm tra
```bash
aws ec2 delete-network-insights-analysis --network-insights-analysis-id "$AN1"
aws ec2 delete-network-insights-analysis --network-insights-analysis-id "$AN2"
aws ec2 delete-network-insights-path --network-insights-path-id "$PATH_ID"
aws ec2 delete-network-interface --network-interface-id "$ENI_A"
aws ec2 delete-network-interface --network-interface-id "$ENI_B"
aws ec2 delete-security-group --group-id "$SG"
aws ec2 delete-subnet --subnet-id "$SN"
aws ec2 delete-vpc --vpc-id "$VPC"
```
Kiểm tra (phải trả về rỗng):

```bash
aws ec2 describe-network-insights-paths --filters Name=tag:Project,Values=net-handbook --query "NetworkInsightsPaths[].NetworkInsightsPathId" --output text
aws ec2 describe-network-interfaces --filters Name=tag:Project,Values=net-handbook --query "NetworkInterfaces[].NetworkInterfaceId" --output text
aws ec2 describe-vpcs --filters Name=tag:Project,Values=net-handbook --query "Vpcs[].VpcId" --output text
```

## Ghi kết quả (làm sạch trước khi commit)
Lưu output **đã che** mọi ID và account ID vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
