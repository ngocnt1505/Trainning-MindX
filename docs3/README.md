# Week 4 — Ticket Handling & Professional Communication

Bài nộp Week 4: xử lý 6 scenario ticket trên **Odoo Helpdesk** theo quy trình 7 bước của MindX và Class of Service, kèm email/chat draft cho từng scenario.

- Đề bài: [week-4/overview.md](../week-4/overview.md) · [tasks.md](../week-4/tasks.md) · [architecture.md](../week-4/architecture.md) · [scenarios/](../week-4/scenarios/)
- Odoo (database trial): https://choi.odoo.com/odoo/helpdesk — xem mục [Truy cập Odoo](#truy-cập-odoo)

## Tổng quan 6 scenario

| #  | Scenario                     | Class of Service | Ticket Odoo | Bài làm | Bản ghi Odoo |
| -- | ---------------------------- | ---------------- | ----------- | ------- | ------------ |
| 01 | Không đăng nhập được LMS     | Standard         | [#6](https://choi.odoo.com/odoo/helpdesk/1/tickets/6)   | [scenario-01-login.md](scenario-01-login.md)                     | [PDF](images/s01-full.pdf) |
| 02 | LMS chậm – 15 học viên       | Priority         | [#7](https://choi.odoo.com/odoo/helpdesk/1/tickets/7)   | [scenario-02-performance.md](scenario-02-performance.md)         | [PDF](images/s02-full.pdf) |
| 03 | Hệ thống nộp bài thi sập – 53 HV | Expedite     | [#8](https://choi.odoo.com/odoo/helpdesk/1/tickets/8)   | [scenario-03-critical-bug.md](scenario-03-critical-bug.md)       | [PDF](images/s03-full.pdf) |
| 04 | Đề xuất tính năng            | Standard         | [#9](https://choi.odoo.com/odoo/helpdesk/1/tickets/9)   | [scenario-04-feature-request.md](scenario-04-feature-request.md) | [PDF](images/s04-full.pdf) |
| 05 | Video không phát – 12 HV     | Priority         | [#10](https://choi.odoo.com/odoo/helpdesk/1/tickets/10) (gộp [#11](https://choi.odoo.com/odoo/helpdesk/1/tickets/11), [#12](https://choi.odoo.com/odoo/helpdesk/1/tickets/12)) | [scenario-05-multi-user.md](scenario-05-multi-user.md) | [chính](images/s05-main.pdf) · [phụ](images/s05-duplicates.pdf) |
| 06 | Báo cáo tuyển sinh cần gấp   | Fixed Deadline   | [#13](https://choi.odoo.com/odoo/helpdesk/1/tickets/13) | [scenario-06-deadline.md](scenario-06-deadline.md)               | [PDF](images/s06-full.pdf) |

Export danh sách ticket từ Odoo (03/11/2026): [exports/tickets.xlsx](exports/tickets.xlsx)

| ID    | Mức độ ưu tiên (Odoo)  | Tiêu đề                                                                  | Phân công cho     | Giai đoạn |
| ----- | ---------------------- | ------------------------------------------------------------------------ | ----------------- | --------- |
| 00006 | Ưu tiên trung bình (1 sao) | LMS login failed - "Invalid username or password" - Teacher Nguyễn Văn A | Nguyễn Thùy Ngọc | Đã xử lý |
| 00007 | Mức độ ưu tiên cao (2 sao) | LMS Performance Issue - Class WEB101-HN-2024 (15 users)              | Nguyễn Thùy Ngọc | Đã xử lý |
| 00008 | Khẩn cấp (3 sao)       | EXPEDITE - Exam submission system down - 53 students / 3 classes         | Nguyễn Thùy Ngọc | Đã xử lý |
| 00009 | Ưu tiên trung bình (1 sao) | Feature request - Weekly auto PDF progress report emailed to parents | Nguyễn Thùy Ngọc | Đã xử lý |
| 00010 | Mức độ ưu tiên cao (2 sao) | Video playback issue - Lesson 3 (JS-ADV-HN-2412) - 12 users          | Nguyễn Thùy Ngọc | Đã xử lý |
| 00011 | Mức độ ưu tiên thấp (0 sao) | Video bài 3 không xem được - HV Trần Minh Khoa _(duplicate của #10)_ | —               | Đã hủy |
| 00012 | Mức độ ưu tiên thấp (0 sao) | Lớp JS-ADV-HN-2412 - video Lesson 3 không chạy - GV Phạm Thu Trang _(duplicate của #10)_ | — | Đã hủy |
| 00013 | Mức độ ưu tiên cao (2 sao) | Fixed Deadline - Enrollment report for Director (Due 09:00 05/11)    | Nguyễn Thùy Ngọc | Đã xử lý |

File export không có cột Thẻ; thẻ của từng ticket xem trong PDF bản ghi.

Báo cáo mô phỏng bàn giao ở S06 (số liệu giả lập): [reports/](reports/README.md)

### Mỗi file scenario gồm

1. **Phân loại** — Class of Service, lý do, vì sao không phải class khác
2. **Ticket Odoo** — tiêu đề, thẻ, mức ưu tiên, khách hàng, link
3. **Chẩn đoán / điều tra** — kết quả kiểm tra (giả định) và quyết định
4. **Timeline** theo 7 bước, có giờ
5. **Email / chat drafts** — ACK, cập nhật / escalation, giải quyết / follow-up
6. **Trend analysis** và **reflection**

## Cách đọc bản ghi Odoo

- Mỗi bước trong 7 bước là **1 ghi chú** trong chatter, bắt đầu bằng giờ của tình huống, ví dụ `[09:05] RECEPTION – …`. Giờ bên cạnh tên người trong chatter là giờ thực hiện thật trên Odoo, nên **đọc timeline theo giờ trong ngoặc `[...]`**.
- Ghi chú chứa nguyên văn email/chat đã gửi, để mọi giao tiếp đều được lưu trên ticket.
- Mỗi lần chuyển giai đoạn, Odoo tự ghi lại trong chatter (VD: `Escalated → Waiting Customer`).
- Email khảo sát hài lòng khi ticket chuyển sang *Đã xử lý* là email tự động của Odoo; dấu ❌ đỏ nghĩa là gửi không thành công vì khách hàng dùng email giả lập (xem bên dưới).

## Cấu hình Odoo đã dùng

| Hạng mục          | Cấu hình                                                                                     |
| ----------------- | -------------------------------------------------------------------------------------------- |
| Class of Service  | Thẻ `cos-standard`, `cos-priority`, `cos-expedite`, `cos-fixed-deadline`                      |
| Loại ticket       | Bản trial không có menu *Ticket Type*, nên dùng thẻ `type-technical-support`, `type-incident`, `type-feature-request`, `type-report-request` |
| Mức ưu tiên       | 1 sao = Standard · 2 sao = Priority / Fixed Deadline · 3 sao = Expedite |
| Giai đoạn         | Mới → Đang thực hiện → **Escalated** → **Waiting Customer** → Tạm dừng → Đã xử lý → Đã hủy (thêm *Escalated* và *Waiting Customer*) |
| Gộp ticket (S05)  | Ticket chính có ghi chú `Related: #11, #12`; ticket phụ có thẻ `duplicate`, ghi chú `Duplicate of #10` và chuyển sang *Đã hủy* |

### Nguyên tắc an toàn dữ liệu

- Đây là môi trường demo: **không liên hệ người dùng thật**. Khách hàng trong Odoo dùng email giả lập `@example.com` thay cho địa chỉ `@mindx.edu.vn` trong đề.
- Email được ghi lại bằng **Ghi chú** (log note nội bộ), không dùng *Gửi tin*, để Odoo không gửi email ra ngoài.
- Không có dữ liệu cá nhân thật trong ticket, ảnh chụp hay file export.

## Trạng thái minh chứng

| Scenario | Thao tác thật trên Odoo                                       | Chỉ mô phỏng trong tài liệu (chưa xác minh trên Odoo)            |
| -------- | ------------------------------------------------------------- | ---------------------------------------------------------------- |
| 01       | Ticket #6, nhánh B (tài khoản bị vô hiệu hoá, vẫn còn làm)    | Nhánh A, C; kết quả tra cứu tài khoản / log đăng nhập            |
| 02       | Ticket #7: ghi chú theo 7 bước, chuyển giai đoạn              | Số liệu monitoring/log; trao đổi với Dev                         |
| 03       | Ticket #8: ghi chú theo 7 bước, chuyển giai đoạn              | Trao đổi Manager/CXO/Dev; số liệu sự cố                          |
| 04       | Ticket #9                                                     | Phản hồi của Product, mã backlog `PRD-REQ-0142`                  |
| 05       | Ticket chính #10 (nhánh A), 2 ticket phụ #11, #12 gộp vào #10 | Nhánh B, C; số liệu storage/CDN                                  |
| 06       | Ticket #13                                                    | Dữ liệu CRM và file báo cáo ([reports/](reports/README.md), số liệu giả lập) |

Mọi email/chat chỉ được ghi lại dưới dạng ghi chú nội bộ, không gửi thật cho ai (xem *Nguyên tắc an toàn dữ liệu*).

## Truy cập Odoo

Database trial cần đăng nhập mới xem được ticket. Mentor cần được mời làm người dùng của database để mở các link ticket; nếu không truy cập được (hoặc trial đã hết hạn sau 14 ngày), các file PDF trong [images/](images/) và file [export](exports/tickets.xlsx) là bản ghi đầy đủ của từng ticket.

## Đối chiếu Acceptance Criteria

| Tiêu chí ([overview.md](../week-4/overview.md))                    | Bằng chứng                                                                                   |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| Hoàn thành 6 scenario (01-06)                                      | Bảng tổng quan ở trên                                                                        |
| Áp dụng đúng quy trình 7 bước                                      | Mục *Timeline* trong mỗi file + ghi chú theo bước trong Odoo                                  |
| Phân loại Class of Service chính xác                               | Mục *Phân loại* (có lý do và vì sao không phải class khác) + thẻ `cos-*`                     |
| Xác nhận và phản hồi ban đầu kịp thời (không hứa ETA cố định)      | Email ACK trong mục tiêu thời gian của từng class; hẹn **mốc cập nhật**, không hứa giờ sửa xong |
| Email draft cho từng scenario (ACK / update / resolution)          | Mục *Email / Chat drafts* trong mỗi file                                                     |
| Giọng văn chuyên nghiệp, rõ ràng                                   | Viết theo đúng đối tượng: khách hàng / Dev (kỹ thuật) / Manager (tác động, phương án, quyết định cần) |
| Tạo và cập nhật ticket đúng                                        | PDF bản ghi Odoo: field đầy đủ, chuyển giai đoạn theo tiến trình                             |
| Dùng thẻ và phân loại đúng                                         | Thẻ `cos-*`, `type-*` và thẻ nội dung trên từng ticket                                       |
| Tài liệu theo template                                             | Cấu trúc thống nhất cho cả 6 file scenario                                                   |

## Chỉnh sửa sau review lần 1

Theo nhận xét của mentor trong issue #2 (review commit `1642e0a`):

| Góp ý                                         | Đã sửa                                                                                   |
| --------------------------------------------- | ---------------------------------------------------------------------------------------- |
| S02/S03: tiêu đề email cho người dùng có nhãn nội bộ `PRIORITY` / `EXPEDITE` | Bỏ nhãn khỏi tiêu đề và nội dung email gửi CXO/giảng viên; chỉ giữ trong tin nhắn cho Dev và email nội bộ cho Manager |
| S04: email chưa hẹn mốc cập nhật tiếp theo    | ACK hẹn cập nhật trước 12:00 05/11; email cập nhật hẹn 10/11 (hỏi về workaround) và trước 17:00 20/11 (kết quả kỳ lập kế hoạch) |
| S04: Standard nhưng 0 sao                     | Đổi thành 1 sao, bỏ quy ước "0 sao = feature request"                                   |
| S05: ACK đầu tiên lúc 20:10, 25 phút sau báo cáo đầu tiên | ACK riêng cho CXO lúc 19:50 và học viên #11 lúc 19:58; email 20:10 là cập nhật chung sau khi gom ticket |
| S06: tạo ticket lúc 14:20, quá 15 phút         | Tạo ticket lúc 14:10                                                                     |
| S06: chưa có tệp báo cáo kiểm tra được        | Thêm [reports/](reports/README.md) với số liệu giả lập; email 5.5/5.6 dẫn tới tệp này    |
| Thiếu minh chứng Odoo                         | Thêm bảng *Trạng thái minh chứng*; Bổ sung PDF S04, S05 (ticket chính chụp lại + ticket phụ), S06 và file export (kèm bảng tóm tắt ở trên) |

## Làm việc với AI

- **AI (Claude Code)** hướng dẫn cấu hình Odoo, soạn nháp nội dung các file scenario (phân loại, timeline, email/chat) và các ghi chú để dán vào Odoo, rồi rà soát bản chụp từng ticket để chỉ ra chỗ còn thiếu (VD: ghi chú chỉ ghi "+ email" mà chưa có nội dung, ticket chưa phân công, thiếu ghi chú quyết định của Manager).
- **Tôi** thực hiện toàn bộ thao tác trên Odoo (tạo database, cấu hình thẻ/giai đoạn, tạo ticket, ghi chú, chuyển giai đoạn, chụp bản ghi), sửa các chỗ được chỉ ra và rà soát nội dung trước khi nộp.
