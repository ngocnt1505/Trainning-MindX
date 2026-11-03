# Scenario 02 — Vấn đề Performance

## 1. Phân loại

- Class of Service: **Priority**
- Lý do: 15 học viên + 1 CXO bị ảnh hưởng (trong khoảng 5–25), lỗi **đang chặn công việc** (học viên không nộp được bài) và **đang diễn ra** trong giờ học.
- Vì sao không phải class khác: không phải Standard vì nhiều người dùng và đang chặn lớp học; không phải Expedite vì < 25 người dùng và chỉ 1 lớp bị ảnh hưởng, các lớp khác bình thường (không phải sự cố toàn hệ thống).
- Lưu ý: ưu tiên dựa trên **số người bị chặn + thời gian tác động**, không phải vì email ghi "Khẩn cấp".

## 2. Ticket Odoo

- Link: https://choi.odoo.com/odoo/helpdesk/1/tickets/7
- Tiêu đề: `LMS Performance Issue - Class WEB101-HN-2024 (15 users)`
- Thẻ: `cos-priority`, `type-incident`, `performance`, `lms`, `web101`
- Mức ưu tiên: 2 sao (High)
- Khách hàng: Nguyễn Thị Hà (CXO) — `coordinator.ha@example.com` (email giả lập)
- Phân công: Nguyễn Thùy Ngọc
- Người dùng bị ảnh hưởng: 15 học viên + 1 CXO

- Bản ghi đầy đủ (form + chatter): [images/s02-full.pdf](images/s02-full.pdf)

## 3. Điều tra

### Kết quả kiểm tra (giả định)

| Nguồn                 | Phát hiện                                                                 |
| --------------------- | ------------------------------------------------------------------------- |
| Azure App Insights    | Response time tăng đột biến từ **14:00**: 2s → 35s                        |
| Application logs      | Nhiều timeout errors, slow queries trên trang bài tập của lớp             |
| System health         | Database connection pool gần đầy (~95%)                                   |
| Phạm vi               | **Chỉ lớp WEB101-HN-2024**, các lớp khác bình thường → cục bộ, không toàn hệ thống |

### Quyết định escalation

| Câu hỏi                                   | Trả lời                                   |
| ----------------------------------------- | ----------------------------------------- |
| Có phải vấn đề phía người dùng?           | Không — 15 user cùng lúc, monitoring cũng ghi nhận |
| Có giải pháp đã biết trong KB?            | Không                                     |
| Nguyên nhân thuộc database / cần thay đổi code-config? | Có → **ngoài phạm vi Support** |
| **Kết luận**                              | **Escalate Dev Team**, kèm dữ liệu điều tra |

Nguyên tắc: điều tra trước (10 phút), escalate **có dữ liệu** — không escalate kiểu "LMS chậm, xin sửa".

## 4. Timeline

| Giờ   | Bước (7-step)     | Hành động                                                              | Ghi chú / Quyết định                     |
| ----- | ----------------- | ---------------------------------------------------------------------- | ---------------------------------------- |
| 14:15 | —                 | Nhận email từ CXO Nguyễn Thị Hà                                        | Lớp đang diễn ra                         |
| 14:18 | 1. Reception      | Phân loại Priority (< 5 phút)                                          | 15 user bị chặn, đang diễn ra            |
| 14:22 | 1. Reception      | Tạo ticket, gắn thẻ, phân công                                         | < 10 phút                                |
| 14:25 | 2. Response       | Gửi ACK, hẹn cập nhật trước 14:40                                      | < 15 phút từ khi nhận                    |
| 14:35 | 3. Diagnosis      | Kiểm tra App Insights, logs, system health                             | Spike từ 14:00, DB pool ~95%, chỉ WEB101 |
| 14:37 | 3. Diagnosis      | Escalate Dev Team qua Teams; chuyển ticket sang Escalated              | Vấn đề database, ngoài phạm vi Support   |
| 14:40 | 5. Communication  | Cập nhật CXO: phát hiện + đã escalate + workaround nộp bài qua email   | Đúng hẹn 14:40                           |
| 14:55 | 5. Communication  | Dev xác định nguyên nhân: truy vấn trang bài nộp lớp WEB101 thiếu index, nhiều học viên nộp cùng lúc làm đầy connection pool; đang áp dụng fix. Cập nhật CXO | Cập nhật mỗi 15 phút |
| 15:10 | 4. Resolution     | Dev deploy hotfix (thêm index + giải phóng các truy vấn treo). Tự kiểm tra: response time về ~2s, mở trang lớp WEB101 bình thường | Tự xác minh trước khi báo |
| 15:15 | 6. Follow-up      | Báo CXO đã xử lý, nhờ xác nhận với học viên; chuyển Waiting Customer   |                                          |
| 15:25 | 6. Follow-up      | CXO xác nhận học viên tải trang và nộp bài bình thường                 |                                          |
| 15:45 | 7. Trend Analysis | Theo dõi 30 phút không tái phát → đóng ticket; ghi nguyên nhân gốc, đề xuất KB + alert | Đã xử lý            |

## 5. Email / Chat drafts

### 5.1 ACK (14:25)

```
Subject: RE: Khẩn cấp - Lớp học đang gặp tình trạng chậm nghiêm trọng - PRIORITY Ticket #7

Chào chị Hà,

Team Support đã ghi nhận tình trạng 15 học viên lớp WEB101-HN-2024 tải trang LMS
rất chậm và không nộp được bài trong lúc lớp đang diễn ra. Ticket đã được xếp mức
PRIORITY và team đang kiểm tra hệ thống ngay.

Team sẽ cập nhật kết quả kiểm tra cho chị trước 14:40.

Trong lúc chờ, chị giúp team:
- Ghi lại các trang cụ thể đang bị chậm (VD: trang bài tập, trang nộp bài) và
  thời điểm học viên bắt đầu gặp lỗi
- Nhờ 1-2 học viên thử mở LMS bằng cửa sổ ẩn danh (Incognito) và báo lại kết quả
- Nhắc học viên lưu bài làm trên máy, chưa cần nộp lại liên tục để tránh mất bài

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #7
```

### 5.2 Escalation Dev Team (14:37, Teams)

```
@dev-team 🔴 PRIORITY – Vấn đề Performance LMS

Ticket: #7
Tác động: 15 học viên lớp WEB101-HN-2024 bị chặn, lớp học đang diễn ra
Triệu chứng:
- Thời gian tải trang 30+ giây (một số trang > 1 phút)
- Học viên không nộp được bài tập
- Chỉ lớp WEB101-HN-2024 bị ảnh hưởng, các lớp khác bình thường

Kết quả điều tra sơ bộ:
- App Insights: response time tăng từ 2s → 35s, bắt đầu từ 14:00 (đính kèm screenshot)
- Logs: nhiều timeout + slow query trên trang bài tập của lớp
- System health: DB connection pool ~95%

Monitoring: App Insights → LMS-Prod → Performance, filter 13:45–14:35 (screenshot đính kèm)
Logs (trích đoạn, giả định):
  14:02:11 WARN  SQL query took 28431 ms – GET /classes/WEB101-HN-2024/assignments
  14:05:47 ERROR Timeout acquiring DB connection (pool 95/100)
  14:06:02 ERROR 504 Gateway Timeout – POST /assignments/submit

Cần: xác định nguyên nhân gốc + giải pháp tạm thời để lớp tiếp tục học
Timeline: Support cập nhật CXO mỗi 15 phút, nhờ team báo tiến độ trước 14:50
```

### 5.3 Cập nhật điều tra (14:40)

```
Subject: RE: Khẩn cấp - Lớp học đang gặp tình trạng chậm - PRIORITY Ticket #7 - Cập nhật

Chào chị Hà,

Team cập nhật tình hình như sau:
- Hệ thống ghi nhận thời gian phản hồi của LMS tăng mạnh từ 14:00, chỉ ảnh hưởng
  lớp WEB101-HN-2024, các lớp khác vẫn hoạt động bình thường.
- Nguyên nhân liên quan đến cơ sở dữ liệu nên team đã chuyển ngay cho đội kỹ
  thuật (Dev Team) để xử lý.

Phương án tạm thời để lớp không bị gián đoạn:
- Học viên gửi bài tập qua email cho giảng viên, team sẽ phối hợp ghi nhận lại
  bài nộp trên LMS sau khi hệ thống ổn định
- Giảng viên có thể chuyển sang phần giảng/thực hành không cần LMS trong lúc chờ

Team sẽ cập nhật tiếp cho chị trước 14:55.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #7
```

### 5.4 Cập nhật tiến độ (14:55)

```
Subject: RE: ... - PRIORITY Ticket #7 - Cập nhật 2

Chào chị Hà,

Đội kỹ thuật đã xác định được nguyên nhân và đang áp dụng bản sửa. Team sẽ tự
kiểm tra lại sau khi bản sửa hoàn tất và cập nhật cho chị trước 15:15.

Trong lúc này, học viên vẫn tiếp tục dùng phương án gửi bài qua email.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #7
```

### 5.5 Đã xử lý — nhờ xác nhận (15:15)

```
Subject: RE: ... - PRIORITY Ticket #7 - Đã xử lý

Chào chị Hà,

Đội kỹ thuật đã hoàn tất bản sửa lúc 15:10. Team đã tự kiểm tra: thời gian tải
trang của lớp WEB101-HN-2024 đã trở lại bình thường (khoảng 2 giây).

Chị giúp team nhờ 2-3 học viên thử tải trang và nộp bài, rồi phản hồi lại kết quả
cho team nhé. Các bài đã gửi qua email, chị gửi danh sách để team hỗ trợ ghi nhận
lên LMS.

Team sẽ tiếp tục theo dõi hệ thống thêm 30 phút để đảm bảo lỗi không tái diễn.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #7
```

### 5.6 Follow-up & đóng ticket (15:45)

```
Subject: RE: ... - PRIORITY Ticket #7 - Hoàn tất

Chào chị Hà,

Cảm ơn chị đã xác nhận học viên lớp WEB101-HN-2024 đã tải trang và nộp bài bình
thường. Sau 30 phút theo dõi, hệ thống ổn định và không ghi nhận lỗi tái diễn,
team xin phép đóng Ticket #7.

Nguyên nhân: một truy vấn dữ liệu của trang bài nộp bị chậm khi nhiều học viên
nộp bài cùng lúc. Đội kỹ thuật đã tối ưu lại để tránh lặp lại.

Nếu chị gặp lại tình trạng tương tự, chị chỉ cần trả lời email này.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #7
```

## 6. Trend Analysis

- Nguyên nhân gốc: truy vấn trang bài nộp thiếu index → khi nhiều học viên nộp bài cùng lúc, connection pool bị đầy.
- Đề xuất Dev: thêm alert khi DB connection pool > 80% để phát hiện sớm trước khi người dùng báo.
- Thêm bài KB: "LMS chậm ở 1 lớp — checklist điều tra (App Insights / logs / connection pool) và mẫu escalation".

## 7. Reflection

- Làm tốt: phân loại có lý do (số user + đang chặn lớp), điều tra 10 phút rồi mới escalate kèm dữ liệu; cập nhật CXO đúng các mốc đã hẹn.
- Khó: phải giữ CXO yên tâm trong khi chưa biết nguyên nhân → dùng mốc cập nhật cố định + workaround nộp bài qua email.
- Lần sau: chuẩn bị sẵn template escalation và checklist điều tra để rút ngắn thời gian từ lúc nhận đến lúc escalate.
