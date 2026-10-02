# Lab 01/05 — CIDR and subnetting

Chapter: [01/05-cidr-subnetting](../../../book/phase-01-foundation/05-cidr-subnetting.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
Chỉ tính toán bằng Python, không thay đổi hệ thống. Không có chi phí.

## Các bước
**1. Predict (tính tay):**
- `10.0.1.0/24` chia thành `/26` được mấy mạng? Địa chỉ đầu của từng mạng?
- `10.0.1.77/26` thuộc mạng nào?
- `10.0.0.0/16` và `10.0.5.0/24` có chồng lấn không?

**2. Run:**

```bash
python3 -c "import ipaddress as i; n=i.ip_network('10.0.1.0/24'); print([str(s) for s in n.subnets(new_prefix=26)])"
python3 -c "import ipaddress as i; print(i.ip_interface('10.0.1.77/26').network)"
python3 -c "import ipaddress as i; print(i.ip_network('10.0.0.0/16').overlaps(i.ip_network('10.0.5.0/24')))"
```

**3. Verify:** so với phép tính tay.

**4. Break it (hai lỗi thiết kế):**

```bash
python3 -c "import ipaddress as i; n=i.ip_network('10.0.2.0/28'); print(n.num_addresses, n.num_addresses-2)"
python3 -c "import ipaddress as i; print(i.ip_network('10.0.0.0/16').overlaps(i.ip_network('10.0.5.0/24')))"
```

Dự đoán: `16 14` (không đủ cho 20 máy) và `True` (chồng lấn). Khôi phục: đổi kế hoạch (`stg=10.1.0.0/16`) và chạy lại phép kiểm tra.

## Dọn dẹp
Không có.

## Ghi kết quả
Lưu vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
