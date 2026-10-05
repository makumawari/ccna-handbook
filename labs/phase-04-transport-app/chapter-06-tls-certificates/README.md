# Lab 04/06 — TLS and certificates

Chapter: [04/06-tls-certificates](../../../book/phase-04-transport-app/06-tls-certificates.md) · Importance: Must

> **Trạng thái:** `[CHƯA CHẠY]` — người học chạy và ghi `expected-output.txt`.

## An toàn và chi phí
- Chạy trong WSL2/Linux (cần `openssl` và `curl`).
- Phần B tạo khóa riêng và chứng chỉ tự ký **thử** trong một thư mục tạm. **Không commit `k.pem`/`c.pem`** (`.gitignore` loại `*.pem`, `*.key`) và xóa thư mục tạm khi xong. `curl -k` chỉ dùng trong lab này.
- Không tạo tài nguyên AWS, không có chi phí.

## Phần A — Đọc chứng chỉ thật
**1. Predict:** phiên bản TLS nào, Issuer là ai, hết hạn khi nào (còn bao nhiêu ngày), SAN có những tên nào?

**2. Run:**

```bash
openssl s_client -connect example.com:443 -servername example.com -brief </dev/null
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | openssl x509 -noout -ext subjectAltName
curl -sv -o /dev/null https://example.com 2>&1 | grep -iE "TLS|SSL|subject|issuer|expire|start date"
```

**3. Verify:** ghi phiên bản TLS, Issuer, ngày hết hạn, số ngày còn lại, SAN.

## Phần B — Break it (ba kiểu lỗi chứng chỉ)

```bash
cd "$(mktemp -d)"
openssl req -x509 -newkey rsa:2048 -nodes -keyout k.pem -out c.pem -days 1 -subj "/CN=www.shopnet.example" -addext "subjectAltName=DNS:www.shopnet.example"
openssl s_server -accept 8443 -cert c.pem -key k.pem -www >/dev/null 2>&1 &
SPID=$!
sleep 1
curl -sS -o /dev/null https://127.0.0.1:8443/; echo "A: mã thoát $?"
curl -sS -o /dev/null --cacert c.pem --resolve www.shopnet.example:8443:127.0.0.1 https://www.shopnet.example:8443/; echo "B: mã thoát $?"
curl -sS -o /dev/null --cacert c.pem https://127.0.0.1:8443/; echo "C: mã thoát $?"
curl -sS -o /dev/null -k https://127.0.0.1:8443/; echo "D: mã thoát $?"
openssl x509 -in c.pem -noout -checkend 172800; echo "E (còn hạn thêm 2 ngày không): mã thoát $?"
kill "$SPID"
```

Dự đoán: A thoát 60 (không tin chứng chỉ tự ký); B thoát 0; C thoát 60 (tin chứng chỉ nhưng sai tên vì IP không có trong SAN); D thoát 0 nhưng đã bỏ mọi xác thực; E thoát khác 0 (chứng chỉ chỉ có hạn 1 ngày).

## Dọn dẹp
Server đã dừng bằng `kill`; xóa thư mục tạm (đường dẫn do `mktemp -d` in ra khi bạn `pwd`) cùng `k.pem`, `c.pem`.

## Ghi kết quả (làm sạch trước khi commit)
Không đưa khóa riêng hay chứng chỉ vào repo; chỉ lưu output văn bản (đã làm sạch) vào `expected-output.txt`. Chạy `python tools/lint_chapters.py`.
