# Week 5 — Reporting, Analysis & Automation

Bài nộp Week 5: phân tích 118 ticket thật để tìm vấn đề lặp lại, và xây **login bot** tự xử lý ticket lỗi đăng nhập (Scenario 1) tích hợp với Odoo Helpdesk.

- Đề bài: [overview.md](brief/overview.md) · [tasks.md](brief/tasks.md) · [architecture.md](brief/architecture.md) · dữ liệu [sample.xlsx](data/sample.xlsx)
- Odoo: https://choi.odoo.com/odoo/helpdesk

## Kết quả chính

- **Top 5 vấn đề** chiếm 72 % ticket: Lead/Thanh toán 24 · Enroll 20 · TMS 19 · Đăng nhập 14 · Cấp tài khoản 8.
- **Login bot**: chạy thật trên Odoo đúng 8/8 ticket test (#250–#257), 51/51 test pass; trên dữ liệu thật nhận diện lỗi đăng nhập với precision 100 %, recall 79 %.
- **Kế hoạch giảm ticket**: ước tính −34 % ticket xử lý tay.

## Đối chiếu Acceptance Criteria

| AC | Bằng chứng | Trạng thái |
| --- | --- | --- |
| Xác định pattern ticket lặp lại | [analysis.md](analysis.md) mục 4–5 · [reports/](reports/) (script + CSV) | ✅ |
| Ghi lại phát hiện và khuyến nghị kèm số liệu | [analysis.md](analysis.md) mục 5–9 · report Odoo trong [images/](images/) | ✅ |
| Automation cho Scenario 1: Login | [automation/](automation/) · [automation.md](automation.md) | ✅ |
| Tự phân tích ticket, kiểm tra HR, xử lý theo kết quả | [automation.md](automation.md) mục 3–4 · [TEST-RESULTS.md](TEST-RESULTS.md) mục 2–3, 6 | ✅ |
| Tích hợp Odoo (webhook/API) | [automation.md](automation.md) mục 6 (API + polling + webhook) · chạy thật trên Odoo: [TEST-RESULTS.md](TEST-RESULTS.md) mục 6, ảnh `images/w5-bot-*.pdf` | ✅ |
| Kế hoạch giảm số lượng ticket | [action-plan.md](action-plan.md) | ✅ |

## Tài liệu

| File | Nội dung |
| --- | --- |
| [analysis.md](analysis.md) | Phân tích pattern: phương pháp, top 5, phát hiện thêm, nguyên nhân gốc, khuyến nghị |
| [automation.md](automation.md) | Login bot: vì sao automation, luồng xử lý, bảng quyết định, tích hợp Odoo, trigger, log |
| [kb-login.md](kb-login.md) | Bài KB "Không đăng nhập được LMS" cho người dùng và team Support |
| [TEST-RESULTS.md](TEST-RESULTS.md) | Kết quả test, demo, đo bộ phân loại trên dữ liệu thật |
| [action-plan.md](action-plan.md) | Kế hoạch giảm ticket: chỉ số, hành động, lộ trình |
| [reports/](reports/) | Script phân nhóm + CSV kết quả + file import Odoo |
| [images/](images/) | Report Odoo (`w5-0*`) và ticket bot đã xử lý trên Odoo (`w5-bot-*`) |

## Chạy lại

```
python reports/classify_tickets.py   # phân tích dữ liệu
cd automation
python -m unittest -v                      # test bot
python -m login_bot.run --demo             # demo bot không cần Odoo
```

## Làm việc với AI

Code, test và bản nháp tài liệu tuần này do Claude (AI) viết theo yêu cầu của người làm bài. Người làm bài tạo API key, import dữ liệu và làm report trên Odoo, chạy bot trên Odoo thật, chụp bằng chứng và quyết định nội dung cuối cùng. Khi chạy thử trên Odoo thật đã phát hiện và sửa 2 lỗi trước khi chạy chính thức ([TEST-RESULTS.md](TEST-RESULTS.md) mục 6).
