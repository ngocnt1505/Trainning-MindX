# Scenario 01 — Không thể đăng nhập LMS

## 1. Phân loại

- Class of Service: **Standard**
- Lý do: chỉ 1 người dùng bị ảnh hưởng (GV Nguyễn Văn A), lỗi nằm ở tài khoản cá nhân, hệ thống LMS vẫn hoạt động bình thường với người dùng khác.
- Vì sao không phải class khác: không phải Priority/Expedite vì < 5 người dùng và không có dấu hiệu lỗi toàn hệ thống; không phải Fixed Deadline vì không có mốc thời gian cứng do hệ thống yêu cầu — tuy nhiên GV cần tài liệu cho buổi học hôm nay nên vẫn phản hồi sớm trong mục tiêu 30 phút.

## 2. Ticket Odoo

- Link: https://choi.odoo.com/odoo/helpdesk/1/tickets/6
- Tiêu đề: `LMS login failed - "Invalid username or password" - Teacher Nguyễn Văn A`
- Thẻ: `cos-standard`, `type-technical-support`, `login`, `lms`, `teacher`
- Mức ưu tiên: 1 sao (Standard)
- Khách hàng: Nguyễn Văn A — `nguyen.van.a@example.com` (email giả lập thay cho địa chỉ thật trong đề)
- Phân công: Nguyễn Thùy Ngọc

> Ghi chú: Odoo trial không có Ticket Type nên dùng thẻ `type-*` thay thế. Mọi email được ghi lại bằng **Ghi chú** (log note) để không gửi email thật ra ngoài.

- Bản ghi đầy đủ (form + chatter): [images/s01-full.pdf](images/s01-full.pdf)

## 3. Chẩn đoán

### Nguyên nhân có thể

1. Sai / quên mật khẩu
2. Tài khoản bị deactivate trong Base (trong khi nhân sự vẫn đang làm việc)
3. Lỗi trình duyệt / cache / sai URL đăng nhập
4. Lỗi toàn hệ thống

### Kết quả kiểm tra (giả định)

| Hạng mục                | Kết quả                                                                 |
| ----------------------- | ----------------------------------------------------------------------- |
| Account status (Base)   | **Deactivated** (nhánh chính) — hoặc **Active** (nhánh phụ)             |
| Nhân sự status (Base)   | Đang làm việc                                                           |
| Email trong Base        | Khớp với email gửi ticket                                               |
| Lần cuối update         | 2 tuần trước                                                            |
| Log đăng nhập           | 3 lần thất bại từ 08:40–08:50, cùng 1 thiết bị; không có dấu hiệu bị dò mật khẩu |
| Người dùng khác         | Đăng nhập bình thường → **loại trừ lỗi toàn hệ thống**                  |

### Bằng chứng (giả định)

```
Base – User: nguyen.van.a@mindx.edu.vn
  Account status : Deactivated   (updated 2 tuần trước, by HR data sync)
  Nhân sự status : Đang làm việc
  Email khớp     : Yes

LMS login log – nguyen.van.a@mindx.edu.vn
  08:40:12  FAILED  reason=account_inactive  device=Chrome/Windows
  08:44:55  FAILED  reason=account_inactive  device=Chrome/Windows
  08:50:03  FAILED  reason=account_inactive  device=Chrome/Windows
  (LMS hiển thị chung thông báo "Invalid username or password" cho mọi lần thất bại)
```

### Cây quyết định

```
Account Active?
├─ Có  → Nhánh A: reset password / hướng dẫn GV tự reset
└─ Không (Deactivated) → hỏi HR / quản lý trực tiếp
     ├─ Đang làm việc → Nhánh B: reactivate + reset password   ← đã xử lý trong Odoo
     └─ Đã nghỉ việc  → Nhánh C: giải thích cho người dùng, đóng ticket
Có dấu hiệu lỗi toàn hệ thống? → escalate dev team (không áp dụng ở case này)
```

Quyết định: Base báo tài khoản bị deactivate 2 tuần trước dù nhân sự vẫn "Đang làm việc" — **không tự reactivate** mà xác minh với HR trước, vì việc bật lại tài khoản của người đã nghỉ là rủi ro bảo mật.

## 4. Timeline (nhánh B — đã thực hiện trong Odoo)

| Giờ   | Bước (7-step)     | Hành động                                                                 | Ghi chú / Quyết định                               |
| ----- | ----------------- | ------------------------------------------------------------------------- | -------------------------------------------------- |
| 09:00 | —                 | Nhận email từ GV Nguyễn Văn A                                             |                                                    |
| 09:05 | 1. Reception      | Tạo ticket #6, gắn thẻ, phân công                                         | CoS Standard (1 user)                              |
| 09:10 | 2. Response       | Gửi email ACK, hẹn cập nhật trước 09:40, gợi ý cách thử tạm thời          | Trong mục tiêu < 30 phút                           |
| 09:20 | 3. Diagnosis      | Kiểm tra Base + log đăng nhập                                             | Account Deactivated, nhân sự Đang làm việc         |
| 09:25 | 3. Diagnosis      | Nhắn HR + quản lý trực tiếp để xác minh                                   | Không tự reactivate khi chưa xác minh              |
| 09:35 | 4. Resolution     | HR xác nhận GV đang làm việc → reactivate + gửi link đặt lại mật khẩu      | Nguyên nhân: deactivate nhầm khi cập nhật dữ liệu nhân sự |
| 09:40 | 5. Communication  | Gửi email kết quả cho GV, chuyển ticket sang Waiting Customer             | Đúng hẹn cập nhật 09:40                            |
| 10:00 | 6. Follow-up      | GV xác nhận đăng nhập thành công → gửi email xác nhận, hỏi cần hỗ trợ thêm | Chỉ đóng sau khi có xác nhận                       |
| 10:05 | 7. Trend Analysis | Ghi lại nguyên nhân, đề xuất HR rà soát các tài khoản bị deactivate cùng đợt; đóng ticket (Đã xử lý) | Tổng thời gian xử lý: ~65 phút |

## 5. Email / Chat drafts

### 5.1 ACK (09:10)

```
Subject: RE: Không thể đăng nhập vào LMS - Ticket #6

Chào Thầy/Cô Nguyễn Văn A,

Cảm ơn Thầy/Cô đã liên hệ. Team Support đã ghi nhận vấn đề Thầy/Cô không thể
đăng nhập LMS với thông báo "Invalid username or password" (Ticket #6).

Team hiểu Thầy/Cô cần tài liệu cho buổi học hôm nay nên đã ưu tiên kiểm tra ngay.
Team sẽ kiểm tra trạng thái tài khoản và lịch sử đăng nhập của Thầy/Cô trên hệ
thống, và sẽ cập nhật kết quả cho Thầy/Cô trước 09:40 hôm nay.

Trong lúc chờ, Thầy/Cô có thể thử:
- Đăng nhập bằng cửa sổ ẩn danh (Incognito) của trình duyệt
- Kiểm tra đúng địa chỉ đăng nhập: lms.mindx.edu.vn
- Kiểm tra phím Caps Lock và tắt bộ gõ tiếng Việt khi nhập mật khẩu

Nếu Thầy/Cô cần tài liệu gấp trước khi tài khoản được xử lý, Thầy/Cô vui lòng
phản hồi email này để team hỗ trợ phương án tạm thời.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #6
```

### 5.2 Tin nhắn nội bộ xác minh với HR (09:25, Teams)

```
Chào chị/anh team HR,

Em đang xử lý Ticket #6: GV Nguyễn Văn A (nguyen.van.a@mindx.edu.vn) không đăng nhập được LMS.
Trên Base, tài khoản đang ở trạng thái Deactivated (cập nhật 2 tuần trước), nhưng
trạng thái nhân sự vẫn là "Đang làm việc".

Nhờ chị/anh xác nhận giúp em: GV Nguyễn Văn A hiện còn làm việc không ạ?
- Nếu còn: em sẽ reactivate tài khoản
- Nếu đã nghỉ: em sẽ phản hồi GV và đóng ticket

GV cần tài liệu cho buổi học hôm nay nên nhờ chị/anh phản hồi sớm giúp em. Em cảm ơn!
```

### 5.3 Resolution — Nhánh B: Deactivated, đang làm việc (09:40)

```
Subject: RE: Không thể đăng nhập vào LMS - Đã xử lý - Ticket #6

Chào Thầy/Cô Nguyễn Văn A,

Team đã kiểm tra và phát hiện tài khoản LMS của Thầy/Cô bị tạm khoá (deactivate)
trên hệ thống từ khoảng 2 tuần trước, đây là lý do Thầy/Cô không đăng nhập được.

Sau khi xác nhận với team HR, team đã mở lại tài khoản cho Thầy/Cô. Team cũng đã
gửi link đặt lại mật khẩu đến email nguyen.van.a@mindx.edu.vn (link có hiệu lực
trong 24 giờ).

Thầy/Cô vui lòng:
1. Mở email và bấm vào link để đặt mật khẩu mới
2. Đăng nhập lại tại lms.mindx.edu.vn
3. Phản hồi email này giúp team khi đã đăng nhập được, hoặc nếu vẫn gặp lỗi

Team sẽ giữ ticket mở đến khi Thầy/Cô xác nhận đăng nhập thành công.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #6
```

### 5.4 Resolution — Nhánh A: tài khoản Active

```
Subject: RE: Không thể đăng nhập vào LMS - Hướng dẫn đặt lại mật khẩu - Ticket #6

Chào Thầy/Cô Nguyễn Văn A,

Team đã kiểm tra: tài khoản LMS của Thầy/Cô vẫn đang hoạt động bình thường. Hệ
thống ghi nhận 3 lần đăng nhập sai mật khẩu sáng nay, nên nhiều khả năng mật khẩu
đã được thay đổi hoặc nhập chưa đúng.

Thầy/Cô có thể đặt lại mật khẩu như sau:
1. Vào lms.mindx.edu.vn, bấm "Quên mật khẩu"
2. Nhập email nguyen.van.a@mindx.edu.vn
3. Mở email từ hệ thống và làm theo hướng dẫn để đặt mật khẩu mới

Nếu không nhận được email sau 10 phút (vui lòng kiểm tra cả thư mục Spam), Thầy/Cô
phản hồi lại để team đặt lại mật khẩu trực tiếp cho Thầy/Cô.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #6
```

### 5.5 Resolution — Nhánh C: Deactivated, đã nghỉ việc

```
Subject: RE: Không thể đăng nhập vào LMS - Ticket #6

Chào anh/chị Nguyễn Văn A,

Team đã kiểm tra và xác nhận với bộ phận Nhân sự: tài khoản LMS đã được đóng theo
quy trình sau khi kết thúc hợp đồng làm việc, nên hiện không thể đăng nhập.

Nếu anh/chị cho rằng thông tin này chưa chính xác, hoặc cần lấy lại tài liệu cá
nhân, anh/chị vui lòng liên hệ trực tiếp bộ phận Nhân sự hoặc quản lý trực tiếp
để được hỗ trợ.

Team xin phép đóng ticket này. Cảm ơn anh/chị đã liên hệ.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #6
```

### 5.6 Follow-up & đóng ticket (10:00)

```
Subject: RE: Không thể đăng nhập vào LMS - Xác nhận hoàn tất - Ticket #6

Chào Thầy/Cô Nguyễn Văn A,

Cảm ơn Thầy/Cô đã xác nhận đăng nhập LMS thành công. Team xin phép đóng Ticket #6.

Nếu Thầy/Cô gặp lại vấn đề tương tự hoặc cần hỗ trợ thêm, Thầy/Cô chỉ cần trả lời
email này, ticket sẽ được mở lại.

Chúc Thầy/Cô có buổi học tốt!

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #6
```

## 6. Trend Analysis

- Nguyên nhân gốc: tài khoản bị deactivate nhầm trong lần cập nhật dữ liệu nhân sự 2 tuần trước.
- Đề xuất: nhờ HR rà soát các tài khoản bị deactivate cùng đợt nhưng nhân sự vẫn "Đang làm việc" để xử lý chủ động, tránh phát sinh thêm ticket.
- Thêm bài KB: "Không đăng nhập được LMS — checklist kiểm tra Base (account status / nhân sự status / email)".

## 7. Reflection

- Làm tốt: phản hồi trong 10 phút, đưa mốc cập nhật cụ thể thay vì hứa giờ sửa xong; không tự reactivate tài khoản khi chưa xác minh với HR.
- Khó: cân bằng giữa tính khẩn cấp (GV cần tài liệu hôm nay) và quy trình xác minh bảo mật.
- Lần sau: hỏi HR song song ngay khi thấy trạng thái Deactivated để rút ngắn thời gian chờ; chuẩn bị sẵn phương án gửi tài liệu tạm cho GV.
