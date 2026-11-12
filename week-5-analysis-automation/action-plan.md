# Kế hoạch giảm số lượng ticket — Week 5

Dựa trên [analysis.md](analysis.md) (118 ticket thật của team Technical Support). Mục tiêu: **giảm 30 % số ticket phải xử lý tay trong 2 tháng** mà không làm chậm thời gian phản hồi.

## 1. Mục tiêu đo được

| Chỉ số | Hiện tại (sample) | Mục tiêu sau 2 tháng | Cách đo |
| --- | --- | --- | --- |
| Ticket phải xử lý tay / kỳ | 118 | ≤ 83 (−30 %) | Odoo report: ticket không có tag `auto-*` |
| Ticket không có tag hệ thống | 52 (44 %) | < 10 % | Odoo: filter *Tags is not set* |
| Ticket trùng lặp | ≥ 9 cặp (8 %) | < 3 % | Đếm ticket chuyển *Đã hủy* với tag `duplicate` |
| Ticket Urgent + High | 82 (69 %) | ≤ 30 % | Odoo report group by Priority |
| Ticket đăng nhập tự xử lý | 0 % | ≥ 80 % số ticket đăng nhập | `python -m login_bot.stats` |

## 2. Hành động

Ưu tiên theo *ảnh hưởng ÷ công sức*. Số ticket giảm ước tính dựa trên tỷ lệ trong sample.

| # | Vấn đề (ticket) | Hành động | Loại | Người phụ trách | Thời hạn | Ước tính giảm |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Đăng nhập LMS (14) | Chạy **login bot** (đã làm, [automation.md](automation.md)) | Automation | Operating Engineer | Tuần 1 | 4 ticket tự xử lý ngay |
| A2 | Đăng nhập TMS / Ecount / Mail (7) | Thêm connector cho từng hệ thống vào bot — cùng luồng kiểm tra HR | Automation | Operating Engineer | Tuần 2–3 | +7 → tổng ~11/14 (79 %) |
| A3 | Gốc của A1 | Đề xuất team dev: **email cảnh báo trước 3 ngày** khi sắp khóa, hoặc chỉ khóa khi HR báo nghỉ việc | Sửa code | Team dev (Support đề xuất) | Đề xuất tuần 1 | Loại bỏ phần lớn ticket đăng nhập về lâu dài |
| B1 | TMS / chấm công (19) | **Gộp sự cố**: ≥ 3 ticket cùng hệ thống trong 1 giờ → 1 ticket chính mức Priority/Expedite, các ticket khác đánh dấu trùng (quy trình S05 Week 4) | Quy trình | Trưởng ca Support | Tuần 1 | ~9 ticket (10 ticket #227–#239 còn 1) |
| B2 | TMS / chấm công | Trang **thông báo sự cố** (status page / tin nhắn nhóm BU) khi TMS lỗi, để giáo viên không phải gửi ticket | Quy trình | Support + IT | Tuần 2 | Giảm ticket trong các sự cố tiếp theo |
| B3 | TMS / chấm công | Gửi team dev bằng chứng lỗi cuối tháng ("lỗi từ ngày 31", "đi đúng ca nhưng báo trễ") để tìm nguyên nhân gốc | Sửa code | Team dev | Tuần 2 | Dài hạn |
| C1 | Lead / Thanh toán (24) | Bài KB "Xử lý payment nhập sai / lead không tự chuyển trạng thái"; cho kế toán quyền tự hủy payment trong giới hạn | KB + phân quyền | Support + Kế toán | Tuần 3 | ~6 ticket (gỡ/hủy payment, chuyển trạng thái đơn giản) |
| C2 | Lead / Thanh toán | Báo team dev lỗi "đã add payment vẫn nằm ở L5A" (#225) | Sửa code | Team dev | Tuần 3 | Dài hạn |
| D1 | Enroll (20) | Bài KB "Các bước enroll + lỗi thường gặp (không tìm thấy lớp, hết slot)"; đào tạo nhanh cho BU gửi nhiều ticket (Thủ Dầu Một, Hoàng Đạo Thúy) | KB + đào tạo | Support | Tuần 3 | ~5 ticket |
| E1 | Phân loại kém (52 ticket không tag) | **Bắt buộc chọn hệ thống** (CRM/LMS/TMS…) trong form gửi ticket | Cấu hình Odoo | Admin Odoo | Tuần 1 | Không giảm ticket, nhưng report chính xác |
| E2 | Ưu tiên bị đánh quá tay (69 %) | Ưu tiên tính theo **Class of Service** (số người bị ảnh hưởng), không theo người gửi chọn | Quy trình | Trưởng ca | Tuần 1 | — |
| E3 | Ticket trùng (≥ 9 cặp) | Kiểm tra trùng khi nhận ticket (cùng người gửi + tiêu đề tương tự trong 7 ngày) → gộp | Quy trình | Support | Tuần 1 | ~9 ticket |
| E4 | Ticket từ Freshdesk mất người gửi (10) | Map lại email người gửi gốc khi chuyển tiếp | Cấu hình | Admin | Tuần 2 | — |

**Tổng ước tính giảm:** A1+A2 (11) + B1 (9) + C1 (6) + D1 (5) + E3 (9) ≈ **40 ticket (34 %)** trên quy mô sample.

## 3. Lộ trình

| Tuần | Việc |
| --- | --- |
| 1 | A1 chạy chính thức · A3 gửi đề xuất · B1, E1, E2, E3 áp dụng quy trình |
| 2 | A2 (TMS) · B2 · B3 · E4 |
| 3 | A2 (Ecount, Mail) · C1 · C2 · D1 |
| 4 | Đo lại bằng Odoo report; so với mục 1 |
| 8 | Đánh giá cuối: giữ / chỉnh / bỏ từng hành động |

## 4. Theo dõi

- Hằng tuần: report Odoo theo tag nhóm và tag `auto-*`, `python -m login_bot.stats`.
- Báo động: tỷ lệ `failed` của bot > 5 %, hoặc user trả lời "vẫn chưa đăng nhập được" sau khi bot xử lý → xem lại bot.
- Khi team dev sửa xong A3, số ticket đăng nhập phải giảm; nếu bot không còn việc thì tắt bot (automation có thể là giải pháp tạm thời).
