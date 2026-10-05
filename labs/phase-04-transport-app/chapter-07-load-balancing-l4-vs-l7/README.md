# Lab 04/07 — Cân bằng tải, health check thụ động và X-Forwarded-For

Chapter: [04/07-load-balancing-l4-vs-l7](../../../book/phase-04-transport-app/07-load-balancing-l4-vs-l7.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Chạy local bằng Docker Compose. Cần Internet để kéo image `nginx:alpine` (kiểm tra image còn tồn tại trước khi dùng).
- Cổng publish chỉ trên `127.0.0.1:8088`. Không tạo tài nguyên AWS, không có chi phí.
- Thư mục lab tạm; xóa khi xong (phần Dọn dẹp).

## Chuẩn bị
Tạo thư mục tạm, ví dụ `lab-lb`, rồi tạo hai tệp sau (UTF-8, LF).

`docker-compose.yml`:

```yaml
services:
  app1:
    image: nginx:alpine
    command: sh -c "echo app1 > /usr/share/nginx/html/index.html && nginx -g 'daemon off;'"
  app2:
    image: nginx:alpine
    command: sh -c "echo app2 > /usr/share/nginx/html/index.html && nginx -g 'daemon off;'"
  lb:
    image: nginx:alpine
    ports:
      - "127.0.0.1:8088:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - app1
      - app2
```

`nginx.conf`:

```nginx
upstream backend {
    server app1:80 max_fails=1 fail_timeout=10s;
    server app2:80 max_fails=1 fail_timeout=10s;
}
server {
    listen 80;
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 2s;
    }
}
```

## Phần A — Chia tải
**1. Predict:** 6 yêu cầu liên tiếp cho kết quả `app1`/`app2` thế nào?

**2. Run:**

```bash
docker compose up -d
for i in 1 2 3 4 5 6; do curl -s http://127.0.0.1:8088/; done
```

**3. Verify:** dự đoán luân phiên `app1`, `app2`, ... (round robin mặc định).

## Phần B — Break it: một backend chết
```bash
docker compose stop app2
for i in 1 2 3 4 5 6; do curl -s -o /dev/null -w "%{http_code} " http://127.0.0.1:8088/; done; echo
docker compose start app2
```
Dự đoán: nginx thử `app2` và chuyển sang `app1` khi kết nối thất bại, nên phần lớn yêu cầu vẫn `200`; sau khi `app2` bị đánh dấu lỗi trong `fail_timeout`, mọi yêu cầu tới `app1`. Ghi lại số lỗi (nếu có) và thời điểm.

## Phần C — X-Forwarded-For và header giả
Thêm vào `nginx.conf` một location in header (tạm) hoặc dùng log của backend; cách đơn giản nhất: đổi `app1` thành một container in header nhận được (ví dụ dùng `nginx` với `return 200 "$http_x_forwarded_for\n";` trong location riêng). Rồi:

```bash
curl -s -H "X-Forwarded-For: 203.0.113.99" http://127.0.0.1:8088/
```
Dự đoán: header ở backend có dạng `203.0.113.99, <IP của client theo nginx>`; mục giả nằm **bên trái**. `[CHƯA CHẠY]` — người học chốt cấu hình in header và ghi lại.

## Dọn dẹp
```bash
docker compose down
```
Xóa thư mục lab tạm.

## Ghi kết quả (làm sạch trước khi commit)
Lưu output (đã làm sạch) vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
