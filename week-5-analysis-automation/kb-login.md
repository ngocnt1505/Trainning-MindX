# KB: Không đăng nhập được LMS

| | |
| --- | --- |
| Áp dụng cho | Giáo viên, nhân sự MindX dùng LMS |
| Triệu chứng | Báo "Invalid username or password" dù chắc chắn nhập đúng mật khẩu; hoặc báo tài khoản bị khóa |
| Cập nhật | 2026-11-11 |

---

## Phần 1 — Dành cho người dùng

### Vì sao bị lỗi?

Thường gặp nhất: **tài khoản LMS tự bị khóa khi bạn không đăng nhập trong 30 ngày** (VD: nghỉ hè, giữa hai khóa dạy). Khi đó LMS vẫn báo "sai mật khẩu" dù bạn nhập đúng.

### Tự kiểm tra trước (2 phút)

1. Mở **chế độ ẩn danh** (Ctrl + Shift + N) và đăng nhập lại.
2. Kiểm tra đúng địa chỉ: `lms.mindx.edu.vn`.
3. Kiểm tra Caps Lock và bộ gõ tiếng Việt (Unikey) đang tắt.
4. Bấm **Quên mật khẩu** trên trang đăng nhập.

### Vẫn không được? Gửi ticket

Gửi email tới support với:

- **Tiêu đề** có chữ "đăng nhập" và tên hệ thống, VD: `Không đăng nhập được LMS`.
- Gửi **từ email công việc** của bạn (email đăng ký trong hệ thống nhân sự).
- Mô tả: thông báo lỗi bạn thấy, lần cuối đăng nhập được (nếu nhớ).

Ticket đúng mẫu sẽ được **xử lý tự động trong khoảng 5 phút**: nếu bạn đang làm việc tại MindX, tài khoản được mở lại và bạn nhận email đặt lại mật khẩu. Sau khi đăng nhập được, hãy **trả lời email** để team đóng ticket.

---

## Phần 2 — Dành cho team Support

### Bot đã làm gì với ticket?

Xem **tag** và **ghi chú `[LOGIN-BOT]`** trong chatter của ticket:

| Tag | Ý nghĩa | Việc của bạn |
| --- | --- | --- |
| `auto-reactivated` | HR active, tài khoản bị khóa → bot đã mở lại + gửi link đặt lại mật khẩu | Chờ user xác nhận → đóng ticket |
| `auto-password-reset` | HR active, tài khoản đang mở → bot gửi link đặt lại mật khẩu | Chờ user xác nhận → đóng ticket. Nếu user vẫn lỗi → kiểm tra log đăng nhập |
| `auto-escalated` | Bot **không** tự xử lý — lý do nằm trong ghi chú | Xử lý tay theo bảng dưới |
| chỉ `auto-processed` | Không phải lỗi đăng nhập | Xử lý như ticket bình thường |

### Xử lý tay các ca `auto-escalated`

| Lý do trong ghi chú | Cách xử lý |
| --- | --- |
| Nhân sự đã nghỉ việc | **Không mở lại.** Xác nhận với HR / quản lý trực tiếp. Nếu đúng đã nghỉ → trả lời user lịch sự và đóng ticket. Nếu HR cập nhật sai → nhờ HR sửa, rồi mở lại |
| Không tìm thấy trong HR | Hỏi user email công việc / mã nhân sự; nhân sự mới → kiểm tra HR đã nhập hồ sơ chưa |
| Chưa có tài khoản LMS | Chuyển quy trình **cấp tài khoản mới** |
| Hệ thống TMS / CRM / Ecount / Mail | Làm tay theo đúng hệ thống đó (kiểm tra HR → mở lại / đặt lại mật khẩu) |
| Tài khoản học viên / Denise | Kiểm tra tài khoản học viên trên Denise / LMS |
| Automation lỗi | HR hoặc LMS API không trả lời — xử lý tay theo Scenario 1, báo người quản lý bot |

### Quy trình tay đầy đủ (khi bot tắt)

1. Kiểm tra HR: còn làm việc? email khớp?
2. Kiểm tra tài khoản: active hay deactivated? log đăng nhập?
3. Active → gửi link đặt lại mật khẩu. Deactivated + còn làm việc → mở lại + đặt lại mật khẩu. Đã nghỉ → không mở lại, giải thích.
4. Email trả lời, chuyển *Waiting Customer*, đóng khi user xác nhận.

Chi tiết: Scenario 1 – [week-4-odoo-helpdesk/scenario-01-login.md](../week-4-odoo-helpdesk/scenario-01-login.md). Thông tin về bot: [automation.md](automation.md).
