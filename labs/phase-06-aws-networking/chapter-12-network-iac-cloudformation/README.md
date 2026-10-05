# Lab 06/12 — Mạng bằng CloudFormation: đồ thị phụ thuộc, vòng và change set

Chapter: [06/12-network-iac-cloudformation](../../../book/phase-06-aws-networking/12-network-iac-cloudformation.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`. Template `cfn/network.yaml` chưa được kiểm tra bằng `validate-template`; đó là bước đầu của Phần B.

## An toàn và chi phí
- **Phần A hoàn toàn local.**
- **Phần B** chỉ chạy `validate-template` và tạo **change set kiểu CREATE** (stack ở `REVIEW_IN_PROGRESS`, **chưa tạo tài nguyên**): không tính phí tài nguyên. **Không chạy `execute-change-set`.**
- **Phần C (tùy chọn) tạo tài nguyên thật**: chỉ khi bạn chủ động đồng ý; với `EnableNat=false` (mặc định) các tài nguyên (VPC, subnet, IGW, route table, SG) không tính phí riêng. **`EnableNat=true` tạo hai NAT gateway + hai Elastic IP: TÍNH PHÍ THEO GIỜ và theo GB; không bật trong lab này** trừ khi đã kiểm tra giá hiện hành.
- Chỉ chạy trên **tài khoản sandbox riêng**, Region `ap-northeast-1`, tag `Project=net-handbook`, sau khi đặt budget alert.
- **Không** in/commit access key, token, `~/.aws/credentials`. `delete-stack` là lệnh phá hủy: chỉ chạy khi bạn chủ động đồng ý đúng lệnh đó.

## Phần A — Đồ thị phụ thuộc và phát hiện vòng (local)
**1. Predict:** `PublicRoute` được tạo sau những tài nguyên nào? Thêm hai quy tắc SG inline tham chiếu nhau thì xảy ra gì?

**2. Run:** chạy từ thư mục `labs/phase-06-aws-networking/chapter-12-network-iac-cloudformation`.

```bash
python3 - <<'PY'
import re, sys

text = open('cfn/network.yaml', encoding='utf-8').read()
body = text.split('\nResources:\n', 1)[1].split('\nOutputs:', 1)[0]
params = {'Env', 'VpcCidr', 'EnableNat'}

deps, current = {}, None
for line in body.splitlines():
    m = re.match(r'^  ([A-Za-z0-9]+):\s*$', line)
    if m:
        current = m.group(1)
        deps[current] = set()
        continue
    if current is None:
        continue
    for pat in (r'!Ref ([A-Za-z0-9]+)', r'!GetAtt ([A-Za-z0-9]+)\.', r'DependsOn: ([A-Za-z0-9]+)'):
        for d in re.findall(pat, line):
            if d not in params and d != current:
                deps[current].add(d)

def topo(deps):
    order, state = [], {}
    def visit(n, stack):
        if state.get(n) == 'done':
            return
        if state.get(n) == 'visiting':
            raise ValueError('VÒNG PHỤ THUỘC: ' + ' -> '.join(stack + [n]))
        state[n] = 'visiting'
        for d in sorted(deps.get(n, ())):
            visit(d, stack + [n])
        state[n] = 'done'
        order.append(n)
    for n in sorted(deps):
        visit(n, [])
    return order

print('Thứ tự tạo (phụ thuộc trước):')
for n in topo(deps):
    print(' ', n, '<-', sorted(deps[n]))

print()
print('Phụ thuộc của PublicRoute:', sorted(deps['PublicRoute']))

# Mô phỏng vòng: hai SG inline tham chiếu nhau
bad = {k: set(v) for k, v in deps.items()}
bad['SgAlb'].add('SgApp')
bad['SgApp'].add('SgAlb')
try:
    topo(bad)
except ValueError as e:
    print(e)
PY
```

**3. Verify:** dự đoán: `PublicRoute <- ['Igw', 'IgwAttachment', 'PublicRouteTable']` (`DependsOn` cộng `!Ref`); danh sách thứ tự có `Vpc` và `Igw` trước mọi thứ phụ thuộc chúng; phần mô phỏng báo `VÒNG PHỤ THUỘC: SgAlb -> SgApp -> SgAlb`.

## Phần B — validate-template và change set (không tạo tài nguyên)
```bash
export AWS_REGION=ap-northeast-1
aws cloudformation validate-template --template-body file://cfn/network.yaml --query "Parameters[].ParameterKey"
aws cloudformation create-change-set \
  --stack-name shopnet-lab0612 --change-set-name cs-create \
  --change-set-type CREATE --template-body file://cfn/network.yaml \
  --parameters ParameterKey=Env,ParameterValue=stg ParameterKey=VpcCidr,ParameterValue=10.0.0.0/16 ParameterKey=EnableNat,ParameterValue=false \
  --tags Key=Project,Value=net-handbook
sleep 15
aws cloudformation describe-change-set --stack-name shopnet-lab0612 --change-set-name cs-create \
  --query "{status:Status,changes:Changes[].ResourceChange.[Action,LogicalResourceId,ResourceType]}" --output json
aws cloudformation describe-stacks --stack-name shopnet-lab0612 --query "Stacks[].StackStatus"
```
Dự đoán: `validate-template` liệt kê ba tham số (`Env`, `VpcCidr`, `EnableNat`); change set `CREATE_COMPLETE` với hành động `Add` cho VPC, subnet, IGW, route table, route, SG (và **không** có `AWS::EC2::NatGateway` vì `EnableNat=false`); trạng thái stack `REVIEW_IN_PROGRESS`.

**Break it — đọc thông báo lỗi:** sửa bản sao `network.yaml` để `SgApp` có `SecurityGroupIngress` inline tham chiếu `!Ref SgAlb` và `SgAlb` có inline tham chiếu `!Ref SgApp`, rồi tạo change set mới (`--change-set-name cs-circular`). Dự đoán: lỗi **circular dependency**. Ghi lại thông báo chính xác. Không sửa file gốc.

## Phần C — Thực thi và cập nhật có Replacement (TÙY CHỌN, tạo tài nguyên thật)
Chỉ chạy khi bạn chủ động đồng ý và đã đặt budget alert. Giữ `EnableNat=false`.

```bash
aws cloudformation execute-change-set --stack-name shopnet-lab0612 --change-set-name cs-create
aws cloudformation wait stack-create-complete --stack-name shopnet-lab0612
aws cloudformation describe-stacks --stack-name shopnet-lab0612 --query "Stacks[].{status:StackStatus,outputs:Outputs}"
# Cập nhật: đổi VpcCidr -> xem change set (CHƯA execute), chú ý cột Replacement
aws cloudformation create-change-set --stack-name shopnet-lab0612 --change-set-name cs-update \
  --use-previous-template \
  --parameters ParameterKey=Env,UsePreviousValue=true ParameterKey=VpcCidr,ParameterValue=10.20.0.0/16 ParameterKey=EnableNat,UsePreviousValue=true
sleep 15
aws cloudformation describe-change-set --stack-name shopnet-lab0612 --change-set-name cs-update \
  --query "Changes[].ResourceChange.{action:Action,id:LogicalResourceId,replace:Replacement}" --output table
```
Dự đoán: đổi `VpcCidr` gây `Replacement` cho `Vpc` và kéo theo thay thế/cập nhật các tài nguyên phụ thuộc (subnet, route table, SG...). **Không thực thi `cs-update`**; xóa change set này.

## Teardown (bắt buộc) và kiểm tra
Chỉ chạy khi bạn đồng ý xóa đúng stack của lab. Nếu chỉ làm Phần A/B:

```bash
aws cloudformation delete-change-set --stack-name shopnet-lab0612 --change-set-name cs-create
aws cloudformation delete-change-set --stack-name shopnet-lab0612 --change-set-name cs-circular 2>/dev/null
aws cloudformation delete-stack --stack-name shopnet-lab0612
```
Nếu đã làm Phần C: xóa `cs-update` rồi `delete-stack` như trên (CloudFormation xóa tài nguyên theo thứ tự ngược của phụ thuộc). Kiểm tra đã xóa hết:

```bash
aws cloudformation describe-stacks --stack-name shopnet-lab0612 --query "Stacks[].StackStatus" 2>&1 | head -3
aws ec2 describe-vpcs --filters Name=tag:Project,Values=net-handbook --query "Vpcs[].VpcId" --output text
aws ec2 describe-nat-gateways --filter Name=tag:Project,Values=net-handbook Name=state,Values=available,pending --query "NatGateways[].NatGatewayId" --output text
aws ec2 describe-addresses --filters Name=tag:Project,Values=net-handbook --query "Addresses[].AllocationId" --output text
```
Dự đoán: `describe-stacks` báo stack không còn tồn tại; ba lệnh còn lại trả về rỗng.

## Ghi kết quả (làm sạch trước khi commit)
Lưu output **đã che** mọi ID và account ID vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
