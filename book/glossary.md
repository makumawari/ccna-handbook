# Glossary

> Mỗi thuật ngữ được định nghĩa **một lần** ở đây; chapter khác chỉ link về. Quy tắc cột: `spec/part-3` §6. Sắp xếp theo alphabet tiếng Anh.

| English | Viết tắt | Tiếng Việt | 日本語 | Giải thích đơn giản | Chapter |
|---|---|---|---|---|---|
| Address pool | | dải địa chỉ cấp phát | アドレスプール | Khoảng địa chỉ mà DHCP server được phép cho thuê | [03/01](phase-03-core-services/01-dhcp.md) |
| ARP (Address Resolution Protocol) | ARP | giao thức phân giải địa chỉ | ARP | Cách máy hỏi "IP này là MAC nào?" trong cùng một mạng | [01/03](phase-01-foundation/03-ethernet-mac-arp.md) |
| ARP cache |  | bảng ARP | ARPキャッシュ | Bảng ghi nhớ các cặp IP ↔ MAC đã học | [01/03](phase-01-foundation/03-ethernet-mac-arp.md) |
| Authoritative name server | | máy chủ tên có thẩm quyền | 権威DNSサーバー | Máy chủ giữ bản ghi "chính chủ" của một tên miền và trả lời chắc chắn | [03/02](phase-03-core-services/02-dns-resolution.md) |
| Bit | | bit | ビット | Đơn vị nhỏ nhất của máy tính, chỉ nhận 0 hoặc 1 | [01/04](phase-01-foundation/04-ipv4-addressing.md) |
| Block size | | kích thước khối | ブロックサイズ | Số địa chỉ trong một mạng con, bằng 2^(32−prefix) | [01/05](phase-01-foundation/05-cidr-subnetting.md) |
| Broadcast address | | địa chỉ quảng bá | ブロードキャストアドレス | Địa chỉ có mọi bit phần máy bằng 1; gửi đến đó là gửi cho mọi máy trong mạng | [01/04](phase-01-foundation/04-ipv4-addressing.md) |
| Cache | | bộ nhớ đệm | キャッシュ | Nơi lưu tạm câu trả lời để lần sau dùng lại | [03/02](phase-03-core-services/02-dns-resolution.md) |
| CIDR (Classless Inter-Domain Routing) | CIDR | định tuyến liên miền không phân lớp | CIDR | Cách viết dải địa chỉ bằng địa chỉ cộng độ dài phần mạng, ví dụ `10.0.1.0/24` | [01/05](phase-01-foundation/05-cidr-subnetting.md) |
| Container | | vùng chạy riêng | コンテナ | Chương trình chạy tách biệt khỏi phần còn lại của máy, có mạng và hệ thống file riêng | [00/01](phase-00-lab-toolkit/01-lab-environment.md) |
| Container image | | ảnh container | コンテナイメージ | Gói chứa chương trình và môi trường, dùng làm "khuôn" tạo container | [00/01](phase-00-lab-toolkit/01-lab-environment.md) |
| Default gateway | | cổng mặc định | デフォルトゲートウェイ | Router mà máy gửi mọi gói tin có đích nằm ngoài LAN | [01/01](phase-01-foundation/01-packet-journey.md) |
| Default route | | tuyến mặc định | デフォルトルート | Dòng `0.0.0.0/0` khớp mọi địa chỉ; chỉ dùng khi không có dòng nào cụ thể hơn | [02/01](phase-02-routing/01-routing-table-basics.md) |
| DHCP (Dynamic Host Configuration Protocol) | DHCP | giao thức cấp địa chỉ tự động | DHCP | Cách một server cấp IP và thông số mạng cho máy vừa vào mạng | [03/01](phase-03-core-services/01-dhcp.md) |
| DHCP server | | máy chủ DHCP | DHCPサーバー | Thiết bị giữ danh sách địa chỉ và cấp cho máy xin | [03/01](phase-03-core-services/01-dhcp.md) |
| DNS | DNS | hệ thống tên miền | DNS（名前解決） | "Danh bạ" đổi tên như `www.shopnet.example` thành địa chỉ IP | [01/01](phase-01-foundation/01-packet-journey.md) |
| DNS TTL | | thời gian lưu của bản ghi DNS | DNSのTTL | Số giây câu trả lời DNS được phép nằm trong cache (khác TTL của gói tin) | [03/02](phase-03-core-services/02-dns-resolution.md) |
| Documentation address range |  | dải địa chỉ dành cho tài liệu | ドキュメント用アドレス範囲 | Dải cố ý không dùng thật, để làm ví dụ mà không trỏ nhầm tới ai | [01/06](phase-01-foundation/06-private-public-ip-rfc1918.md) |
| Encapsulation |  | đóng gói | カプセル化 | Mỗi tầng bọc dữ liệu của tầng trên bằng header của mình | [01/02](phase-01-foundation/02-osi-vs-tcpip.md) |
| Ethernet |  | chuẩn mạng có dây | イーサネット | Chuẩn mạng có dây phổ biến, quy định dạng khung và cách gửi | [01/03](phase-01-foundation/03-ethernet-mac-arp.md) |
| FQDN | FQDN | tên miền đầy đủ | FQDN | Tên đủ các phần tới gốc, ví dụ `www.shopnet.example` | [03/02](phase-03-core-services/02-dns-resolution.md) |
| Frame |  | khung | フレーム | Đơn vị dữ liệu ở tầng liên kết, bọc bởi header của đường truyền | [01/02](phase-01-foundation/02-osi-vs-tcpip.md) |
| Header |  | phần đầu | ヘッダー | Thông tin điều khiển mỗi tầng thêm vào trước dữ liệu | [01/02](phase-01-foundation/02-osi-vs-tcpip.md) |
| Hop | | chặng | ホップ | Mỗi lần gói tin đi qua một router trên đường đi | [01/01](phase-01-foundation/01-packet-journey.md) |
| Host | | máy chủ vật chủ | ホスト | Máy thật đang chạy mọi thứ khác (ở đây là máy Windows của bạn) | [00/01](phase-00-lab-toolkit/01-lab-environment.md) |
| HTTP | HTTP | giao thức web | HTTP | Cách trình duyệt và server nói chuyện với nhau | [00/02](phase-00-lab-toolkit/02-linux-network-tools.md) |
| IP address | | địa chỉ IP | IPアドレス | Dãy số dùng làm địa chỉ của một máy trên mạng | [01/01](phase-01-foundation/01-packet-journey.md) |
| IPv4 | IPv4 | địa chỉ IP phiên bản 4 | IPv4アドレス | Địa chỉ dài 32 bit, viết thành bốn số cách nhau bằng dấu chấm | [01/04](phase-01-foundation/04-ipv4-addressing.md) |
| Lab environment | | môi trường thực hành | ラボ環境 | Nơi chạy lệnh thử mà không ảnh hưởng đến máy hay hệ thống thật | [00/01](phase-00-lab-toolkit/01-lab-environment.md) |
| LAN (Local Area Network) | LAN | mạng cục bộ | ローカルネットワーク | Các máy nối chung một router hoặc switch trong nhà hay văn phòng | [01/01](phase-01-foundation/01-packet-journey.md) |
| Layer |  | tầng | 階層 | Một nhóm chức năng giải một phần của bài toán truyền dữ liệu | [01/02](phase-01-foundation/02-osi-vs-tcpip.md) |
| Lease | | thời hạn thuê | リース | Khoảng thời gian một địa chỉ được cấp cho một máy | [03/01](phase-03-core-services/01-dhcp.md) |
| Link-local | | địa chỉ cục bộ tự cấp | リンクローカルアドレス | Địa chỉ máy tự gán trong dải `169.254.0.0/16`, chỉ dùng được với máy cùng đường dây | [01/04](phase-01-foundation/04-ipv4-addressing.md) |
| Listening | | đang lắng nghe | リッスン | Dịch vụ đã mở cổng và chờ có người kết nối đến | [00/02](phase-00-lab-toolkit/02-linux-network-tools.md) |
| Loopback | | vòng lặp nội bộ | ループバック | Địa chỉ (`127.0.0.1`) để máy nói chuyện với chính nó | [01/04](phase-01-foundation/04-ipv4-addressing.md) |
| MAC address | MAC | địa chỉ phần cứng | MACアドレス | Mã định danh của card mạng | [01/03](phase-01-foundation/03-ethernet-mac-arp.md) |
| Metric | | số đo chi phí | メトリック | Khi nhiều dòng route cùng khớp, dòng có số nhỏ hơn được ưu tiên | [02/01](phase-02-routing/01-routing-table-basics.md) |
| Name resolution | | phân giải tên | 名前解決 | Việc đổi một tên thành địa chỉ IP | [03/02](phase-03-core-services/02-dns-resolution.md) |
| NAT (Network Address Translation) | NAT | dịch địa chỉ mạng | NAT | Đổi địa chỉ IP trên gói tin khi nó đi qua thiết bị ở biên mạng | [02/05](phase-02-routing/05-nat-pat.md) |
| NAT table | | bảng NAT | NATテーブル | Danh sách các kết nối đang có, ghi "địa chỉ:cổng bên trong ↔ bên ngoài" | [02/05](phase-02-routing/05-nat-pat.md) |
| Network address | | địa chỉ mạng | ネットワークアドレス | Địa chỉ có mọi bit phần máy bằng 0, dùng để gọi tên cả mạng | [01/04](phase-01-foundation/04-ipv4-addressing.md) |
| Network interface | | giao diện mạng | ネットワークインターフェース | "Cửa" một máy dùng để nối vào mạng; mỗi cửa có địa chỉ riêng | [00/02](phase-00-lab-toolkit/02-linux-network-tools.md) |
| Next hop | | chặng kế tiếp | ネクストホップ | Thiết bị mà gói tin được đưa cho ở bước tiếp theo | [02/01](phase-02-routing/01-routing-table-basics.md) |
| Octet | | octet | オクテット | Nhóm 8 bit; mỗi số trong địa chỉ IPv4 là một octet (0–255) | [01/04](phase-01-foundation/04-ipv4-addressing.md) |
| Off-link |  | nằm ngoài đường dây | 直接接続されていない | Địa chỉ không thuộc mạng máy nối trực tiếp, nên không gửi thẳng tới được | [02/03](phase-02-routing/03-default-route-gateway.md) |
| On-link | | nằm ngay trên đường dây | 直接接続 | Đích ở cùng mạng, gửi thẳng không qua router | [02/01](phase-02-routing/01-routing-table-basics.md) |
| OSI model | OSI | mô hình OSI | OSI参照モデル | Mô hình tham chiếu 7 tầng, dùng làm ngôn ngữ chung khi nói về mạng | [01/02](phase-01-foundation/02-osi-vs-tcpip.md) |
| Packet | | gói tin | パケット | Một mẩu dữ liệu kèm địa chỉ người gửi và người nhận để gửi qua mạng | [01/01](phase-01-foundation/01-packet-journey.md) |
| PAT | PAT | dịch cổng và địa chỉ | PAT | Dạng NAT đổi cả địa chỉ lẫn cổng, để nhiều máy dùng chung một địa chỉ công khai (còn gọi là NAPT) | [02/05](phase-02-routing/05-nat-pat.md) |
| Port | | cổng | ポート | Con số đánh dấu một dịch vụ trên máy; IP chọn máy, cổng chọn dịch vụ | [00/02](phase-00-lab-toolkit/02-linux-network-tools.md) |
| Prefix length | | độ dài tiền tố | プレフィックス長 | Số bit đầu thuộc phần mạng, số sau dấu `/` | [01/05](phase-01-foundation/05-cidr-subnetting.md) |
| Private IP address | | địa chỉ IP riêng | プライベートIPアドレス | Địa chỉ thuộc dải dành cho mạng nội bộ; Internet không định tuyến dải này | [01/06](phase-01-foundation/06-private-public-ip-rfc1918.md) |
| Protocol |  | giao thức | プロトコル | Bộ quy tắc hai bên cùng tuân theo để nói chuyện | [01/02](phase-01-foundation/02-osi-vs-tcpip.md) |
| Public IP address | | địa chỉ IP công khai | グローバルIPアドレス | Địa chỉ duy nhất toàn Internet, ai cũng gửi gói tới được | [01/06](phase-01-foundation/06-private-public-ip-rfc1918.md) |
| Recursive resolver | | bộ phân giải đệ quy | 再帰リゾルバー | Máy chủ DNS nhận câu hỏi của máy bạn rồi tự hỏi các máy chủ khác cho tới khi có đáp án | [03/02](phase-03-core-services/02-dns-resolution.md) |
| Reservation | | đặt trước | 予約 | Luôn cấp cùng một địa chỉ cho một MAC address nhất định | [03/01](phase-03-core-services/01-dhcp.md) |
| Resolver | | bộ phân giải | リゾルバー | Phần mềm/máy chủ nhận câu hỏi "tên này là IP nào" rồi đi tìm đáp án | [03/02](phase-03-core-services/02-dns-resolution.md) |
| RFC 1918 |  | dải địa chỉ riêng theo RFC 1918 | RFC 1918 | Tài liệu chuẩn định nghĩa ba dải địa chỉ private | [01/06](phase-01-foundation/06-private-public-ip-rfc1918.md) |
| Root server | | máy chủ gốc | ルートサーバー | Tầng trên cùng của cây DNS; chỉ đường xuống tầng dưới | [03/02](phase-03-core-services/02-dns-resolution.md) |
| Route | | tuyến | 経路 | Một dòng trong bảng định tuyến | [02/01](phase-02-routing/01-routing-table-basics.md) |
| Router | | bộ định tuyến | ルーター | Thiết bị nhận gói tin rồi chuyển đến chặng kế tiếp theo địa chỉ đích | [01/01](phase-01-foundation/01-packet-journey.md) |
| Routing | | định tuyến | ルーティング | Quá trình chọn đường cho gói tin | [02/01](phase-02-routing/01-routing-table-basics.md) |
| Routing table | | bảng định tuyến | ルーティングテーブル | Danh sách "đích nào thì gửi qua đường nào" mà mỗi thiết bị giữ | [02/01](phase-02-routing/01-routing-table-basics.md) |
| Segment |  | đoạn | セグメント | Đơn vị dữ liệu ở tầng vận chuyển, bọc bởi header TCP | [01/02](phase-01-foundation/02-osi-vs-tcpip.md) |
| Shared address space | CGNAT | không gian địa chỉ dùng chung | 共有アドレス空間 | Dải `100.64.0.0/10` nhà mạng dùng cho CGNAT; không phải private cũng không phải public | [01/06](phase-01-foundation/06-private-public-ip-rfc1918.md) |
| Subnet | | mạng con | サブネット | Một phần của mạng lớn, chia ra để quản lý và cô lập | [01/05](phase-01-foundation/05-cidr-subnetting.md) |
| Subnet mask | | mặt nạ mạng | サブネットマスク | Dãy 32 bit cho biết bao nhiêu bit đầu của địa chỉ thuộc phần mạng | [01/04](phase-01-foundation/04-ipv4-addressing.md) |
| Subnetting | | chia mạng con | サブネット化 | Việc cắt một mạng thành nhiều mạng con | [01/05](phase-01-foundation/05-cidr-subnetting.md) |
| Switch |  | bộ chuyển mạch | スイッチ | Thiết bị nối các máy trong cùng mạng, chuyển khung theo MAC | [01/03](phase-01-foundation/03-ethernet-mac-arp.md) |
| TCP/IP model |  | mô hình TCP/IP | TCP/IPモデル | Mô hình 4 tầng mô tả cách Internet thực sự vận hành | [01/02](phase-01-foundation/02-osi-vs-tcpip.md) |
| TTL (Time To Live) | TTL | thời gian sống | 生存時間 | Số chặng tối đa còn lại của gói tin; mỗi router trừ 1, về 0 thì gói bị bỏ | [01/01](phase-01-foundation/01-packet-journey.md) |
| WSL2 | WSL2 | WSL phiên bản 2 | WSL2 | Cách chạy Linux ngay trong Windows | [00/01](phase-00-lab-toolkit/01-lab-environment.md) |
