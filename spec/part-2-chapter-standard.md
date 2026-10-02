# Network Fundamentals Handbook (Infra / DevOps / Cloud)

## Project Specification

Version: 1.0 (đã duyệt 2026-10-02)

# PART 2 — Quy chuẩn của mỗi Chapter

> Đây là "DNA" của handbook: mọi chapter đều phải theo tài liệu này. Template 18 mục dưới đây là **chuẩn của repo này**; repo Java chỉ là tham khảo ý tưởng. Mâu thuẫn với `CLAUDE.md` thì ưu tiên theo CLAUDE.md §0.

---

# 1. Một chapter KHÔNG phải là

Không phải cheat sheet, không phải FAQ, không phải ghi chú lệnh, không phải trang copy từ tài liệu nguồn. Một chapter là một **chương sách kỹ thuật ngắn**: có mở đầu bằng sự cố, dẫn dắt từ vấn đề tới khái niệm, có hình, có lab, có hậu quả khi làm sai và cách chẩn đoán.

---

# 2. Tên chapter, file và metadata

## 2.1 Slug và Title

- **Slug** (tên file, roadmap, metadata): danh từ ngắn, ASCII không dấu, ví dụ `05-nat-pat.md`. File nằm ở `book/phase-NN-<slug>/NN-<slug>.md`.
- **Title** (H1 trong file): dạng **câu hỏi**, ví dụ `# Máy trong mạng private ra Internet bằng cách nào? (NAT/PAT)`.
- Hai vai trò này không lẫn nhau khi review: roadmap và bảng phụ thuộc dùng slug, người đọc thấy title.

## 2.2 Front matter và khối Metadata

Đầu file có YAML front matter (cho tag filter của MkDocs), ngay sau H1 là khối Metadata:

````markdown
---
tags:
  - NAT
  - Routing
---

# Máy trong mạng private ra Internet bằng cách nào? (NAT/PAT)

## Metadata

```yaml
Chapter: nat-pat
Phase: 02 — routing
Importance: Must            # Must | Should | Nice
Status: todo                # todo | draft | reviewed | done
Prerequisites:
  - Phase 01 / 06-private-public-ip-rfc1918
  - Phase 02 / 03-default-route-gateway
Used Later:
  - Phase 06 / 02-route-table-igw-nat-gateway
  - Phase 05 / 03-sg-vs-nacl-concept
Estimated Reading: 25 phút
Estimated Practice: 40 phút
```
````

Quy tắc: `Prerequisites` và `Used Later` dùng slug; đây là nơi duy nhất ghi "Used Later" (không thành mục riêng trong 18 mục). Không ghi "Interview Frequency %" vì không kiểm chứng được.

---

# 3. Template 18 mục

Giữ **đúng tên và thứ tự**; không tự thêm, bớt hay đổi chỗ. Mỗi mục là một heading `##`, đánh số như bảng dưới.

| # | Mục | Nội dung bắt buộc phải có |
|---|---|---|
| 1 | Story | Sự cố thật (đã viết lại bằng dữ liệu giả) mở đầu bằng triệu chứng, không bằng định nghĩa |
| 2 | Objectives | Sau chapter làm được gì, **đo được** ("dự đoán đúng…", "chẩn đoán được…") |
| 3 | Prerequisites | Danh sách `> Xem lại: ...` tới chapter cần biết trước |
| 4 | Why it exists | Vấn đề nó giải quyết; nếu không có thì sao |
| 5 | Mental model | Một ví von đời thường + tóm tắt một câu |
| 6 | How it works | Luồng gói tin / luồng điều khiển: Mermaid + đoạn giải thích |
| 7 | Key settings | Thông số hay phải chỉnh trong thực tế, kèm giá trị mặc định đã kiểm chứng |
| 8 | AWS mapping | Dịch vụ/resource AWS, CloudFormation type, IAM liên quan (nếu có) |
| 9 | Hands-on lab | Predict → Run → Verify; lệnh ghi rõ `bash`/`powershell`/`cmd` |
| 10 | Break it | Gây một lỗi cụ thể, quan sát triệu chứng, khôi phục |
| 11 | Troubleshooting | Triệu chứng → thứ tự kiểm tra → công cụ; gồm kết quả của mục 10 |
| 12 | Security & cost | Hệ quả bảo mật; nguồn phát sinh chi phí theo giờ/GB (không ghi số tiền) |
| 13 | Misconceptions | Hiểu nhầm hay gặp, và sự thật |
| 14 | Interview questions | Câu hỏi + "gợi ý ý chính" hiển thị sẵn; **đáp án mẫu nằm trong block collapse** (xem §3.2) |
| 15 | Exercises | Bài tập có deliverable cụ thể; không ghi "tìm hiểu X" |
| 16 | Cheat sheet | Một trang tóm tắt: khái niệm, lệnh, thứ tự debug |
| 17 | Glossary terms | EN / VN / JA, đồng bộ với `book/glossary.md` |
| 18 | Further reading | Nguồn gốc (RFC, tài liệu chính thức), kèm ngày kiểm tra |

## 3.1 Hướng dẫn từng mục

- **Story:** viết như một đoạn truyện ngắn: "một chiều thứ Sáu, service A không gọi được service B…". Không mở bằng định nghĩa. Tên hệ thống dùng `shopnet`.
- **Why it exists → Mental model → How it works:** đúng thứ tự "vì sao" trước "thế nào". Không giải thích cơ chế trước khi người đọc hiểu vấn đề.
- **How it works:** luôn là packet journey: từng chặng gói tin đi qua. Sơ đồ theo mục 5; **mỗi sơ đồ có đoạn giải thích đi kèm**.
- **Key settings:** chỉ những thông số gặp trong 80% công việc.
- **AWS mapping:** chapter Phase 06 không dạy lại khái niệm, dùng `> Xem lại:`. Mọi sự thật AWS có thể đổi phải có `<!-- verified: YYYY-MM-DD <url> -->`; chưa kiểm chứng → `[CHƯA KIỂM CHỨNG]`.
- **Break it:** nêu rõ *thay đổi cụ thể*, *triệu chứng quan sát được*, *cách khôi phục*, và chạy được lại từ đầu.
- **Interview questions:** phân cấp Junior / Middle / Senior nếu phù hợp; đáp án mẫu viết bằng lời của người học, không chép câu trả lời mẫu của nguồn khác. Cách trình bày ở §3.2.

## 3.2 Interview questions: gợi ý hiển thị, đáp án thu gọn

Mục đích: người đọc **tự trả lời trước**, chỉ mở đáp án để đối chiếu sau khi đã có câu trả lời của mình.

- **Hiển thị sẵn:** câu hỏi và **gợi ý ý chính** (các ý cần chạm tới, không phải câu trả lời hoàn chỉnh).
- **Thu gọn:** đáp án mẫu (đáp án chuẩn) nằm trong block collapse, mặc định **đóng**. Dùng cú pháp `???` của `pymdownx.details` (bật trong `mkdocs.yml`, xem Part 3).
- Gợi ý ý chính không được lộ đáp án: chỉ nêu hướng ("nghĩ về tầng nào, trạng thái nào, ai khởi tạo kết nối"), không nêu kết luận.
- Đáp án mẫu nên ngắn, có cấu trúc (ý chính → giải thích → ví dụ/lệnh kiểm tra); sự thật AWS trong đáp án cũng cần `verified` hoặc `[CHƯA KIỂM CHỨNG]`.

````markdown
### Q1 (Middle) — Vì sao máy trong subnet private không ra được Internet dù đã có default route?

**Gợi ý ý chính:**
- Gói đi ra: route nào, qua thiết bị nào?
- Gói trả về: ai dịch địa chỉ, ai biết đường về?
- Tầng nào cần kiểm tra trước?

??? success "Đáp án mẫu (tự trả lời trước khi mở)"
    1. Ý chính thứ nhất …
    2. Ý chính thứ hai …
    3. Cách kiểm tra bằng lệnh …
````

> Lưu ý trên Windows/GitHub: nếu nền tảng không render `???`, nội dung vẫn đọc được dạng văn bản thụt lề; không đặt thông tin an toàn quan trọng chỉ trong block collapse.

---

# 4. Quy tắc viết trong chapter

1. **Thuật ngữ lần đầu xuất hiện:** `Term (bản dịch — giải thích ngắn bằng từ đơn giản)`; tiếng Nhật `日本語 (romaji — nghĩa)`. Không giải thích thuật ngữ bằng thuật ngữ chưa giải thích.
2. **Thuật ngữ đã giải thích ở chapter trước:** `> Xem lại:` + link glossary, không giải thích lại.
3. **Mọi thuật ngữ mới** thêm vào `book/glossary.md`.
4. **Không dạy lại** nội dung chapter trước; chỉ tham chiếu.
5. **Chỉ ra sai lầm** cụ thể: giả định sai, rủi ro bảo mật, độ phức tạp thừa, rủi ro production.
6. **Dữ liệu ví dụ:** chỉ dùng `shopnet` và dải IP ở `CLAUDE.md` §5.3; không có dữ liệu thật.
7. **Không chép nguyên văn** Cisco, khóa học, sách, blog; viết bằng lời của người học, ghi nguồn ở mục 18.

---

# 5. Sơ đồ

- Mermaid là mặc định cho luồng gói tin, dependency, deployment; luồng rất đơn giản dùng text (`User → ALB → App → DB`).
- Mặc định `flowchart LR`; phân cấp dùng `flowchart TD`; tương tác theo thời gian dùng `sequenceDiagram` (ví dụ TCP handshake).
- Mỗi sơ đồ một ý. Hệ thống phức tạp tách thành Business / Network / Security / Monitoring flow.
- Nhãn có ký tự đặc biệt đặt trong dấu nháy kép.
- Sau mỗi sơ đồ: giải thích quan hệ chính và vì sao mỗi thành phần tồn tại.

---

# 6. Lab và kiểm chứng

- Mỗi lab theo bốn bước **Predict → Run → Verify → Break it**; người học ghi dự đoán **trước khi chạy**.
- Cấu trúc thư mục lab: `labs/phase-NN-<slug>/chapter-NN-<slug>/` gồm `README.md`, file chạy, `expected-output.txt`, teardown.
- **Người học chạy lab và dán output.** Claude không viết hay bịa `expected-output.txt`. Chưa có output thật → `[CHƯA CHẠY]`.
- An toàn lab AWS: theo `CLAUDE.md` §3 (sandbox, Region `ap-northeast-1`, tag `Project=net-handbook`, cảnh báo chi phí, teardown + lệnh kiểm tra đã xóa hết).

---

# 7. Importance và mức bắt buộc

Ba mức, thay cho thang ★ của repo Java:

- **Must** — dùng hằng ngày hoặc gây sự cố nếu thiếu.
- **Should** — gặp thường xuyên trong dự án.
- **Nice** — nên biết khái niệm, không cần lab đầy đủ.

| Mục | Must | Should | Nice |
|---|---|---|---|
| 1 Story, 2 Objectives, 3 Prerequisites, 4 Why it exists, 5 Mental model, 6 How it works | Đủ | Đủ | Đủ (ngắn) |
| 7 Key settings, 12 Security & cost, 13 Misconceptions | Đủ | Đủ | Tùy chọn |
| 8 AWS mapping | Đủ nếu có liên quan AWS | Tùy chọn | Bỏ |
| 9 Hands-on lab | Đủ + `expected-output.txt` | Rút gọn | Bỏ |
| 10 Break it, 11 Troubleshooting | Đủ (≥ 1 Break it, kết quả ghi vào mục 11) | Rút gọn | Bỏ |
| 14 Interview questions, 15 Exercises, 16 Cheat sheet, 17 Glossary terms | Đủ | Đủ | Đủ (ngắn) |
| 18 Further reading | Đủ | Đủ | Đủ |

Nguyên tắc: **không bao giờ bỏ** 1 Story, 4 Why it exists, 6 How it works, 11 Troubleshooting (trừ Nice được ghi rõ "Bỏ"), 14 Interview questions và 18 Further reading. Mục "Bỏ" có thể được thêm lại nếu tác giả thấy đáng viết.

---

# 8. Trạng thái và Definition of Done

`Status`: `todo` (khung `TODO`) → `draft` (đã viết) → `reviewed` (đã qua review theo `CLAUDE.md` §9) → `done`.

Một chapter chỉ được `done` khi:

- [ ] Đủ mục theo bảng mức bắt buộc ở §7 cho Importance của nó.
- [ ] Lab đã chạy thật, `expected-output.txt` là kết quả thật; Break it đã thực hiện và ghi lại triệu chứng.
- [ ] Troubleshooting có đủ triệu chứng → thứ tự kiểm tra → công cụ.
- [ ] Mọi sự thật AWS có `verified` + ngày, hoặc được đánh dấu `[CHƯA KIỂM CHỨNG]` và nằm trong danh sách việc cần làm.
- [ ] Glossary, cross-reference, coverage map đã cập nhật (`troubleshooting-playbook.md` nếu có).
- [ ] `tools/lint_chapters.py` sạch, gồm quét thông tin nhạy cảm (áp dụng khi công cụ đã tồn tại).
- [ ] Người học tự đánh dấu đã giải thích lại được bằng lời của mình.

---

Đây là **Part 2** của Specification (v1.0).
