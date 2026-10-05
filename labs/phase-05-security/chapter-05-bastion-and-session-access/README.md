# Lab 05/05 — Bastion và truy cập theo phiên (lab rút gọn)

Chapter: [05/05-bastion-and-session-access](../../../book/phase-05-security/05-bastion-and-session-access.md) · Importance: Should

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## Phạm vi
Chapter Should nên lab rút gọn. Lab này **hoàn toàn cục bộ**: không dựng bastion hay dịch vụ AWS thật (tránh chi phí và rủi ro). Bạn luyện cấu hình `ProxyJump` và phân biệt lỗi khóa với lỗi mạng của SSH.

## An toàn và chi phí
- Chạy trong WSL2/Linux (cần `ssh`, `ssh-keygen`). Khóa thử được tạo trong một thư mục tạm và **chỉ dùng cho lab**.
- **Không commit khóa** vào repo; xóa thư mục tạm khi xong.
- Không tạo tài nguyên AWS, không có chi phí.

## Phần A — Cấu hình hiệu lực với ProxyJump
**1. Predict:** `ssh -G` (không kết nối) sẽ in những dòng nào liên quan tới jump host?

**2. Run:**

```bash
ssh -V
ssh -G -J admin@jump.example.com admin@target.example.com | grep -iE '^(hostname|user|port|proxyjump) '
```

**3. Verify:** có dòng `proxyjump admin@jump.example.com` cùng `hostname target.example.com`, `user admin`, `port 22`.

## Phần B — Khóa thử và hai kiểu thất bại

```bash
cd "$(mktemp -d)"
ssh-keygen -t ed25519 -f lab-key -N "" -C "lab-only-throwaway" >/dev/null
ls -l lab-key lab-key.pub
cut -c1-40 lab-key.pub
chmod 644 lab-key
ssh -i lab-key -o BatchMode=yes -o ConnectTimeout=3 admin@192.0.2.1; echo "mã thoát: $?"
chmod 600 lab-key
ssh -i lab-key -o BatchMode=yes -o ConnectTimeout=3 admin@192.0.2.1; echo "mã thoát: $?"
```

Dự đoán: với quyền `644`, SSH từ chối dùng khóa vì quyền quá rộng (lỗi cục bộ, chưa gửi gói nào); với quyền `600`, khóa hợp lệ nhưng `192.0.2.1` không ai trả lời nên SSH hết thời gian kết nối (lỗi mạng).

## Dọn dẹp
Xóa thư mục tạm chứa `lab-key` và `lab-key.pub` (thư mục mà `mktemp -d` đã tạo; xem `pwd`).

## Ghi kết quả (làm sạch trước khi commit)
Không đưa khóa vào repo; chỉ lưu output văn bản (đã làm sạch) vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
