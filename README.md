# AI Training – Bài tập theo tuần

Nguyễn Thúy Ngọc · AI Training (MindX), Weeks 1–5

Mỗi tuần nằm trong một thư mục riêng. Đề bài gốc của từng tuần được giữ nguyên (trong `brief/` hoặc `overview.md`), bên cạnh là bài làm.

| Tuần | Thư mục | Nội dung | Bắt đầu đọc từ |
| --- | --- | --- | --- |
| 1 | [week-1-tdd-research/](week-1-tdd-research/) | Nghiên cứu TDD với 3 workflow làm việc cùng AI (không có code) | [Report.md](week-1-tdd-research/Report.md) |
| 2 | [week-2-3-cli/](week-2-3-cli/) | CLI `tickets`: tạo, liệt kê, xem, cập nhật ticket lưu trong file JSON, làm theo TDD (JavaScript) | [README](week-2-3-cli/README.md) · [docs/week-2-tickets/](week-2-3-cli/docs/week-2-tickets/) |
| 3 | [week-2-3-cli/](week-2-3-cli/) | CLI `kb`: tìm, liệt kê, đọc, thêm tài liệu Knowledge Base qua Mock client và HTTP client (TypeScript) | [README](week-2-3-cli/README.md#knowledge-base-cli-kb) · [docs/week-3-kb/](week-2-3-cli/docs/week-3-kb/) |
| 4 | [week-4-odoo-helpdesk/](week-4-odoo-helpdesk/) | Xử lý 6 scenario ticket trên Odoo Helpdesk, kèm email/chat draft (không có code) | [README](week-4-odoo-helpdesk/README.md) |
| 5 | [week-5-analysis-automation/](week-5-analysis-automation/) | Phân tích 118 ticket thật + login bot tự xử lý ticket đăng nhập, tích hợp Odoo (Python) | [README](week-5-analysis-automation/README.md) |

Tuần 2 và tuần 3 dùng chung một project Node.js (một `package.json`), vì `kb` được thêm vào cùng repo với `tickets`; hai phần code không phụ thuộc nhau.

## Cấu trúc

```
week-1-tdd-research/          Report.md, đề bài, ảnh chụp toàn bộ hội thoại với AI (chat_history.pdf)
week-2-3-cli/                 project Node.js: bin/, src/, test/ (tickets + kb)
  docs/week-2-tickets/        tuần 2: quyết định thiết kế, test list, kết quả test, nhật ký
  docs/week-3-kb/             tuần 3: đề bài, quyết định thiết kế, kết quả test, nhật ký
week-4-odoo-helpdesk/         bài làm 6 scenario, bản ghi Odoo (PDF), export
  brief/                      đề bài tuần 4
week-5-analysis-automation/   phân tích, kế hoạch hành động, KB đăng nhập, kết quả test
  brief/, data/               đề bài và dữ liệu sample.xlsx
  reports/                    script phân loại ticket + CSV
  automation/                 login bot (Python) và test
```

## Chạy nhanh

```bash
# Tuần 2–3
cd week-2-3-cli && npm install && npm test

# Tuần 5
cd week-5-analysis-automation
python reports/classify_tickets.py                     # phân tích dữ liệu
cd automation && python -m unittest -v                 # test login bot
```

## Lịch sử

Repo này trước đây là `ticket-manager-cli` (tuần 2–5, mỗi tuần một thư mục `docs*`); tuần 1 nằm ở repo riêng `ai-training-week1`. Ngày 12/11/2026 hai repo được gộp làm một và sắp xếp lại theo tuần. Lịch sử commit của cả hai repo vẫn được giữ (`git log --follow <file>` để xem lịch sử một file trước khi đổi chỗ).
