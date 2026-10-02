# Network Fundamentals Handbook (Infra / DevOps / Cloud)

## Project Specification

Version: 1.0 (đã duyệt 2026-10-02)

> Chuyển thể từ `part-1-vision.md` của repo tham chiếu, viết lại cho mạng máy tính. Các quyết định đã chốt ở Bước 0:
> H1 chapter dạng câu hỏi + slug ngắn; metadata YAML trong mỗi chapter; Mermaid là sơ đồ mặc định; glossary dạng bảng;
> phiên bản blueprint CCNA **chưa chốt** (xem `spec/ccna-coverage-map-process.md`).

---

# PART 1 — Tầm nhìn, mục tiêu và triết lý

---

# 1. Tầm nhìn

Xây dựng một handbook mạng máy tính bằng **tiếng Việt đơn giản**, đủ sâu để người làm Infra/DevOps/Cloud **hiểu bản chất** thay vì học thuộc lệnh, và đủ thực tế để dùng được ngay khi đi làm.

Handbook gồm hai phần ghép lại:

- Phần **CCNA cần cho công việc hạ tầng hiện đại** (IP, subnet, routing, NAT, DHCP, DNS, ICMP, ACL/firewall…).
- Phần **CCNA bỏ sót nhưng DevOps cần**: TCP/TLS/HTTP, load balancing, công cụ debug trên Linux, mạng container, và **AWS networking**.

Handbook không thay thế tài liệu chính thức (RFC, tài liệu AWS, tài liệu Linux) mà là **bản đồ** nối các nguồn đó lại, và luôn chỉ về nguồn gốc để người đọc kiểm tra.

Sau khi hoàn thành, người đọc có thể:

- Theo dõi được một gói tin đi từ máy này sang máy kia qua những chặng nào.
- Đọc và thiết kế được một VPC: CIDR, subnet, route table, gateway, security group.
- Chẩn đoán theo tầng khi "không kết nối được", thay vì đoán mò.
- Nói đúng thuật ngữ (Anh/Nhật) khi làm việc trong dự án thật.

---

# 2. Đối tượng độc giả

Người học chính (dùng làm giả định khi viết):

- Kỹ sư IT người Việt đang chuyển sang DevOps, hướng dài hạn là Solution/Cloud Architect.
- Hands-on hạ tầng còn yếu; **không** giả định đã hiểu sâu AWS dù có chứng chỉ.
- Tiếng Anh trung bình: **không** giả định hiểu thuật ngữ chuyên ngành tiếng Anh.
- Làm việc trên **Windows** (PowerShell/CMD), có thể thêm WSL2.

Nhóm phụ (nội dung phải dùng được, nhưng không viết riêng cho họ):

| Nhóm | Dùng handbook để |
|---|---|
| Người mới vào Infra | Học từ nền, theo thứ tự Phase |
| DevOps/SRE trung cấp | Tra cứu, ôn lại bản chất, troubleshoot |
| Người ôn phỏng vấn | Mục Interview questions và Phase 08 |

---

# 3. Handbook này KHÔNG phải là

- Không phải ngân hàng câu hỏi thi CCNA, cũng không phải tài liệu luyện thi chứng chỉ.
- Không phải cheat sheet lệnh.
- Không phải hướng dẫn cấu hình thiết bị Cisco.

Nó là một handbook theo hướng **hiểu bản chất + production-first** cho kỹ sư hạ tầng trên cloud.

---

# 4. Triết lý

## Nguyên tắc 1 — Packet journey first

Luôn bắt đầu từ câu hỏi "gói tin đi qua những chặng nào", rồi mới xuống chi tiết từng giao thức.

```
Client → DNS → Router → NAT → Load balancer → Server
```

## Nguyên tắc 2 — Hiểu bản chất, không học thuộc

Không hỏi "NAT là gì?" mà hỏi "Nếu không có NAT thì máy trong mạng private ra Internet bằng cách nào, và chuyện gì xảy ra với gói trả về?". Mỗi khái niệm trả lời theo thứ tự: **vì sao tồn tại → giải quyết gì → hoạt động ra sao → cấu hình sai thì sao**.

## Nguyên tắc 3 — Production-first / troubleshoot-first

Không học "Security Group là gì" một cách lý thuyết, mà học:

```
Kết nối bị treo → nghi tầng nào → kiểm tra theo thứ tự → công cụ → nguyên nhân gốc → cách sửa
```

## Nguyên tắc 4 — Thực hành bắt buộc

Mỗi chapter Must có lab theo bốn bước: **Predict → Run → Verify → Break it**. Hiểu thật sự được kiểm tra bằng việc dự đoán đúng kết quả và chẩn đoán được lỗi tự gây ra.

## Nguyên tắc 5 — 20/80

Chỉ dạy phần dùng trong 80% công việc thực tế. Cú pháp tra được trong 30 giây thì không bắt học thuộc.

## Nguyên tắc 6 — Khái niệm tách khỏi AWS

Phase 01–05 trung lập vendor; Phase 06 áp dụng vào AWS và không dạy lại khái niệm. Một số khái niệm cố ý xuất hiện hai lần ở hai góc nhìn: NAT, firewall/ACL, DNS, DHCP, load balancer, routing, VPN.

---

# 5. Sáu câu hỏi mỗi chapter phải trả lời

| Câu hỏi | Nội dung |
|---|---|
| **What?** | Nó là gì (bằng lời đơn giản trước) |
| **Why?** | Vì sao tồn tại; không có nó thì sao |
| **How?** | Gói tin / luồng điều khiển hoạt động ra sao |
| **When?** | Khi nào dùng, khi nào không |
| **What if?** | Cấu hình sai thì sao; thay bằng cách khác thì sao |
| **Troubleshoot?** | Triệu chứng thật, thứ tự kiểm tra, công cụ |

---

# 6. Tiêu chí chất lượng (mức tổng quát)

Một chapter chỉ được coi là hoàn thành khi: giải thích được bản chất; có sơ đồ kèm lời giải thích; có lab chạy thật (với chapter Must); có Break it; có troubleshooting; có câu hỏi phỏng vấn và bài tập có deliverable cụ thể; có cheat sheet; mọi sự thật AWS đã kiểm chứng kèm ngày; không chứa dữ liệu thật. Tiêu chí chi tiết theo Importance nằm ở `spec/part-2-chapter-standard.md`.

---

# 7. Mô hình trình bày

```
Story (sự cố thật) → Mục tiêu → Vì sao tồn tại → Mental model → Cách hoạt động
→ Cấu hình → AWS → Lab → Break it → Troubleshoot → Bảo mật & chi phí → Hiểu nhầm → Ôn tập
```

Người đọc hiểu **tại sao** trước khi biết **là gì**, và luôn thấy hậu quả khi làm sai.

---

# 8. Phạm vi kiến thức

**Trong phạm vi** (chi tiết ở `spec/part-4-roadmap.md`, 59 chapter):

- Lab toolkit: môi trường lab, công cụ mạng Linux, bắt gói tin.
- Nền tảng: mô hình OSI/TCP-IP, Ethernet/ARP, IPv4/IPv6, CIDR, RFC 1918.
- Routing: bảng định tuyến, longest-prefix match, default route, NAT/PAT.
- Dịch vụ lõi: DHCP, DNS, ICMP, NTP, syslog.
- Transport/ứng dụng: TCP, UDP, HTTP, TLS, load balancing, reverse proxy.
- Bảo mật: firewall, ACL, SG vs NACL (khái niệm), VPN, bastion.
- AWS networking: VPC, route table/IGW/NAT Gateway, endpoint, ENI, Route 53, ELB, TGW, VPN/DX, Flow Logs, IaC.
- Linux và container: network namespace, Docker, ECS awsvpc, nhập môn Kubernetes.
- Troubleshooting theo tầng và phỏng vấn.

**Ngoài phạm vi** (trừ khi người dùng yêu cầu): cú pháp Cisco IOS chi tiết, STP/EtherChannel chi tiết, wireless, QoS, cáp vật lý.

---

# 9. Mục tiêu cuối cùng

Sau khi đọc và làm lab, người học nên có khả năng:

- Giải thích bằng lời mình đường đi của một request từ trình duyệt đến database trong kiến trúc `User → ALB → App → DB` trên AWS.
- Thiết kế CIDR và subnet cho nhiều môi trường mà không trùng và không cạn IP.
- Dùng công cụ (ping, traceroute, dig, curl, ss, tcpdump, Flow Logs, Reachability Analyzer) để khoanh vùng nguyên nhân một lỗi kết nối.
- Có nền tảng mạng để tiến tới vai trò DevOps/Cloud Engineer rồi Solution Architect.

---

Đây là **Part 1** của Specification (v1.0).
