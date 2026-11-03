# Scenario 04 — Feature Request: báo cáo tiến độ PDF tự động gửi phụ huynh

## 1. Phân loại

| Câu hỏi                                  | Trả lời                                                                 |
| ---------------------------------------- | ----------------------------------------------------------------------- |
| Yêu cầu support hay feedback sản phẩm?   | **Feedback sản phẩm (feature request)** — không có lỗi, hệ thống vẫn hoạt động đúng; đây là đề xuất tính năng mới ngoài scope hiện tại |
| Ai xử lý chính?                          | **Product** đánh giá và quyết định; Support là đầu mối tiếp nhận, chuyển yêu cầu và cập nhật cho khách hàng |
| Cách phản hồi để quản lý kỳ vọng?        | Cảm ơn, giải thích quy trình đánh giá của Product, **không hứa sẽ làm / không hứa timeline**, đưa workaround để khách vẫn "engaged" |

- Class of Service: **Standard**
- Lý do: không có người dùng nào bị chặn công việc, không có thời hạn cứng; là đề xuất cải tiến.
- Vì sao không phải class khác: không phải Priority/Expedite vì không có sự cố; không phải Fixed Deadline vì khách không đưa ra mốc thời gian bắt buộc.

## 2. Ticket Odoo

- Link: https://choi.odoo.com/odoo/helpdesk/1/tickets/9
- Tiêu đề: `Feature request - Weekly auto PDF progress report emailed to parents`
- Thẻ: `cos-standard`, `type-feature-request`, `product`, `report`, `parents`
- Mức ưu tiên: 1 sao (Standard)
- Khách hàng: CXO Cơ sở Nguyễn Chí Thanh — `cxo.nct@example.com` (email giả lập)
- Phân công: Nguyễn Thùy Ngọc
- Tham chiếu Product backlog: `PRD-REQ-0142` (giả định)

- Bản ghi đầy đủ (form + chatter): [images/s04-full.pdf](images/s04-full.pdf)

## 3. Timeline

| Thời điểm      | Bước (7-step)     | Hành động                                                                 | Ghi chú / Quyết định                          |
| -------------- | ----------------- | ------------------------------------------------------------------------- | --------------------------------------------- |
| Ngày 1 (03/11) – 13:00 | —                 | Nhận email đề xuất từ CXO Cơ sở Nguyễn Chí Thanh                           |                                               |
| Ngày 1 (03/11) – 13:10 | 1. Reception      | Tạo ticket, phân loại Feature Request / Standard                           | Không phải lỗi → chủ quản là Product          |
| Ngày 1 (03/11) – 13:25 | 2. Response       | Gửi ACK: cảm ơn, giải thích quy trình, không hứa timeline, gợi ý workaround; hẹn cập nhật trạng thái trước 12:00 thứ Năm 05/11 | Trong mục tiêu < 30 phút; hẹn mốc cập nhật, không hẹn ngày triển khai |
| Ngày 1 (03/11) – 13:40 | 3. Diagnosis      | Kiểm tra LMS hiện có: đã có export báo cáo tiến độ lớp (Excel), chưa có PDF tự động gửi phụ huynh | Xác nhận ngoài scope hiện tại |
| Ngày 1 (03/11) – 13:45 | 4. Resolution     | Chuyển yêu cầu sang Product kèm ngữ cảnh, nhờ phản hồi trước 10:00 05/11; chuyển ticket sang Tạm dừng | Chờ Product đánh giá |
| Ngày 3 (05/11) – 10:00 | 5. Communication  | Product phản hồi: ghi nhận vào backlog `PRD-REQ-0142`, đánh giá trong kỳ lập kế hoạch ngày 18/11 (giả định); cần lưu ý PII phụ huynh | Chưa có cam kết triển khai |
| Ngày 3 (05/11) – 10:15 | 5. Communication  | Gửi email cập nhật trạng thái cho CXO; hẹn hỏi lại về workaround thứ Ba 10/11 và cập nhật kết quả kỳ lập kế hoạch trước 17:00 thứ Sáu 20/11 | Đúng mốc đã hẹn trong ACK |
| Ngày 8 (10/11) – 09:00 | 6. Follow-up      | Hỏi CXO workaround có dùng được không; CXO xác nhận đang dùng export Excel hàng tuần | Đóng ticket Support; mốc 20/11 vẫn giữ, theo dõi qua `PRD-REQ-0142` |
| Ngày 8 (10/11) – 09:10 | 7. Trend Analysis | Ghi nhận nhu cầu "báo cáo tự động cho phụ huynh" để tổng hợp các yêu cầu tương tự | Đã xử lý                                      |

## 4. Email / Chat drafts

### 4.1 ACK (Ngày 1 – 03/11, 13:25)

```
Subject: RE: Đề xuất tính năng - Có thể thêm tính năng này không? - Ticket #9

Chào anh/chị,

Cảm ơn anh/chị đã dành thời gian gửi đề xuất về tính năng tự động tạo báo cáo
tiến độ học viên dạng PDF và gửi email cho phụ huynh hàng tuần. Team rất trân
trọng góp ý từ người dùng LMS lâu năm như anh/chị.

Đây là đề xuất tính năng mới, nên team Support sẽ chuyển đến team Product để
xem xét. Team Product đánh giá các đề xuất dựa trên nhu cầu của người dùng, mức
độ ảnh hưởng và lộ trình phát triển chung của sản phẩm, vì vậy hiện tại team
chưa thể xác nhận tính năng có được triển khai hay thời điểm triển khai.

Team sẽ gửi anh/chị cập nhật trạng thái trước 12:00 thứ Năm 05/11, kể cả khi
team Product chưa có quyết định.

Trong lúc chờ, anh/chị có thể dùng chức năng sẵn có của LMS để tiết kiệm thời gian:
- Vào lớp học → Báo cáo → "Tiến độ học viên" → Xuất file Excel
- File này có thể lọc theo từng học viên để gửi phụ huynh hàng tuần
Nếu cần, team có thể gửi anh/chị hướng dẫn chi tiết từng bước.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #9
```

### 4.2 Chuyển yêu cầu cho Product (Ngày 1 – 03/11, 13:45, nội bộ)

```
Subject: [Feature Request] Báo cáo tiến độ học viên PDF tự động gửi phụ huynh hàng tuần - Ticket #9

Chào team Product,

Support nhận được đề xuất tính năng từ CXO Cơ sở Nguyễn Chí Thanh (đã dùng LMS
6 tháng):

Yêu cầu: tự động tạo báo cáo tiến độ học viên dạng PDF và gửi email cho phụ
huynh mỗi tuần.

Lợi ích theo khách hàng: tiết kiệm nhiều thời gian cho team CXO (hiện đang làm
báo cáo thủ công).

Hiện trạng LMS: đã có export "Tiến độ học viên" dạng Excel theo lớp; chưa có
xuất PDF theo từng học viên và chưa có gửi email tự động cho phụ huynh.

Lưu ý cần đánh giá:
- Dữ liệu cá nhân phụ huynh/học viên (PII) khi gửi email tự động
- Nguồn email phụ huynh (có sẵn trong hệ thống hay chưa)

Nhờ team ghi nhận vào backlog và phản hồi giúp Support trạng thái trước 10:00
thứ Năm 05/11 (Support đã hẹn cập nhật khách hàng trước 12:00 cùng ngày). Support
đã thông báo khách hàng là chưa có cam kết timeline.

Cảm ơn team,
Nguyễn Thùy Ngọc – Support
```

### 4.3 Cập nhật trạng thái (Ngày 3 – 05/11, 10:15)

```
Subject: RE: Đề xuất tính năng - Cập nhật trạng thái - Ticket #9

Chào anh/chị,

Team cập nhật về đề xuất tính năng báo cáo tiến độ PDF gửi phụ huynh:

- Team Product đã ghi nhận đề xuất vào danh sách yêu cầu (mã PRD-REQ-0142).
- Đề xuất sẽ được xem xét trong kỳ lập kế hoạch sản phẩm tiếp theo (ngày
  18/11), cùng với các yêu cầu tương tự từ các cơ sở khác.
- Hiện chưa có quyết định triển khai và chưa có thời gian dự kiến.

Các mốc tiếp theo:
- Thứ Ba 10/11: team liên hệ lại để hỏi cách xuất báo cáo Excel có đáp ứng tạm
  thời nhu cầu của team anh/chị không
- Trước 17:00 thứ Sáu 20/11: team cập nhật kết quả của kỳ lập kế hoạch, dù đề
  xuất được chọn hay chưa

Trong thời gian này, anh/chị có cần team hướng dẫn chi tiết cách xuất báo cáo
tiến độ Excel hàng tuần không ạ?

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #9
```

### 4.4 Follow-up & đóng ticket (Ngày 8 – 10/11, 09:00)

```
Subject: RE: Đề xuất tính năng - Ticket #9 - Follow-up

Chào anh/chị,

Cảm ơn anh/chị đã phản hồi rằng cách xuất báo cáo tiến độ Excel hàng tuần đang
giúp được team anh/chị trong thời gian chờ. Team xin phép đóng ticket hỗ trợ
này. Đề xuất của anh/chị vẫn được team Product theo dõi với mã PRD-REQ-0142, và
team vẫn giữ hẹn gửi anh/chị kết quả kỳ lập kế hoạch trước 17:00 thứ Sáu 20/11.

Nếu anh/chị có thêm góp ý cho LMS, anh/chị cứ gửi về support@mindx.edu.vn.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #9
```

## 5. Reflection

- Làm tốt: phân biệt rõ feedback sản phẩm với yêu cầu support; không hứa điều Support không kiểm soát (quyết định và timeline thuộc Product); vẫn đưa workaround để khách được hỗ trợ ngay.
- Khó: viết phản hồi "chưa thể cam kết" mà khách vẫn thấy được trân trọng.
- Lần sau: gắn mã backlog Product vào ticket ngay khi chuyển để khách và team cùng tra cứu được trạng thái.
