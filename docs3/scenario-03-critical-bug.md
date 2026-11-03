# Scenario 03 — Lỗi nghiêm trọng: hệ thống nộp bài thi bị sập

## 1. Phân loại

- Class of Service: **Expedite**
- Tiêu chí Expedite đã đáp ứng:
  - ✅ > 25 người dùng bị ảnh hưởng: 53 học viên (WEB102-HN 20 + DATA101-SG 18 + MOBILE201-HN 15)
  - ✅ Chức năng kinh doanh quan trọng: nộp bài **thi cuối kỳ**
  - ✅ Hệ thống lỗi hoàn toàn: 100% lượt nộp bài thất bại
  - ✅ Nhiều stakeholders: CXO nhiều cơ sở + Manager vận hành
- Vì sao không phải class khác: không phải Priority vì > 25 user và nhiều lớp/cơ sở cùng lỗi (sự cố toàn hệ thống); không xếp Fixed Deadline vì mức độ nghiêm trọng đã đủ để kích hoạt giao thức khẩn cấp ngay.
- Hành động: **giao thức khẩn cấp** — báo Dev trong < 5 phút, điều tra song song, cập nhật stakeholders mỗi 15 phút.

## 2. Ticket Odoo

- Link: https://choi.odoo.com/odoo/helpdesk/1/tickets/8
- Tiêu đề: `EXPEDITE - Exam submission system down - 53 students / 3 classes`
- Thẻ: `cos-expedite`, `type-incident`, `exam`, `submission`, `outage`
- Mức ưu tiên: 3 sao (Urgent)
- Khách hàng: Lê Ngọc A (CXO Khối 18+ Cơ sở Nguyễn Chí Thanh) — `cxo.ngoc.a@example.com` (email giả lập)
- Phân công: Nguyễn Thùy Ngọc
- Tickets liên quan: các ticket cùng lỗi từ CXO cơ sở khác được gộp vào ticket này (giả định)

- Bản ghi đầy đủ (form + chatter): [images/s03-full.pdf](images/s03-full.pdf)

## 3. Phân vai khi xử lý sự cố

| Vai trò              | Người                    | Việc                                              |
| -------------------- | ------------------------ | ------------------------------------------------- |
| Điều phối + giao tiếp | Support (Ngọc)           | Ticket, cập nhật CXO/Manager mỗi 15 phút, xác minh sau fix |
| Xử lý kỹ thuật        | Senior Engineer + Dev    | Tìm nguyên nhân, rollback/fix                     |
| Hạ tầng               | DevOps                   | Deploy lại, theo dõi database                     |
| Quyết định kinh doanh | Manager vận hành         | Gia hạn thời gian thi, thông báo học viên         |

Không tự xử lý một mình: Support giữ vai trò điều phối và giao tiếp, engineer xử lý kỹ thuật.

## 4. Thông tin thu thập (giả định)

| Nguồn              | Phát hiện                                                        |
| ------------------ | ---------------------------------------------------------------- |
| Lỗi người dùng     | "System error - please contact administrator", 100% failure rate |
| Thời điểm bắt đầu  | ~10:00 (30 phút trước khi nhận ticket)                           |
| Azure App Insights | Exception spike, database connection errors từ 10:00             |
| Application logs   | Database timeout, không lưu được submissions                     |
| Thay đổi gần nhất  | Bản release mới được deploy lúc 09:55                            |

Kết luận: sự cố toàn hệ thống, trùng thời điểm với bản release 09:55 → workaround nhanh nhất là **revert bản release, deploy lại để database tự kết nối lại**.

## 5. Timeline

| Giờ   | Bước (7-step)     | Hành động                                                                  | Ghi chú / Quyết định                    |
| ----- | ----------------- | -------------------------------------------------------------------------- | --------------------------------------- |
| 10:28 | —                 | Nhận email KHẨN CẤP từ CXO Lê Ngọc A; Manager vận hành ping trên Teams     |                                         |
| 10:30 | 1. Reception      | Nhận diện Expedite (< 2 phút)                                              | 53 HV, bài thi, 100% lỗi, nhiều stakeholder |
| 10:31 | 2. Response       | Trả lời Manager trên Teams                                                 | Song song                               |
| 10:32 | 2. Response       | Gửi ACK cho CXO                                                            | Song song                               |
| 10:33 | 3. Diagnosis      | Ping Dev/Senior/DevOps ngay; tạo ticket Expedite, chuyển Escalated          | < 5 phút từ khi nhận                    |
| 10:40 | 3. Diagnosis      | Thu thập thông tin cùng engineer: App Insights, logs, release gần nhất      | < 10 phút; nghi do release 09:55        |
| 10:42 | 3. Diagnosis      | Gửi escalation đầy đủ cho Dev Team                                         | < 15 phút                               |
| 10:45 | 5. Communication  | Cập nhật Manager (phương án + đề xuất) và CXO (workaround)                 | Cập nhật #1                             |
| 10:50 | 4. Resolution     | Manager duyệt phương án A (rollback) + gia hạn thời gian thi; Dev bắt đầu rollback |                                  |
| 11:00 | 5. Communication  | Cập nhật #2 cho Manager + CXO: đang rollback                               | Đúng nhịp 15 phút                       |
| 11:05 | 4. Resolution     | Dev hoàn tất rollback, database kết nối lại                                |                                         |
| 11:05–11:15 | 4. Resolution | Tự xác minh: nộp bài thử bằng tài khoản test ở 3 lớp, App Insights error rate về 0% | Chưa thông báo khi chưa tự kiểm tra |
| 11:15 | 6. Follow-up      | Thông báo đã khôi phục cho Manager + CXO, nhờ CXO xác nhận HV nộp được bài  | Chuyển Waiting Customer                 |
| 11:45 | 6. Follow-up      | Theo dõi 30 phút ổn định; CXO xác nhận HV đã nộp bài                       |                                         |
| 11:50 | 7. Trend Analysis | Ghi lịch sử sự cố, thu thập dữ liệu post-mortem; đóng ticket                | Đã xử lý                                |

## 6. Email / Chat drafts

### 6.1 Trả lời Manager vận hành trên Teams (10:31)

```
Dạ em nhận được rồi chị. Em xác định đây là sự cố EXPEDITE (53 học viên ở 3 lớp
không nộp được bài thi cuối kỳ). Em đang báo ngay cho đội kỹ thuật và sẽ cập nhật
tình hình cho chị trước 10:45 ạ.
```

### 6.2 ACK cho CXO (10:32)

```
Subject: RE: KHẨN CẤP - Không nộp được bài trên hệ thống - EXPEDITE Ticket #8

Chào chị Ngọc A,

Team Support đã nhận được thông tin hệ thống nộp bài thi không hoạt động, ảnh
hưởng các lớp WEB102-HN, DATA101-SG và MOBILE201-HN. Sự cố đã được xếp mức KHẨN
CẤP cao nhất và đội kỹ thuật đang xử lý ngay.

Team sẽ cập nhật tình hình cho chị mỗi 15 phút, lần tiếp theo trước 10:45.

Trong lúc chờ, chị giúp team nhắn giảng viên các lớp:
- Nhắc học viên KHÔNG đóng trang bài thi và lưu lại bài làm trên máy
  (copy nội dung hoặc chụp màn hình)
- Ghi nhận danh sách học viên chưa nộp được bài

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #8
```

### 6.3 Ping nhanh Dev Team (10:33, Teams)

```
🚨 EXPEDITE – Hệ thống nộp bài thi DOWN – 53 HV / 3 lớp không nộp được bài thi cuối kỳ,
lỗi "System error - please contact administrator". Ticket #8.
@senior-engineer @engineer-team @devops cần hỗ trợ ngay, em gửi chi tiết trong 10 phút.
```

### 6.4 Escalation đầy đủ cho Dev Team (10:42, Teams)

```
🚨 EXPEDITE - Hệ thống nộp bài thi DOWN 🚨

TÁC ĐỘNG NGHIÊM TRỌNG:
- 53 học viên không thể nộp bài thi cuối kỳ
- Tỷ lệ lỗi 100%
- 3 lớp / 2 cơ sở: WEB102-HN (20), DATA101-SG (18), MOBILE201-HN (15)

LỖI: "System error - please contact administrator"

PHÁT HIỆN BAN ĐẦU:
- Logs: Database timeout, không lưu được submissions
- App Insights: exception spike + database connection errors
- Bắt đầu khoảng 10:00, ngay sau bản release lúc 09:55

ĐỀ XUẤT: revert bản release 09:55 và deploy lại để database kết nối lại

YÊU CẦU: Điều tra ngay lập tức + sửa khẩn cấp

CẬP NHẬT TRẠNG THÁI: Support cập nhật Manager + CXO mỗi 15 phút,
nhờ team báo tiến độ trước 10:55

TICKET: #8

@senior-engineer @engineer-team @devops
```

### 6.5 Cập nhật Manager vận hành (10:45)

```
Subject: [EXPEDITE] Sự cố hệ thống nộp bài thi - Cập nhật #1 - Ticket #8

Chào chị,

Tình hình: Từ khoảng 10:00, hệ thống nộp bài thi lỗi hoàn toàn. Đội kỹ thuật đã
xác định sự cố trùng thời điểm với bản cập nhật hệ thống lúc 09:55.

Tác động: 53 học viên ở 3 lớp (WEB102-HN, DATA101-SG, MOBILE201-HN) chưa nộp được
bài thi cuối kỳ. Bài làm vẫn được học viên lưu lại trên máy.

Phương án:
A. Gỡ bản cập nhật, khôi phục phiên bản trước — dự kiến khoảng 20 phút,
   rủi ro thấp
B. Giữ bản cập nhật và chờ bản sửa lỗi — chưa xác định được thời gian

Đề xuất: chọn phương án A.

Cần chị quyết định:
1. Đồng ý phương án A
2. Gia hạn thời gian nộp bài thi cho 3 lớp (đề xuất thêm 30 phút sau khi hệ
   thống khôi phục) và thông báo cho giảng viên

Em sẽ cập nhật tiếp cho chị trước 11:00.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
```

### 6.6 Cập nhật CXO (10:45)

```
Subject: RE: KHẨN CẤP - Không nộp được bài trên hệ thống - EXPEDITE Ticket #8 - Cập nhật #1

Chào chị Ngọc A,

Đội kỹ thuật đã xác định nguyên nhân và đang khôi phục hệ thống. Team đã đề xuất
quản lý vận hành gia hạn thời gian nộp bài cho các lớp bị ảnh hưởng, sẽ thông
báo lại chị ngay khi có quyết định.

Chị vui lòng tiếp tục nhắc học viên giữ nguyên trang bài thi và lưu bài làm trên máy.

Team sẽ cập nhật tiếp cho chị trước 11:00.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #8
```

### 6.7 Cập nhật #2 (11:00 — gửi Manager + CXO)

```
Subject: [EXPEDITE] Sự cố hệ thống nộp bài thi - Cập nhật #2 - Ticket #8

Chào chị,

- Đội kỹ thuật đang khôi phục phiên bản trước của hệ thống (phương án A đã được duyệt).
- Thời gian nộp bài của 3 lớp được gia hạn thêm 30 phút, tính từ khi hệ thống
  hoạt động lại.
- Hệ thống hiện vẫn chưa nộp được bài; team sẽ tự kiểm tra ngay khi khôi phục xong.

Cập nhật tiếp theo trước 11:15.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #8
```

### 6.8 Thông báo đã khôi phục (11:15 — gửi Manager + CXO, sau khi tự xác minh)

```
Subject: [EXPEDITE] Hệ thống nộp bài thi đã hoạt động lại - Ticket #8

Chào chị,

Hệ thống nộp bài thi đã hoạt động lại từ 11:05. Team đã tự kiểm tra: nộp bài thử
thành công ở cả 3 lớp WEB102-HN, DATA101-SG, MOBILE201-HN, và hệ thống không còn
ghi nhận lỗi.

Học viên có thể nộp bài ngay, thời gian nộp được gia hạn đến 11:35.

Nhờ chị Ngọc A xác nhận giúp team khi học viên các lớp đã nộp bài thành công,
hoặc gửi ngay danh sách học viên vẫn gặp lỗi (nếu có).

Team sẽ tiếp tục theo dõi hệ thống thêm 30 phút.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #8
```

### 6.9 Hoàn tất & đóng ticket (11:50)

```
Subject: [EXPEDITE] Sự cố hệ thống nộp bài thi - Hoàn tất - Ticket #8

Chào chị,

Cảm ơn chị Ngọc A đã xác nhận toàn bộ học viên 3 lớp đã nộp bài thi thành công.
Sau 30 phút theo dõi, hệ thống ổn định, team xin phép đóng Ticket #8.

Tóm tắt sự cố:
- Thời gian: 10:00 – 11:05 (khoảng 65 phút)
- Ảnh hưởng: 53 học viên, 3 lớp, không nộp được bài thi cuối kỳ
- Nguyên nhân: bản cập nhật hệ thống lúc 09:55 gây lỗi kết nối cơ sở dữ liệu
- Xử lý: khôi phục phiên bản trước, gia hạn thời gian nộp bài 30 phút

Đội kỹ thuật sẽ họp rà soát sự cố (post-mortem) để tránh lặp lại; team sẽ gửi
chị các cải tiến sau buổi rà soát.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #8
```

## 7. Sau sự cố (dữ liệu cho post-mortem)

- Timeline đầy đủ: phát hiện 10:28 (người dùng báo, **trước** khi monitoring cảnh báo) → báo Dev 10:33 → rollback xong 11:05 → đóng 11:50.
- Nguyên nhân gốc (cần Dev xác nhận): bản release 09:55 làm hỏng kết nối database của chức năng lưu submission.
- Câu hỏi cho post-mortem:
  - Vì sao không có alert tự động khi error rate nộp bài lên 100%?
  - Vì sao bản release được deploy trong khung giờ thi cuối kỳ?
- Đề xuất: alert khi error rate submission > 5%; freeze release trong lịch thi; checklist test chức năng nộp bài trước khi release.

## 8. Reflection

- Làm tốt: nhận diện Expedite trong 2 phút, báo Dev trong 5 phút và điều tra song song; mỗi đối tượng nhận thông tin phù hợp (Dev: kỹ thuật; Manager: tác động + phương án + quyết định cần; CXO: tình hình + việc cần làm).
- Khó: giữ đúng nhịp cập nhật 15 phút khi đang phối hợp nhiều bên cùng lúc.
- Lần sau: đặt timer nhắc cập nhật ngay khi mở sự cố; chỉ báo "đã khôi phục" sau khi tự nộp bài thử thành công.
