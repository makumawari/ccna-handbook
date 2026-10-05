# Glossary

> Mỗi thuật ngữ được định nghĩa **một lần** ở đây; chapter khác chỉ link về. Quy tắc cột: `spec/part-3` §6. Sắp xếp theo alphabet tiếng Anh.

| English | Viết tắt | Tiếng Việt | 日本語 | Giải thích đơn giản | Chapter |
|---|---|---|---|---|---|
| 5-tuple |  | bộ năm | 5タプル | Năm trường xác định một luồng: IP nguồn, IP đích, giao thức, cổng nguồn, cổng đích | [05/01](phase-05-security/01-firewall-stateful-vs-stateless.md) |
| A record |  | bản ghi A | Aレコード | Bản ghi đổi tên thành địa chỉ IPv4 (AAAA: IPv6) | [03/03](phase-03-core-services/03-dns-records-ttl-private-dns.md) |
| ACL (Access Control List) | ACL | danh sách kiểm soát truy cập | アクセスコントロールリスト | Danh sách có thứ tự các quy tắc cho phép/từ chối dùng để lọc lưu lượng | [05/02](phase-05-security/02-acl.md) |
| Address pool | | dải địa chỉ cấp phát | アドレスプール | Khoảng địa chỉ mà DHCP server được phép cho thuê | [03/01](phase-03-core-services/01-dhcp.md) |
| Agent forwarding |  | chuyển tiếp agent | エージェントフォワーディング | Cho máy từ xa dùng khóa trong agent trên máy bạn; có rủi ro nếu quản trị viên máy đó không đáng tin | [05/05](phase-05-security/05-bastion-and-session-access.md) |
| Aggregation interval |  | khoảng gộp | 集計間隔 | Thời gian một luồng được gom thành một bản ghi flow log | [06/11](phase-06-aws-networking/11-flow-logs-reachability-analyzer.md) |
| Alias record |  | bản ghi alias | エイリアスレコード | Bản ghi mở rộng của Route 53 trỏ tới tài nguyên AWS, dùng được ở zone apex | [06/07](phase-06-aws-networking/07-route53.md) |
| Application-layer firewall |  | firewall tầng ứng dụng | アプリケーション層ファイアウォール | Firewall hiểu nội dung giao thức tầng 7, ví dụ tên miền hoặc đường dẫn HTTP | [05/01](phase-05-security/01-firewall-stateful-vs-stateless.md) |
| ARP (Address Resolution Protocol) | ARP | giao thức phân giải địa chỉ | ARP | Cách máy hỏi "IP này là MAC nào?" trong cùng một mạng | [01/03](phase-01-foundation/03-ethernet-mac-arp.md) |
| ARP cache |  | bảng ARP | ARPキャッシュ | Bảng ghi nhớ các cặp IP ↔ MAC đã học | [01/03](phase-01-foundation/03-ethernet-mac-arp.md) |
| ASN (Autonomous System Number) | ASN | số hiệu hệ thống tự trị | AS番号 | Số hiệu dùng trong BGP để nhận diện một hệ thống mạng | [06/10](phase-06-aws-networking/10-site-to-site-vpn-direct-connect.md) |
| Attachment (transit gateway) |  | điểm gắn | アタッチメント | Thứ được nối vào TGW: VPC, VPN, Direct Connect gateway, peering TGW | [06/09](phase-06-aws-networking/09-vpc-peering-transit-gateway.md) |
| Authoritative name server | | máy chủ tên có thẩm quyền | 権威DNSサーバー | Máy chủ giữ bản ghi "chính chủ" của một tên miền và trả lời chắc chắn | [03/02](phase-03-core-services/02-dns-resolution.md) |
| Availability Zone | AZ | vùng khả dụng | アベイラビリティゾーン | Cụm trung tâm dữ liệu độc lập trong một Region; lỗi ở AZ này không nên kéo theo AZ khác | [06/01](phase-06-aws-networking/01-vpc-subnet-az.md) |
| AWS PrivateLink |  | PrivateLink | AWS PrivateLink | Công nghệ truy cập dịch vụ ở VPC khác bằng địa chỉ riêng như thể dịch vụ nằm trong VPC của bạn | [06/04](phase-06-aws-networking/04-vpc-endpoints-gateway-interface-gwlb.md) |
| Bastion host |  | máy trung gian | 踏み台サーバー | Điểm vào duy nhất được bảo vệ để từ đó truy cập các máy trong mạng riêng (còn gọi là jump host) | [05/05](phase-05-security/05-bastion-and-session-access.md) |
| BGP (Border Gateway Protocol) | BGP | giao thức định tuyến biên | BGP | Giao thức định tuyến động, hai bên tự quảng bá route cho nhau | [06/10](phase-06-aws-networking/10-site-to-site-vpn-direct-connect.md) |
| Bind |  | gắn | バインド | Gán một socket vào một địa chỉ IP và cổng cụ thể | [04/04](phase-04-transport-app/04-ports-sockets.md) |
| Bit | | bit | ビット | Đơn vị nhỏ nhất của máy tính, chỉ nhận 0 hoặc 1 | [01/04](phase-01-foundation/04-ipv4-addressing.md) |
| Blackhole route |  | tuyến "hố đen" | ブラックホールルート | Dòng route khiến gói tin tới đích bị loại bỏ thay vì chuyển đi | [02/02](phase-02-routing/02-longest-prefix-match.md) |
| Block size | | kích thước khối | ブロックサイズ | Số địa chỉ trong một mạng con, bằng 2^(32−prefix) | [01/05](phase-01-foundation/05-cidr-subnetting.md) |
| Broadcast address | | địa chỉ quảng bá | ブロードキャストアドレス | Địa chỉ có mọi bit phần máy bằng 1; gửi đến đó là gửi cho mọi máy trong mạng | [01/04](phase-01-foundation/04-ipv4-addressing.md) |
| Buffering |  | đệm | バッファリング | Proxy nhận trọn phản hồi từ backend rồi mới gửi cho client chậm | [04/08](phase-04-transport-app/08-reverse-proxy.md) |
| CA (Certificate Authority) | CA | tổ chức cấp chứng chỉ | 認証局 | Bên đáng tin ký xác nhận chứng chỉ | [04/06](phase-04-transport-app/06-tls-certificates.md) |
| Cache | | bộ nhớ đệm | キャッシュ | Nơi lưu tạm câu trả lời để lần sau dùng lại | [03/02](phase-03-core-services/02-dns-resolution.md) |
| Capture filter |  | bộ lọc lúc bắt | キャプチャフィルタ | Điều kiện quyết định gói nào được ghi lại; gói không khớp bị bỏ ngay | [00/03](phase-00-lab-toolkit/03-packet-capture.md) |
| Certificate |  | chứng chỉ | 証明書 | Tệp ghi tên chủ sở hữu, khóa công khai, thời hạn và chữ ký của bên cấp | [04/06](phase-04-transport-app/06-tls-certificates.md) |
| Certificate chain |  | chuỗi chứng chỉ | 証明書チェーン | Dãy chứng chỉ từ chứng chỉ của server lên qua CA trung gian tới CA gốc | [04/06](phase-04-transport-app/06-tls-certificates.md) |
| Change set |  | bộ thay đổi | 変更セット | Bản xem trước những gì sẽ đổi khi cập nhật stack, chưa áp dụng | [06/12](phase-06-aws-networking/12-network-iac-cloudformation.md) |
| CIDR (Classless Inter-Domain Routing) | CIDR | định tuyến liên miền không phân lớp | CIDR | Cách viết dải địa chỉ bằng địa chỉ cộng độ dài phần mạng, ví dụ `10.0.1.0/24` | [01/05](phase-01-foundation/05-cidr-subnetting.md) |
| Circular dependency |  | phụ thuộc vòng | 循環依存 | A cần B mà B cần A nên không xác định được thứ tự tạo | [06/12](phase-06-aws-networking/12-network-iac-cloudformation.md) |
| Client IP preservation |  | giữ IP client | クライアントIPの保持 | Target thấy địa chỉ nguồn thật của client thay vì của LB | [04/07](phase-04-transport-app/07-load-balancing-l4-vs-l7.md) |
| CNAME record |  | bản ghi bí danh | CNAMEレコード | Nói "tên này là bí danh của tên kia"; resolver hỏi tiếp tên đích | [03/03](phase-03-core-services/03-dns-records-ttl-private-dns.md) |
| Conditional forwarder |  | chuyển tiếp có điều kiện | 条件付きフォワーダー | DNS server chuyển câu hỏi về một miền cho server khác | [06/06](phase-06-aws-networking/06-dhcp-options-and-vpc-dns.md) |
| Congestion control |  | kiểm soát tắc nghẽn | 輻輳制御 | Cơ chế giảm tốc độ gửi khi mạng nghẽn | [04/03](phase-04-transport-app/03-udp.md) |
| Connection state |  | trạng thái kết nối | コネクション状態 | Giai đoạn hiện tại của một kết nối TCP, ví dụ ESTABLISHED | [04/01](phase-04-transport-app/01-tcp-handshake-states.md) |
| Connection tracking |  | theo dõi kết nối | コネクショントラッキング | Cơ chế bộ lọc stateful dùng để nhớ từng kết nối | [05/01](phase-05-security/01-firewall-stateful-vs-stateless.md) |
| Connectionless |  | không kết nối | コネクションレス | Không có bước thiết lập trước khi gửi; hai bên không giữ trạng thái chung | [04/03](phase-04-transport-app/03-udp.md) |
| Container | | vùng chạy riêng | コンテナ | Chương trình chạy tách biệt khỏi phần còn lại của máy, có mạng và hệ thống file riêng | [00/01](phase-00-lab-toolkit/01-lab-environment.md) |
| Container image | | ảnh container | コンテナイメージ | Gói chứa chương trình và môi trường, dùng làm "khuôn" tạo container | [00/01](phase-00-lab-toolkit/01-lab-environment.md) |
| Customer gateway |  | cổng phía khách | カスタマーゲートウェイ | Thiết bị hoặc phần mềm VPN ở phía mạng của bạn | [05/04](phase-05-security/04-vpn-ipsec-site-to-site.md) |
| Customer gateway device |  | thiết bị phía khách | カスタマーゲートウェイデバイス | Thiết bị hoặc phần mềm VPN ở mạng của bạn | [06/10](phase-06-aws-networking/10-site-to-site-vpn-direct-connect.md) |
| Datagram |  | gói tin độc lập | データグラム | Một thông điệp UDP, tự đủ thông tin và không phụ thuộc gói khác | [04/03](phase-04-transport-app/03-udp.md) |
| Default deny |  | từ chối mặc định | デフォルト拒否 | Chính sách chặn mọi thứ chưa được cho phép tường minh | [05/01](phase-05-security/01-firewall-stateful-vs-stateless.md) |
| Default gateway | | cổng mặc định | デフォルトゲートウェイ | Router mà máy gửi mọi gói tin có đích nằm ngoài LAN | [01/01](phase-01-foundation/01-packet-journey.md) |
| Default route | | tuyến mặc định | デフォルトルート | Dòng `0.0.0.0/0` khớp mọi địa chỉ; chỉ dùng khi không có dòng nào cụ thể hơn | [02/01](phase-02-routing/01-routing-table-basics.md) |
| Defense in depth |  | phòng thủ nhiều lớp | 多層防御 | Dùng nhiều lớp bảo vệ độc lập để một lớp sai không làm hở cả hệ thống | [05/03](phase-05-security/03-sg-vs-nacl-concept.md) |
| DependsOn |  | DependsOn | DependsOn | Thuộc tính CloudFormation khai báo thứ tự tạo tường minh giữa hai tài nguyên | [06/12](phase-06-aws-networking/12-network-iac-cloudformation.md) |
| DHCP (Dynamic Host Configuration Protocol) | DHCP | giao thức cấp địa chỉ tự động | DHCP | Cách một server cấp IP và thông số mạng cho máy vừa vào mạng | [03/01](phase-03-core-services/01-dhcp.md) |
| DHCP option set |  | bộ tùy chọn DHCP | DHCPオプションセット | Cấu hình DNS server, domain, NTP mà VPC phát cho máy; không sửa được sau khi tạo | [06/06](phase-06-aws-networking/06-dhcp-options-and-vpc-dns.md) |
| DHCP server | | máy chủ DHCP | DHCPサーバー | Thiết bị giữ danh sách địa chỉ và cấp cho máy xin | [03/01](phase-03-core-services/01-dhcp.md) |
| Direct Connect | DX | đường kết nối riêng | Direct Connect | Cáp riêng từ mạng của bạn tới một địa điểm Direct Connect của AWS, không qua Internet | [06/10](phase-06-aws-networking/10-site-to-site-vpn-direct-connect.md) |
| Display filter |  | bộ lọc lúc xem | 表示フィルタ | Điều kiện chỉ để lọc hiển thị trên dữ liệu đã bắt | [00/03](phase-00-lab-toolkit/03-packet-capture.md) |
| DNS | DNS | hệ thống tên miền | DNS（名前解決） | "Danh bạ" đổi tên như `www.shopnet.example` thành địa chỉ IP | [01/01](phase-01-foundation/01-packet-journey.md) |
| DNS record |  | bản ghi DNS | DNSレコード | Một dòng dữ liệu trong cơ sở dữ liệu DNS, gồm tên, loại, giá trị và TTL | [03/03](phase-03-core-services/03-dns-records-ttl-private-dns.md) |
| DNS TTL | | thời gian lưu của bản ghi DNS | DNSのTTL | Số giây câu trả lời DNS được phép nằm trong cache (khác TTL của gói tin) | [03/02](phase-03-core-services/02-dns-resolution.md) |
| Documentation address range |  | dải địa chỉ dành cho tài liệu | ドキュメント用アドレス範囲 | Dải cố ý không dùng thật, để làm ví dụ mà không trỏ nhầm tới ai | [01/06](phase-01-foundation/06-private-public-ip-rfc1918.md) |
| ECMP (Equal Cost Multipath) | ECMP | định tuyến nhiều đường cùng giá | ECMP | Dùng nhiều đường cùng giá để chia tải; VPN trên TGW hỗ trợ | [06/10](phase-06-aws-networking/10-site-to-site-vpn-direct-connect.md) |
| Egress |  | chiều ra | アウトバウンド | Lưu lượng đi ra khỏi thứ được bảo vệ | [05/01](phase-05-security/01-firewall-stateful-vs-stateless.md) |
| Elastic IP | EIP | IP công khai cố định | Elastic IP | Địa chỉ IPv4 công khai cố định gắn vào tài nguyên của bạn | [06/02](phase-06-aws-networking/02-route-table-igw-nat-gateway.md) |
| Encapsulation |  | đóng gói | カプセル化 | Mỗi tầng bọc dữ liệu của tầng trên bằng header của mình | [01/02](phase-01-foundation/02-osi-vs-tcpip.md) |
| Endpoint policy |  | chính sách endpoint | エンドポイントポリシー | Chính sách IAM gắn vào endpoint, giới hạn ai dùng endpoint để làm gì | [06/04](phase-06-aws-networking/04-vpc-endpoints-gateway-interface-gwlb.md) |
| ENI (Elastic Network Interface) | ENI | card mạng ảo | ENI | Card mạng ảo có IP riêng gắn vào instance hoặc dịch vụ | [06/04](phase-06-aws-networking/04-vpc-endpoints-gateway-interface-gwlb.md) |
| Ephemeral port |  | cổng tạm thời | エフェメラルポート | Cổng ngẫu nhiên client chọn làm cổng nguồn; server trả lời về đúng cổng này | [05/03](phase-05-security/03-sg-vs-nacl-concept.md) |
| ESP (Encapsulating Security Payload) | ESP | giao thức đóng gói bảo mật | ESP | Giao thức của IPsec cung cấp mã hóa, toàn vẹn và xác thực | [05/04](phase-05-security/04-vpn-ipsec-site-to-site.md) |
| Ethernet |  | chuẩn mạng có dây | イーサネット | Chuẩn mạng có dây phổ biến, quy định dạng khung và cách gửi | [01/03](phase-01-foundation/03-ethernet-mac-arp.md) |
| Exponential backoff |  | lùi theo cấp số nhân | 指数バックオフ | Mỗi lần thử lại chờ gấp đôi lần trước | [04/02](phase-04-transport-app/02-tcp-timeouts-retransmission-keepalive.md) |
| Fail open |  | mở khi lỗi hết | フェイルオープン | Nếu mọi target đều unhealthy, LB gửi tới tất cả thay vì từ chối | [06/08](phase-06-aws-networking/08-elb-alb-nlb-gwlb.md) |
| FIN |  | cờ kết thúc | FIN | Thông báo bên gửi không còn dữ liệu để gửi nữa | [04/01](phase-04-transport-app/01-tcp-handshake-states.md) |
| Firewall |  | tường lửa | ファイアウォール | Thiết bị hoặc phần mềm lọc lưu lượng theo quy tắc, cho phép hoặc chặn | [05/01](phase-05-security/01-firewall-stateful-vs-stateless.md) |
| First match |  | khớp đầu tiên | 最初に一致 | Nguyên tắc dùng quy tắc đầu tiên khớp gói rồi ngừng xét | [05/02](phase-05-security/02-acl.md) |
| Flow |  | luồng | フロー | Chuỗi gói tin cùng chung các trường của bộ năm trong một cuộc trao đổi | [05/01](phase-05-security/01-firewall-stateful-vs-stateless.md) |
| Flow log record |  | bản ghi luồng | フローログレコード | Một dòng mô tả một luồng 5-tuple trong một khoảng gộp | [06/11](phase-06-aws-networking/11-flow-logs-reachability-analyzer.md) |
| Forward proxy |  | proxy thuận | フォワードプロキシ | Đứng trước client, đi ra Internet thay client | [04/08](phase-04-transport-app/08-reverse-proxy.md) |
| FQDN | FQDN | tên miền đầy đủ | FQDN | Tên đủ các phần tới gốc, ví dụ `www.shopnet.example` | [03/02](phase-03-core-services/02-dns-resolution.md) |
| Frame |  | khung | フレーム | Đơn vị dữ liệu ở tầng liên kết, bọc bởi header của đường truyền | [01/02](phase-01-foundation/02-osi-vs-tcpip.md) |
| Gateway endpoint |  | endpoint cổng | ゲートウェイエンドポイント | Endpoint dùng route table để tới S3 hoặc DynamoDB, không phí thêm | [06/04](phase-06-aws-networking/04-vpc-endpoints-gateway-interface-gwlb.md) |
| Gateway Load Balancer endpoint | GWLBe | endpoint cho GWLB | ゲートウェイロードバランサーエンドポイント | Endpoint gửi lưu lượng tới đội thiết bị ảo bằng IP riêng, định tuyến bằng route table | [06/04](phase-06-aws-networking/04-vpc-endpoints-gateway-interface-gwlb.md) |
| GENEVE |  | GENEVE | GENEVE | Giao thức đóng gói GWLB dùng trao đổi lưu lượng với thiết bị ảo, cổng 6081 | [06/08](phase-06-aws-networking/08-elb-alb-nlb-gwlb.md) |
| Header |  | phần đầu | ヘッダー | Thông tin điều khiển mỗi tầng thêm vào trước dữ liệu | [01/02](phase-01-foundation/02-osi-vs-tcpip.md) |
| Health check |  | kiểm tra sức khỏe | ヘルスチェック | LB định kỳ thử một target; fail thì ngừng gửi việc tới target đó | [04/07](phase-04-transport-app/07-load-balancing-l4-vs-l7.md) |
| Hop | | chặng | ホップ | Mỗi lần gói tin đi qua một router trên đường đi | [01/01](phase-01-foundation/01-packet-journey.md) |
| Host | | máy chủ vật chủ | ホスト | Máy thật đang chạy mọi thứ khác (ở đây là máy Windows của bạn) | [00/01](phase-00-lab-toolkit/01-lab-environment.md) |
| Host key |  | khóa máy chủ | ホストキー | Khóa công khai của máy chủ SSH để client kiểm tra mình đang nói chuyện đúng máy | [05/05](phase-05-security/05-bastion-and-session-access.md) |
| Hosted zone |  | vùng được lưu trữ | ホストゾーン | Container chứa bản ghi DNS cho một miền trong Route 53 | [06/07](phase-06-aws-networking/07-route53.md) |
| HTTP | HTTP | giao thức web | HTTP | Cách trình duyệt và server nói chuyện với nhau | [00/02](phase-00-lab-toolkit/02-linux-network-tools.md) |
| HTTPS | HTTPS | HTTP trên TLS | HTTPS | HTTP được mã hóa bằng TLS, thường dùng cổng 443 | [04/06](phase-04-transport-app/06-tls-certificates.md) |
| IaC (Infrastructure as Code) | IaC | hạ tầng như mã | Infrastructure as Code | Mô tả hạ tầng bằng tệp để lặp lại, review và quản lý phiên bản | [06/12](phase-06-aws-networking/12-network-iac-cloudformation.md) |
| ICMP (Internet Control Message Protocol) | ICMP | giao thức thông điệp điều khiển Internet | ICMP | Giao thức đi kèm IP, dùng để báo lỗi và kiểm tra liên lạc | [03/04](phase-03-core-services/04-icmp-ping-traceroute.md) |
| Idempotent |  | lặp lại được | 冪等 | Gửi nhiều lần cho kết quả như gửi một lần | [04/05](phase-04-transport-app/05-http.md) |
| Idle timeout |  | hết thời hạn rảnh | アイドルタイムアウト | Thời gian tối đa một thiết bị nhớ kết nối khi không có dữ liệu đi qua | [04/02](phase-04-transport-app/02-tcp-timeouts-retransmission-keepalive.md) |
| IKE (Internet Key Exchange) | IKE | trao đổi khóa Internet | IKE | Giao thức để hai thiết bị VPN xác thực nhau và thương lượng thông số bảo mật | [05/04](phase-05-security/04-vpn-ipsec-site-to-site.md) |
| Implicit deny |  | từ chối ngầm | 暗黙の拒否 | Gói không khớp quy tắc nào bị từ chối | [05/01](phase-05-security/01-firewall-stateful-vs-stateless.md) |
| Ingress |  | chiều vào | インバウンド | Lưu lượng đi vào thứ được bảo vệ | [05/01](phase-05-security/01-firewall-stateful-vs-stateless.md) |
| Interface endpoint |  | endpoint giao diện | インターフェイスエンドポイント | Endpoint là ENI trong subnet của bạn làm điểm vào tới dịch vụ qua PrivateLink; tính phí | [06/04](phase-06-aws-networking/04-vpc-endpoints-gateway-interface-gwlb.md) |
| Internet gateway | IGW | cổng Internet | インターネットゲートウェイ | Cổng cho phép VPC liên lạc hai chiều với Internet qua địa chỉ công khai | [06/02](phase-06-aws-networking/02-route-table-igw-nat-gateway.md) |
| IP address | | địa chỉ IP | IPアドレス | Dãy số dùng làm địa chỉ của một máy trên mạng | [01/01](phase-01-foundation/01-packet-journey.md) |
| IP address plan |  | kế hoạch địa chỉ | IPアドレス計画 | Bảng cấp phát dải địa chỉ cho toàn tổ chức để tránh trùng | [06/13](phase-06-aws-networking/13-cidr-planning-multi-env.md) |
| IPAM (IP Address Manager) | IPAM | quản lý địa chỉ IP | IPAM | Dịch vụ AWS để lập kế hoạch, theo dõi và cấp CIDR cho VPC | [06/13](phase-06-aws-networking/13-cidr-planning-multi-env.md) |
| IPsec |  | bộ giao thức bảo mật tầng IP | IPsec | Mã hóa, xác thực và bảo vệ toàn vẹn cho gói IP | [05/04](phase-05-security/04-vpn-ipsec-site-to-site.md) |
| IPv4 | IPv4 | địa chỉ IP phiên bản 4 | IPv4アドレス | Địa chỉ dài 32 bit, viết thành bốn số cách nhau bằng dấu chấm | [01/04](phase-01-foundation/04-ipv4-addressing.md) |
| Isolated subnet |  | subnet cô lập | 分離サブネット | Subnet không có route nào ra ngoài VPC | [06/01](phase-06-aws-networking/01-vpc-subnet-az.md) |
| Keepalive |  | giữ sống | キープアライブ | Gói thăm dò gửi định kỳ trên kết nối rảnh để kiểm tra đối phương còn đó | [04/02](phase-04-transport-app/02-tcp-timeouts-retransmission-keepalive.md) |
| Lab environment | | môi trường thực hành | ラボ環境 | Nơi chạy lệnh thử mà không ảnh hưởng đến máy hay hệ thống thật | [00/01](phase-00-lab-toolkit/01-lab-environment.md) |
| LAN (Local Area Network) | LAN | mạng cục bộ | ローカルネットワーク | Các máy nối chung một router hoặc switch trong nhà hay văn phòng | [01/01](phase-01-foundation/01-packet-journey.md) |
| Layer |  | tầng | 階層 | Một nhóm chức năng giải một phần của bài toán truyền dữ liệu | [01/02](phase-01-foundation/02-osi-vs-tcpip.md) |
| Layer 4 | L4 | tầng vận chuyển | レイヤー4 | LB quyết định theo giao thức, IP và cổng, không đọc nội dung ứng dụng | [04/07](phase-04-transport-app/07-load-balancing-l4-vs-l7.md) |
| Layer 7 | L7 | tầng ứng dụng | レイヤー7 | LB hiểu giao thức như HTTP và quyết định theo đường dẫn, host, header | [04/07](phase-04-transport-app/07-load-balancing-l4-vs-l7.md) |
| Lease | | thời hạn thuê | リース | Khoảng thời gian một địa chỉ được cấp cho một máy | [03/01](phase-03-core-services/01-dhcp.md) |
| Link-local | | địa chỉ cục bộ tự cấp | リンクローカルアドレス | Địa chỉ máy tự gán trong dải `169.254.0.0/16`, chỉ dùng được với máy cùng đường dây | [01/04](phase-01-foundation/04-ipv4-addressing.md) |
| Listener |  | bộ lắng nghe | リスナー | Chờ kết nối theo giao thức và cổng, áp quy tắc để chuyển tới target group | [06/08](phase-06-aws-networking/08-elb-alb-nlb-gwlb.md) |
| Listening | | đang lắng nghe | リッスン | Dịch vụ đã mở cổng và chờ có người kết nối đến | [00/02](phase-00-lab-toolkit/02-linux-network-tools.md) |
| Load balancer |  | bộ cân bằng tải | ロードバランサー | Nhận kết nối/yêu cầu từ client và chia cho nhiều server phía sau | [04/07](phase-04-transport-app/07-load-balancing-l4-vs-l7.md) |
| Load balancer node |  | nút cân bằng tải | ロードバランサーノード | Thành phần chạy thực tế của LB; mỗi AZ bật có nút với IP trong subnet của bạn | [06/08](phase-06-aws-networking/08-elb-alb-nlb-gwlb.md) |
| Local route |  | route nội bộ | ローカルルート | Route tự có, đưa gói tin đi trong VPC | [06/02](phase-06-aws-networking/02-route-table-igw-nat-gateway.md) |
| Longest prefix match |  | khớp tiền tố dài nhất | 最長一致 | Quy tắc chọn dòng route có độ dài prefix lớn nhất trong những dòng cùng khớp địa chỉ đích | [02/02](phase-02-routing/02-longest-prefix-match.md) |
| Loopback | | vòng lặp nội bộ | ループバック | Địa chỉ (`127.0.0.1`) để máy nói chuyện với chính nó | [01/04](phase-01-foundation/04-ipv4-addressing.md) |
| MAC address | MAC | địa chỉ phần cứng | MACアドレス | Mã định danh của card mạng | [01/03](phase-01-foundation/03-ethernet-mac-arp.md) |
| Main route table |  | bảng route mặc định | メインルートテーブル | Bảng mà subnet dùng nếu chưa được gắn bảng riêng | [06/02](phase-06-aws-networking/02-route-table-igw-nat-gateway.md) |
| Managed prefix list |  | danh sách tiền tố quản lý | マネージドプレフィックスリスト | Tập CIDR có tên mà nhiều quy tắc/route dùng chung | [06/03](phase-06-aws-networking/03-security-group-and-nacl.md) |
| Method |  | phương thức | メソッド | Động từ của yêu cầu HTTP, ví dụ GET để lấy, POST để gửi dữ liệu xử lý | [04/05](phase-04-transport-app/05-http.md) |
| Metric | | số đo chi phí | メトリック | Khi nhiều dòng route cùng khớp, dòng có số nhỏ hơn được ưu tiên | [02/01](phase-02-routing/01-routing-table-basics.md) |
| MTU (Maximum Transmission Unit) | MTU | kích thước gói tối đa | MTU | Gói lớn nhất một đường truyền chuyển được mà không phải chia nhỏ | [03/04](phase-03-core-services/04-icmp-ping-traceroute.md) |
| MX record |  | bản ghi thư | MXレコード | Nơi nhận email cho miền | [03/03](phase-03-core-services/03-dns-records-ttl-private-dns.md) |
| Name resolution | | phân giải tên | 名前解決 | Việc đổi một tên thành địa chỉ IP | [03/02](phase-03-core-services/02-dns-resolution.md) |
| NAT (Network Address Translation) | NAT | dịch địa chỉ mạng | NAT | Đổi địa chỉ IP trên gói tin khi nó đi qua thiết bị ở biên mạng | [02/05](phase-02-routing/05-nat-pat.md) |
| NAT gateway |  | cổng NAT | NATゲートウェイ | Dịch vụ cho instance private kết nối ra ngoài nhưng không nhận kết nối khởi tạo từ ngoài | [06/02](phase-06-aws-networking/02-route-table-igw-nat-gateway.md) |
| NAT table | | bảng NAT | NATテーブル | Danh sách các kết nối đang có, ghi "địa chỉ:cổng bên trong ↔ bên ngoài" | [02/05](phase-02-routing/05-nat-pat.md) |
| NAT traversal | NAT-T | vượt NAT | NAT越え | Đóng gói ESP trong UDP (cổng 4500) để đi qua thiết bị NAT | [05/04](phase-05-security/04-vpn-ipsec-site-to-site.md) |
| Negative caching |  | nhớ đáp án phủ định | ネガティブキャッシュ | Resolver cũng cache câu trả lời "tên này không tồn tại" | [03/03](phase-03-core-services/03-dns-records-ttl-private-dns.md) |
| Network ACL | NACL | danh sách kiểm soát truy cập mạng | ネットワークACL | Bộ lọc stateless của AWS gắn vào subnet, có cả quy tắc cho phép lẫn từ chối | [05/03](phase-05-security/03-sg-vs-nacl-concept.md) |
| Network address | | địa chỉ mạng | ネットワークアドレス | Địa chỉ có mọi bit phần máy bằng 0, dùng để gọi tên cả mạng | [01/04](phase-01-foundation/04-ipv4-addressing.md) |
| Network Address Usage | NAU | mức dùng địa chỉ mạng | ネットワークアドレス使用量 | Chỉ số đo mức dùng địa chỉ (IP, ENI, CIDR trong prefix list) của VPC | [06/13](phase-06-aws-networking/13-cidr-planning-multi-env.md) |
| Network interface | | giao diện mạng | ネットワークインターフェース | "Cửa" một máy dùng để nối vào mạng; mỗi cửa có địa chỉ riêng | [00/02](phase-00-lab-toolkit/02-linux-network-tools.md) |
| Next hop | | chặng kế tiếp | ネクストホップ | Thiết bị mà gói tin được đưa cho ở bước tiếp theo | [02/01](phase-02-routing/01-routing-table-basics.md) |
| NS record |  | bản ghi máy chủ tên | NSレコード | Chỉ ra máy chủ nào có thẩm quyền cho một miền | [03/03](phase-03-core-services/03-dns-records-ttl-private-dns.md) |
| Octet | | octet | オクテット | Nhóm 8 bit; mỗi số trong địa chỉ IPv4 là một octet (0–255) | [01/04](phase-01-foundation/04-ipv4-addressing.md) |
| Off-link |  | nằm ngoài đường dây | 直接接続されていない | Địa chỉ không thuộc mạng máy nối trực tiếp, nên không gửi thẳng tới được | [02/03](phase-02-routing/03-default-route-gateway.md) |
| On-link | | nằm ngay trên đường dây | 直接接続 | Đích ở cùng mạng, gửi thẳng không qua router | [02/01](phase-02-routing/01-routing-table-basics.md) |
| OSI model | OSI | mô hình OSI | OSI参照モデル | Mô hình tham chiếu 7 tầng, dùng làm ngôn ngữ chung khi nói về mạng | [01/02](phase-01-foundation/02-osi-vs-tcpip.md) |
| Overlapping CIDR |  | CIDR chồng lấn | CIDRの重複 | Hai dải có địa chỉ chung nên không nối được bằng peering/VPN | [06/13](phase-06-aws-networking/13-cidr-planning-multi-env.md) |
| Packet | | gói tin | パケット | Một mẩu dữ liệu kèm địa chỉ người gửi và người nhận để gửi qua mạng | [01/01](phase-01-foundation/01-packet-journey.md) |
| Packet capture |  | bắt gói tin | パケットキャプチャ | Ghi lại bản sao các gói tin đi qua một giao diện mạng để phân tích | [00/03](phase-00-lab-toolkit/03-packet-capture.md) |
| Packet filtering |  | lọc gói tin | パケットフィルタリング | Quyết định từng gói dựa trên các trường như địa chỉ, giao thức, cổng | [05/01](phase-05-security/01-firewall-stateful-vs-stateless.md) |
| Packet loss |  | mất gói | パケットロス | Tỷ lệ gói gửi đi mà không nhận được trả lời | [03/04](phase-03-core-services/04-icmp-ping-traceroute.md) |
| PAT | PAT | dịch cổng và địa chỉ | PAT | Dạng NAT đổi cả địa chỉ lẫn cổng, để nhiều máy dùng chung một địa chỉ công khai (còn gọi là NAPT) | [02/05](phase-02-routing/05-nat-pat.md) |
| Path MTU Discovery | PMTUD | dò MTU của cả đường đi | パスMTUディスカバリ | Cách máy tìm MTU nhỏ nhất trên đường tới đích nhờ thông điệp ICMP | [03/04](phase-03-core-services/04-icmp-ping-traceroute.md) |
| pcap file |  | tệp bắt gói tin | pcapファイル | Tệp lưu các gói tin đã bắt; không commit vào repo vì có thể chứa dữ liệu nhạy cảm | [00/03](phase-00-lab-toolkit/03-packet-capture.md) |
| Persistent connection |  | kết nối bền | 持続的接続 | Một kết nối TCP được dùng cho nhiều cặp yêu cầu/phản hồi | [04/05](phase-04-transport-app/05-http.md) |
| Ping |  | lệnh thử liên lạc | ping | Gửi ICMP echo tới một đích và chờ echo trả lời | [03/04](phase-03-core-services/04-icmp-ping-traceroute.md) |
| Port | | cổng | ポート | Con số đánh dấu một dịch vụ trên máy; IP chọn máy, cổng chọn dịch vụ | [00/02](phase-00-lab-toolkit/02-linux-network-tools.md) |
| Port forwarding |  | chuyển tiếp cổng | ポートフォワーディング | Dùng đường SSH để đưa một cổng của máy từ xa về một cổng trên máy mình | [05/05](phase-05-security/05-bastion-and-session-access.md) |
| Prefix length | | độ dài tiền tố | プレフィックス長 | Số bit đầu thuộc phần mạng, số sau dấu `/` | [01/05](phase-01-foundation/05-cidr-subnetting.md) |
| Primary private IPv4 |  | IP riêng chính | プライマリプライベートIPv4 | IP riêng đầu tiên của ENI, lấy từ dải subnet; không chuyển sang ENI khác | [06/05](phase-06-aws-networking/05-eni-and-ip-allocation.md) |
| Private DNS |  | DNS nội bộ | プライベートDNS | Vùng DNS chỉ trả lời cho máy trong một mạng nhất định, không công khai | [03/03](phase-03-core-services/03-dns-records-ttl-private-dns.md) |
| Private DNS (endpoint) |  | DNS riêng cho endpoint | プライベートDNS | Tên công khai của dịch vụ phân giải thành IP riêng của endpoint trong VPC | [06/04](phase-06-aws-networking/04-vpc-endpoints-gateway-interface-gwlb.md) |
| Private hosted zone | PHZ | zone riêng | プライベートホストゾーン | Zone có bản ghi định tuyến lưu lượng trong các VPC được gắn | [06/07](phase-06-aws-networking/07-route53.md) |
| Private IP address | | địa chỉ IP riêng | プライベートIPアドレス | Địa chỉ thuộc dải dành cho mạng nội bộ; Internet không định tuyến dải này | [01/06](phase-01-foundation/06-private-public-ip-rfc1918.md) |
| Private key |  | khóa riêng | 秘密鍵 | Nửa bí mật của cặp khóa; chỉ chủ sở hữu giữ, dùng để chứng minh mình là chủ; không bao giờ commit | [04/06](phase-04-transport-app/06-tls-certificates.md) |
| Private subnet |  | subnet riêng | プライベートサブネット | Subnet không có route trực tiếp tới Internet gateway | [06/01](phase-06-aws-networking/01-vpc-subnet-az.md) |
| Protocol |  | giao thức | プロトコル | Bộ quy tắc hai bên cùng tuân theo để nói chuyện | [01/02](phase-01-foundation/02-osi-vs-tcpip.md) |
| Proxy protocol |  | giao thức proxy | プロキシプロトコル | Cách LB gửi kèm thông tin client gốc ở đầu kết nối tới target | [04/07](phase-04-transport-app/07-load-balancing-l4-vs-l7.md) |
| PTR record |  | bản ghi tra ngược | PTRレコード | Đổi địa chỉ IP thành tên | [03/03](phase-03-core-services/03-dns-records-ttl-private-dns.md) |
| Public hosted zone |  | zone công khai | パブリックホストゾーン | Zone có bản ghi định tuyến lưu lượng từ Internet | [06/07](phase-06-aws-networking/07-route53.md) |
| Public IP address | | địa chỉ IP công khai | グローバルIPアドレス | Địa chỉ duy nhất toàn Internet, ai cũng gửi gói tới được | [01/06](phase-01-foundation/06-private-public-ip-rfc1918.md) |
| Public key |  | khóa công khai | 公開鍵 | Nửa công khai của cặp khóa; nằm trong chứng chỉ, ai cũng biết | [04/06](phase-04-transport-app/06-tls-certificates.md) |
| Public subnet |  | subnet công khai | パブリックサブネット | Subnet có route trực tiếp tới Internet gateway | [06/01](phase-06-aws-networking/01-vpc-subnet-az.md) |
| Reachability Analyzer |  | công cụ phân tích khả năng liên lạc | Reachability Analyzer | Công cụ phân tích cấu hình mạng tĩnh, không gửi gói, chỉ ra thành phần chặn | [06/11](phase-06-aws-networking/11-flow-logs-reachability-analyzer.md) |
| Recursive resolver | | bộ phân giải đệ quy | 再帰リゾルバー | Máy chủ DNS nhận câu hỏi của máy bạn rồi tự hỏi các máy chủ khác cho tới khi có đáp án | [03/02](phase-03-core-services/02-dns-resolution.md) |
| Region |  | khu vực | リージョン | Nhóm trung tâm dữ liệu ở một vùng địa lý, ví dụ Tokyo | [06/01](phase-06-aws-networking/01-vpc-subnet-az.md) |
| Request |  | yêu cầu | リクエスト | Một chiều của lần trao đổi HTTP: phía gửi nêu phương thức và đích | [04/05](phase-04-transport-app/05-http.md) |
| Requester-managed ENI |  | ENI do dịch vụ quản lý | リクエスタ管理ENI | ENI do dịch vụ AWS tạo thay bạn; bạn xem được nhưng không sửa | [06/05](phase-06-aws-networking/05-eni-and-ip-allocation.md) |
| Reservation | | đặt trước | 予約 | Luôn cấp cùng một địa chỉ cho một MAC address nhất định | [03/01](phase-03-core-services/01-dhcp.md) |
| Resolver | | bộ phân giải | リゾルバー | Phần mềm/máy chủ nhận câu hỏi "tên này là IP nào" rồi đi tìm đáp án | [03/02](phase-03-core-services/02-dns-resolution.md) |
| Resolver endpoint |  | endpoint của Resolver | Resolverエンドポイント | Điểm vào (inbound) hoặc ra (outbound) của VPC Resolver cho DNS lai giữa VPC và mạng khác | [06/07](phase-06-aws-networking/07-route53.md) |
| Response |  | phản hồi | レスポンス | Chiều trả lời của HTTP: mã trạng thái kèm nội dung | [04/05](phase-04-transport-app/05-http.md) |
| Retransmission |  | gửi lại | 再送 | Gửi lần nữa đoạn dữ liệu chưa được xác nhận | [04/02](phase-04-transport-app/02-tcp-timeouts-retransmission-keepalive.md) |
| Reverse proxy |  | proxy ngược | リバースプロキシ | Đứng trước server, nhận yêu cầu thay server rồi chuyển tiếp | [04/08](phase-04-transport-app/08-reverse-proxy.md) |
| RFC 1918 |  | dải địa chỉ riêng theo RFC 1918 | RFC 1918 | Tài liệu chuẩn định nghĩa ba dải địa chỉ private | [01/06](phase-01-foundation/06-private-public-ip-rfc1918.md) |
| Root server | | máy chủ gốc | ルートサーバー | Tầng trên cùng của cây DNS; chỉ đường xuống tầng dưới | [03/02](phase-03-core-services/02-dns-resolution.md) |
| Route | | tuyến | 経路 | Một dòng trong bảng định tuyến | [02/01](phase-02-routing/01-routing-table-basics.md) |
| Route 53 Resolver |  | bộ phân giải Route 53 | Route 53 Resolver | Bộ phân giải DNS có sẵn trong mỗi VPC (Amazon DNS, VPC+2) | [06/06](phase-06-aws-networking/06-dhcp-options-and-vpc-dns.md) |
| Route aggregation |  | gộp tuyến | 経路集約 | Dùng một dòng prefix ngắn thay cho nhiều dòng prefix dài nằm trong nó | [02/02](phase-02-routing/02-longest-prefix-match.md) |
| Route table |  | bảng định tuyến | ルートテーブル | Danh sách 'đích nào thì gửi qua đường nào' gắn với subnet | [06/02](phase-06-aws-networking/02-route-table-igw-nat-gateway.md) |
| Router | | bộ định tuyến | ルーター | Thiết bị nhận gói tin rồi chuyển đến chặng kế tiếp theo địa chỉ đích | [01/01](phase-01-foundation/01-packet-journey.md) |
| Routing | | định tuyến | ルーティング | Quá trình chọn đường cho gói tin | [02/01](phase-02-routing/01-routing-table-basics.md) |
| Routing policy |  | chính sách định tuyến | ルーティングポリシー | Cách Route 53 chọn đáp án cho một truy vấn (simple, weighted, failover, latency...) | [06/07](phase-06-aws-networking/07-route53.md) |
| Routing table | | bảng định tuyến | ルーティングテーブル | Danh sách "đích nào thì gửi qua đường nào" mà mỗi thiết bị giữ | [02/01](phase-02-routing/01-routing-table-basics.md) |
| RST |  | cờ đặt lại | RST | Ngắt kết nối ngay lập tức, thường vì lỗi hoặc vì không có dịch vụ ở cổng đó | [04/01](phase-04-transport-app/01-tcp-handshake-states.md) |
| RTO (Retransmission Timeout) | RTO | thời gian chờ gửi lại | 再送タイムアウト | Thời gian chờ ACK trước khi gửi lại; tăng gấp đôi sau mỗi lần thất bại | [04/02](phase-04-transport-app/02-tcp-timeouts-retransmission-keepalive.md) |
| RTT (Round-Trip Time) | RTT | thời gian khứ hồi | 往復遅延時間 | Thời gian từ lúc gửi tới lúc nhận trả lời | [03/04](phase-03-core-services/04-icmp-ping-traceroute.md) |
| Rule |  | quy tắc | ルール | Một dòng trong ACL, gồm điều kiện khớp và hành động | [05/02](phase-05-security/02-acl.md) |
| Rule number |  | số thứ tự quy tắc | ルール番号 | Số quyết định vị trí quy tắc trong danh sách ở hệ thống đánh số, ví dụ network ACL của AWS | [05/02](phase-05-security/02-acl.md) |
| Rule shadowing |  | che khuất quy tắc | ルールのシャドーイング | Quy tắc không bao giờ được dùng vì quy tắc đứng trước đã khớp mọi gói nó định xử lý | [05/02](phase-05-security/02-acl.md) |
| SAN (Subject Alternative Name) | SAN | tên thay thế của chủ thể | サブジェクト代替名 | Danh sách tên miền mà chứng chỉ có hiệu lực; client so tên truy cập với danh sách này | [04/06](phase-04-transport-app/06-tls-certificates.md) |
| Scheme |  | kiểu | スキーム | Internet-facing (IP công khai) hoặc internal (chỉ IP riêng) của load balancer | [06/08](phase-06-aws-networking/08-elb-alb-nlb-gwlb.md) |
| Secondary CIDR |  | CIDR phụ | セカンダリCIDR | Khối CIDR thêm vào VPC sau khi tạo; có hạn chế theo họ dải | [06/13](phase-06-aws-networking/13-cidr-planning-multi-env.md) |
| Secondary private IPv4 |  | IP riêng phụ | セカンダリプライベートIPv4 | IP riêng thêm vào ENI, có thể chuyển sang ENI khác | [06/05](phase-06-aws-networking/05-eni-and-ip-allocation.md) |
| Security Association | SA | liên kết bảo mật | セキュリティアソシエーション | Một kết nối một chiều có thông số mã hóa và khóa; hai chiều cần một cặp SA | [05/04](phase-05-security/04-vpn-ipsec-site-to-site.md) |
| Security group | SG | nhóm bảo mật | セキュリティグループ | Bộ lọc stateful của AWS gắn vào network interface/tài nguyên, chỉ có quy tắc cho phép | [05/03](phase-05-security/03-sg-vs-nacl-concept.md) |
| Security group referencing |  | tham chiếu nhóm bảo mật | セキュリティグループの参照 | Dùng ID của một security group làm nguồn/đích trong quy tắc thay vì dải IP | [06/03](phase-06-aws-networking/03-security-group-and-nacl.md) |
| Segment |  | đoạn | セグメント | Đơn vị dữ liệu ở tầng vận chuyển, bọc bởi header TCP | [01/02](phase-01-foundation/02-osi-vs-tcpip.md) |
| Self-signed certificate |  | chứng chỉ tự ký | 自己署名証明書 | Chứng chỉ do chính chủ ký, không có CA đáng tin xác nhận | [04/06](phase-04-transport-app/06-tls-certificates.md) |
| Sequence number |  | số thứ tự | シーケンス番号 | Số đánh dấu từng byte dữ liệu để bên nhận sắp xếp và xác nhận | [04/01](phase-04-transport-app/01-tcp-handshake-states.md) |
| Session-based access |  | truy cập theo phiên | セッションベースのアクセス | Kết nối quản trị qua dịch vụ trung gian đã xác thực danh tính, không cần mở cổng đến ở máy đích | [05/05](phase-05-security/05-bastion-and-session-access.md) |
| Shared address space | CGNAT | không gian địa chỉ dùng chung | 共有アドレス空間 | Dải `100.64.0.0/10` nhà mạng dùng cho CGNAT; không phải private cũng không phải public | [01/06](phase-01-foundation/06-private-public-ip-rfc1918.md) |
| SNI (Server Name Indication) | SNI | chỉ dẫn tên máy chủ | SNI | Client nêu tên miền muốn truy cập ngay trong ClientHello để server chọn đúng chứng chỉ | [04/06](phase-04-transport-app/06-tls-certificates.md) |
| SOA record |  | bản ghi khởi đầu vùng | SOAレコード | Thông tin quản trị của một zone, gồm giá trị quyết định thời gian nhớ đáp án phủ định | [03/03](phase-03-core-services/03-dns-records-ttl-private-dns.md) |
| Socket |  | ổ cắm mạng | ソケット | Điểm đầu cuối chương trình dùng để gửi/nhận dữ liệu, gồm giao thức, địa chỉ IP và cổng | [04/04](phase-04-transport-app/04-ports-sockets.md) |
| Source-destination check |  | kiểm tra nguồn-đích | 送信元/送信先チェック | ENI chỉ nhận gói mà instance là nguồn hoặc đích; phải tắt cho NAT/firewall | [06/05](phase-06-aws-networking/05-eni-and-ip-allocation.md) |
| Split-horizon DNS |  | DNS chân trời kép | スプリットホライズンDNS | Cùng một tên miền nhưng câu trả lời khác nhau tùy máy hỏi ở trong hay ngoài mạng | [03/03](phase-03-core-services/03-dns-records-ttl-private-dns.md) |
| SSH (Secure Shell) | SSH | Secure Shell | SSH | Giao thức đăng nhập và truyền dữ liệu từ xa qua kênh mã hóa | [05/05](phase-05-security/05-bastion-and-session-access.md) |
| Stack |  | ngăn xếp | スタック | Tập tài nguyên được tạo, sửa, xóa cùng nhau từ một template | [06/12](phase-06-aws-networking/12-network-iac-cloudformation.md) |
| State table |  | bảng trạng thái | ステートテーブル | Bảng firewall dùng để nhớ các kết nối đang được theo dõi (còn gọi là conntrack) | [05/01](phase-05-security/01-firewall-stateful-vs-stateless.md) |
| Stateful |  | có trạng thái | ステートフル | Bộ lọc nhớ các kết nối đang diễn ra nên tự cho phép gói trả lời của kết nối đã được phép | [05/01](phase-05-security/01-firewall-stateful-vs-stateless.md) |
| Stateless |  | không lưu trạng thái | ステートレス | Mỗi yêu cầu tự đủ thông tin, server không dựa vào yêu cầu trước | [05/01](phase-05-security/01-firewall-stateful-vs-stateless.md) |
| Status code |  | mã trạng thái | ステータスコード | Số ba chữ số trong phản hồi HTTP nói kết quả, ví dụ 200, 404, 502 | [04/05](phase-04-transport-app/05-http.md) |
| Sticky session |  | phiên dính | スティッキーセッション | Luôn gửi cùng một client tới cùng một target | [04/07](phase-04-transport-app/07-load-balancing-l4-vs-l7.md) |
| Subnet | | mạng con | サブネット | Một phần của mạng lớn, chia ra để quản lý và cô lập | [01/05](phase-01-foundation/05-cidr-subnetting.md) |
| Subnet mask | | mặt nạ mạng | サブネットマスク | Dãy 32 bit cho biết bao nhiêu bit đầu của địa chỉ thuộc phần mạng | [01/04](phase-01-foundation/04-ipv4-addressing.md) |
| Subnetting | | chia mạng con | サブネット化 | Việc cắt một mạng thành nhiều mạng con | [01/05](phase-01-foundation/05-cidr-subnetting.md) |
| Switch |  | bộ chuyển mạch | スイッチ | Thiết bị nối các máy trong cùng mạng, chuyển khung theo MAC | [01/03](phase-01-foundation/03-ethernet-mac-arp.md) |
| SYN |  | cờ đồng bộ | SYN | Gói mở đầu, đề nghị bắt đầu kết nối và nêu số thứ tự khởi đầu | [04/01](phase-04-transport-app/01-tcp-handshake-states.md) |
| Target |  | đích | ターゲット | Server nhận việc từ load balancer | [04/07](phase-04-transport-app/07-load-balancing-l4-vs-l7.md) |
| Target group |  | nhóm đích | ターゲットグループ | Tập target nhận việc từ LB cùng cấu hình health check | [06/08](phase-06-aws-networking/08-elb-alb-nlb-gwlb.md) |
| TCP (Transmission Control Protocol) | TCP | giao thức điều khiển truyền tải | TCP | Giao thức tầng vận chuyển cung cấp luồng dữ liệu tin cậy, đúng thứ tự giữa hai máy | [04/01](phase-04-transport-app/01-tcp-handshake-states.md) |
| TCP/IP model |  | mô hình TCP/IP | TCP/IPモデル | Mô hình 4 tầng mô tả cách Internet thực sự vận hành | [01/02](phase-01-foundation/02-osi-vs-tcpip.md) |
| tcpdump |  | công cụ bắt gói dòng lệnh | tcpdump | Công cụ dòng lệnh để bắt và hiển thị gói tin trên Linux | [00/03](phase-00-lab-toolkit/03-packet-capture.md) |
| Template |  | mẫu | テンプレート | Tệp YAML/JSON mô tả tài nguyên của một stack CloudFormation | [06/12](phase-06-aws-networking/12-network-iac-cloudformation.md) |
| Three-way handshake |  | bắt tay ba bước | 3ウェイハンドシェイク | Ba gói SYN, SYN-ACK, ACK để mở một kết nối TCP | [04/01](phase-04-transport-app/01-tcp-handshake-states.md) |
| TLS (Transport Layer Security) | TLS | bảo mật tầng vận chuyển | TLS | Giao thức thêm mã hóa, xác thực và toàn vẹn lên trên một kết nối TCP | [04/06](phase-04-transport-app/06-tls-certificates.md) |
| TLS termination |  | kết thúc TLS | TLS終端 | Thiết bị, thường là load balancer, giải mã TLS ở đó | [04/06](phase-04-transport-app/06-tls-certificates.md) |
| Traceroute |  | lệnh dò đường | traceroute | Liệt kê các router trên đường tới đích bằng gói có TTL tăng dần (Windows: `tracert`) | [03/04](phase-03-core-services/04-icmp-ping-traceroute.md) |
| Transit gateway | TGW | cổng trung chuyển | トランジットゲートウェイ | Hub định tuyến cấp Region nối nhiều VPC và mạng on-premise | [06/09](phase-06-aws-networking/09-vpc-peering-transit-gateway.md) |
| Transitive routing |  | định tuyến bắc cầu | 推移的ルーティング | A đi tới C qua B; peering không hỗ trợ | [06/09](phase-06-aws-networking/09-vpc-peering-transit-gateway.md) |
| Trust store |  | kho tin cậy | トラストストア | Danh sách CA gốc mà hệ điều hành hoặc trình duyệt tin sẵn | [04/06](phase-04-transport-app/06-tls-certificates.md) |
| TTL (Time To Live) | TTL | thời gian sống | 生存時間 | Số chặng tối đa còn lại của gói tin; mỗi router trừ 1, về 0 thì gói bị bỏ | [01/01](phase-01-foundation/01-packet-journey.md) |
| Tunnel |  | đường hầm | トンネル | Gói gốc được đóng gói bên trong một gói khác để đi qua mạng trung gian | [05/04](phase-05-security/04-vpn-ipsec-site-to-site.md) |
| TXT record |  | bản ghi văn bản | TXTレコード | Chuỗi chữ tùy ý, thường dùng để xác minh quyền sở hữu hoặc cấu hình xác thực email | [03/03](phase-03-core-services/03-dns-records-ttl-private-dns.md) |
| Upstream |  | phía trên dòng | アップストリーム | Server hoặc nhóm server phía sau mà proxy chuyển tiếp tới | [04/08](phase-04-transport-app/08-reverse-proxy.md) |
| Virtual interface | VIF | giao diện ảo | 仮想インターフェイス | Kênh logic trên Direct Connect: private, public hoặc transit | [06/10](phase-06-aws-networking/10-site-to-site-vpn-direct-connect.md) |
| Virtual private gateway | VGW | cổng riêng ảo | 仮想プライベートゲートウェイ | Điểm cuối VPN phía AWS, gắn vào một VPC | [05/04](phase-05-security/04-vpn-ipsec-site-to-site.md) |
| VPC (Virtual Private Cloud) | VPC | mạng riêng ảo | VPC | Mạng tách biệt logic trên AWS, thuộc một Region, bạn tự chọn dải CIDR | [06/01](phase-06-aws-networking/01-vpc-subnet-az.md) |
| VPC endpoint |  | điểm cuối VPC | VPCエンドポイント | Đường riêng từ VPC tới một dịch vụ, không qua Internet gateway hay NAT | [06/04](phase-06-aws-networking/04-vpc-endpoints-gateway-interface-gwlb.md) |
| VPC Flow Logs |  | nhật ký luồng VPC | VPCフローログ | Bản ghi lưu lượng IP đi tới/đi khỏi network interface trong VPC | [06/11](phase-06-aws-networking/11-flow-logs-reachability-analyzer.md) |
| VPC peering connection |  | kết nối peering | VPCピアリング接続 | Liên kết riêng một-một giữa hai VPC để định tuyến bằng địa chỉ riêng; không bắc cầu | [06/09](phase-06-aws-networking/09-vpc-peering-transit-gateway.md) |
| VPN (Virtual Private Network) | VPN | mạng riêng ảo | VPN | Kết nối được mã hóa nối hai mạng riêng qua một mạng công cộng như Internet | [05/04](phase-05-security/04-vpn-ipsec-site-to-site.md) |
| Wireshark |  | công cụ phân tích gói đồ họa | Wireshark | Công cụ có giao diện đồ họa để mở và phân tích gói tin | [00/03](phase-00-lab-toolkit/03-packet-capture.md) |
| WSL2 | WSL2 | WSL phiên bản 2 | WSL2 | Cách chạy Linux ngay trong Windows | [00/01](phase-00-lab-toolkit/01-lab-environment.md) |
| X-Forwarded-For | XFF | X-Forwarded-For | X-Forwarded-For | Tiêu đề HTTP chứa IP client gốc; mỗi proxy thêm vào cuối | [04/07](phase-04-transport-app/07-load-balancing-l4-vs-l7.md) |
| Zone |  | vùng | ゾーン | Phần của cây DNS mà một bên quản lý và giữ bản ghi | [03/03](phase-03-core-services/03-dns-records-ttl-private-dns.md) |
| Zone apex |  | đỉnh miền | ゾーンエイペックス | Chính tên miền gốc, ví dụ shopnet.example; không dùng CNAME ở đây | [06/07](phase-06-aws-networking/07-route53.md) |
