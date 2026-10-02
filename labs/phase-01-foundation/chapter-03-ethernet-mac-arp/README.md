# Lab 01/03 — Ethernet, MAC and ARP

Chapter: [01/03-ethernet-mac-arp](../../../book/phase-01-foundation/03-ethernet-mac-arp.md) · Importance: Should

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Phần A chỉ **đọc** bảng ARP và ping gateway.
- Phần B chạy trong container tạm thời (`--rm`, `--cap-add NET_ADMIN`); chỉ sửa bảng ARP **trong container**.
- Không có chi phí.

## Phần A — Đọc bảng ARP
**1. Predict:** IP nào chắc chắn có trong bảng ARP? (gợi ý: default gateway). MAC của nó có dạng gì?

**2. Run** (thay `192.168.1.1` bằng default gateway của bạn):

```powershell
ping -n 1 192.168.1.1
arp -a
Get-NetNeighbor -AddressFamily IPv4
```

**3. Verify:** gateway có trong bảng chưa? Trạng thái là gì?

## Phần B — Break it (gán sai MAC cho gateway)

```powershell
docker run --rm -it --cap-add NET_ADMIN alpine sh
```

Trong container:

```sh
GW=$(ip route show default | awk '{print $3}')
ping -c 1 -W 2 $GW
ip neigh replace $GW lladdr 02:00:00:00:00:99 dev eth0 nud permanent
ping -c 1 -W 2 $GW
ip neigh del $GW dev eth0
ping -c 1 -W 2 $GW
```

Dự đoán: ping 1 thành công; ping 2 hết thời gian (MAC sai); ping 3 thành công lại (ARP hỏi lại). Nếu gateway không trả lời ping ngay từ đầu, bỏ qua bài này.

## Dọn dẹp
Thoát bằng `exit`; container `--rm` tự xóa.

## Ghi kết quả (làm sạch trước khi commit)
Thay IP và MAC thật bằng dữ liệu giả; lưu vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
