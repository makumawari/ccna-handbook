# Lab 04/08 — Reverse proxy và header chuyển tiếp (lab rút gọn)

Chapter: [04/08-reverse-proxy](../../../book/phase-04-transport-app/08-reverse-proxy.md) · Importance: Should

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Chạy local bằng Docker Compose; cần Internet để kéo image `nginx:alpine`. Cổng chỉ publish trên `127.0.0.1:8089`.
- Không tạo tài nguyên AWS, không có chi phí.

## Chuẩn bị
Tạo thư mục tạm `lab-proxy` với hai tệp (UTF-8, LF).

`docker-compose.yml`:

```yaml
services:
  backend:
    image: nginx:alpine
    volumes:
      - ./backend.conf:/etc/nginx/conf.d/default.conf:ro
  proxy:
    image: nginx:alpine
    ports:
      - "127.0.0.1:8089:80"
    volumes:
      - ./proxy.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - backend
```

`backend.conf` (in ra header nhận được):

```nginx
server {
    listen 80;
    location / {
        default_type text/plain;
        return 200 "host=$host xff=$http_x_forwarded_for proto=$http_x_forwarded_proto\n";
    }
}
```

`proxy.conf` (bản đầy đủ header):

```nginx
server {
    listen 80;
    location / {
        proxy_pass http://backend;
        proxy_set_header Host              $host;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Phần A — Có đủ header
**1. Predict:** `host`, `xff`, `proto` ở backend là gì khi gọi `curl http://127.0.0.1:8089/`?

**2. Run:**

```bash
docker compose up -d
curl -s http://127.0.0.1:8089/
```

**3. Verify:** dự đoán `host=127.0.0.1`, `xff` là IP nguồn nginx thấy (thường là địa chỉ cổng Docker), `proto=http`.

## Phần B — Break it: thiếu header và header giả
Bỏ dòng `proxy_set_header Host $host;` khỏi `proxy.conf`, rồi:

```bash
docker compose restart proxy
curl -s http://127.0.0.1:8089/
curl -s -H "X-Forwarded-For: 203.0.113.99" http://127.0.0.1:8089/
```
Dự đoán: `host=backend` (tên upstream thay vì `127.0.0.1`); với header giả, `xff=203.0.113.99, <IP nguồn>`, mục giả nằm bên trái.

## Dọn dẹp
```bash
docker compose down
```
Xóa thư mục lab tạm.

## Ghi kết quả (làm sạch trước khi commit)
Lưu output (đã làm sạch) vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
