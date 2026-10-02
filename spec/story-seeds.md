# Story seeds — ý tưởng cho mục 1 (Story) và mục 10 (Break it)

> Bài học chung, đã tách khỏi dự án thật. Mọi tên và số liệu khi viết chapter phải dùng dữ liệu giả (`shopnet`, dải IP RFC 5737 / RFC 1918).
> **Tất cả nhãn hiện là `[CHƯA KIỂM CHỨNG]`** cho tới khi có `<!-- verified: YYYY-MM-DD <url> -->` (docs AWS) hoặc kết quả lab do người học chạy (`[lab]` = cần chứng minh bằng lab).

| # | Bài học | Chapter đích | Cách kiểm chứng |
|---|---|---|---|
| 1 | Interface endpoint tạo ENI có IP trong subnet; IP tự cấp có thể trùng IP định gán cho server → tạo ENI giữ chỗ trước, endpoint tạo sau | 06/04, 06/05, 06/12 | lab |
| 2 | Hai Interface endpoint cùng dịch vụ trong cùng VPC không thể cùng bật Private DNS → dùng chung một endpoint cho nhiều subnet | 06/04 | lab |
| 3 | Subnet cho ALB: cần đủ IP trống để scale (kiểm số tối thiểu và kích thước khuyến nghị trong docs); thiếu thì ALB suy giảm, có thể 5xx/timeout | 06/08, 06/13 | docs |
| 4 | Hai ENI cùng một Security Group **không** tự nói chuyện với nhau; cần rule tham chiếu chính SG đó | 05/03, 06/03 | lab |
| 5 | SG stateful vs NACL stateless: quên ephemeral port ở chiều trả → kết nối treo dù SG đúng | 05/03, 06/03 | lab |
| 6 | S3 Gateway endpoint: gắn route table, không dùng được từ on-premise/peering khác Region/TGW; Interface endpoint dùng được | 06/04 | docs |
| 7 | Dải `172.32.x.x` **không** thuộc private RFC 1918 (`172.16`–`172.31`) → rủi ro xung đột khi nối mạng khác | 01/06, 06/13 | RFC 1918 |
| 8 | Private subnet không NAT: Fleet Manager/SSM cần đủ endpoint (ssm, ssmmessages, ec2messages) + SG cho phép 443 + Private DNS bật | 06/04, 08/02 | lab |
| 9 | CloudFormation tự dựng dependency graph từ `!Ref`/`!GetAtt`; `DependsOn` cho ràng buộc không biểu diễn được bằng tham chiếu | 06/12 | lab |
| 10 | SG tham chiếu lẫn nhau gây circular dependency → tách rule thành resource Ingress/Egress riêng | 06/12 | lab |
| 11 | Trộn rule inline và rule resource riêng trên cùng SG có thể xung đột khi update → xem change set | 06/12 | lab |
| 12 | Main route table lỡ có route ra IGW → subnet mới quên gắn route table sẽ vô tình thành public | 06/02 | lab |
| 13 | Interface endpoint tính phí theo giờ **mỗi AZ** và theo GB; chọn Gateway khi đủ dùng | 06/04, 12 | docs (không ghi số tiền) |
| 14 | Flow Logs: chiều vào ACCEPT mà chiều ra REJECT → nghi NACL (stateless) | 06/11, 08/01 | lab |
