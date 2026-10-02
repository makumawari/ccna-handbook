# Lab 00/01 — Lab environment

Chapter: [00/01-lab-environment](../../../book/phase-00-lab-toolkit/01-lab-environment.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`. Claude không tự viết output.

## An toàn và chi phí
- Các lệnh chỉ **đọc thông tin** hoặc chạy container tạm thời (`--rm`); không đổi cấu hình mạng của Windows.
- Không tạo tài nguyên AWS, **không có chi phí**. Teardown: gõ `exit` trong container.
- Trên máy công ty: kiểm tra chính sách trước khi cài WSL/Docker.

## Chuẩn bị
Cài WSL2 và Docker (xem mục 7 của chapter). Kiểm tra: `wsl --list --verbose` thấy distro ở phiên bản 2; `docker version` chạy được.

## Các bước
**1. Predict:** ghi ra giấy: IP của WSL2 có giống Windows không? Container mặc định có IP trong dải nào? Container `--network none` có những giao diện nào?

**2. Run:**

```powershell
wsl --list --verbose
wsl hostname -I
docker version
docker run --rm alpine ip addr
docker run --rm --network none alpine ip addr
```

**3. Verify:** so sánh địa chỉ bốn nơi: Windows, WSL2, container mặc định, container `none`.

**4. Break it:**

```powershell
docker run --rm -it --network none alpine sh
```

Trong container:

```sh
ip addr
ping -c 1 -W 2 192.0.2.1
```

Dự đoán: chỉ có `lo`; ping báo ngay không có đường đi. Thoát bằng `exit`.

## Dọn dẹp
`docker ps -a` không còn container của lab (dùng `--rm`).

## Ghi kết quả (làm sạch trước khi commit)
Lưu output vào `expected-output.txt`, thay IP thật bằng IP giả (`10.0.x.x`, `192.168.x.x`, `192.0.2.x`, `198.51.100.x`, `203.0.113.x`). Chạy `python tools/lint_chapters.py`.
