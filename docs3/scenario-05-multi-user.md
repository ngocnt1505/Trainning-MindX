# Scenario 05 — Video không xem được (nhiều người dùng)

## 1. Phân loại

- Class of Service: **Priority**
- Lý do: **12 học viên** bị ảnh hưởng (trong khoảng 5–25), không xem được video bài học → bị chặn việc học, đang diễn ra từ ~19:40.
- Vì sao không phải class khác: không phải Standard vì nhiều người dùng và nhiều ticket cùng báo một lỗi; chưa phải Expedite vì < 25 người dùng — **nếu điều tra cho thấy lỗi lan sang nhiều lớp/khoá (Branch B) thì nâng lên Expedite**.

### Triage nhanh (< 5 phút)

| Câu hỏi                      | Dữ liệu ban đầu                                         |
| ---------------------------- | ------------------------------------------------------- |
| 1 lớp hay nhiều lớp?         | Mới thấy lớp `JS-ADV-HN-2412` (khoá Advanced JavaScript) |
| 1 video/lesson hay toàn bộ?  | Các báo cáo đều nhắc **Lesson 3** → cần xác minh        |
| Web-only hay cả mobile?      | **Cả hai**: 8 web (Chrome 120+), 4 mobile (iOS Safari / Android Chrome) |
| Phía người dùng?             | Ít khả năng: đổi wifi/4G vẫn lỗi, nhiều thiết bị khác nhau |

## 2. Ticket Odoo — gom nhóm

| Ticket       | Người báo                       | Nhận lúc | Vai trò                          | Giai đoạn cuối |
| ------------ | ------------------------------- | -------- | -------------------------------- | -------------- |
| **#10** | CXO lớp JS-ADV-HN-2412          | 19:45    | **Ticket chính**                 | Đã xử lý       |
| #11      | Học viên Trần Minh Khoa (mobile) | 19:52   | Duplicate → liên kết ticket chính | Đã hủy        |
| #12      | GV Phạm Thu Trang               | 20:02    | Duplicate → liên kết ticket chính | Đã hủy        |

- Link ticket chính: https://choi.odoo.com/odoo/helpdesk/1/tickets/10 (phụ: .../tickets/11, .../tickets/12)
- Tiêu đề ticket chính: `Video playback issue - Lesson 3 (JS-ADV-HN-2412) - 12 users`
- Thẻ: `cos-priority`, `type-incident`, `lms`, `video`, `cdn`, `js-adv`, `lesson-3`
- Thẻ ticket phụ: `cos-priority`, `type-incident`, `video`, `duplicate`
- Mức ưu tiên: 2 sao (High)
- Phân công: Nguyễn Thùy Ngọc

> Odoo trial: liên kết bằng ghi chú "Duplicate of #…" / "Related: #…" + thẻ `duplicate`, sau đó chuyển ticket phụ sang Đã hủy. Mọi cập nhật chỉ trao đổi trên ticket chính để thông tin đồng bộ.

- Bản ghi ticket chính: [images/s05-main.pdf](images/s05-main.pdf)
- Bản ghi ticket phụ: [images/s05-duplicates.pdf](images/s05-duplicates.pdf) _(bổ sung sau)_

### Email của 2 ticket phụ (giả lập)

```
From: hv.khoa@mindx.edu.vn
Subject: Video bài 3 không xem được
Nhận lúc: 19:52

Em học lớp JS-ADV-HN-2412, vào bài 3 trên điện thoại (iPhone) thì video báo
"Cannot load media". Em đổi sang 4G rồi vẫn bị ạ.
Trần Minh Khoa
```

```
From: gv.trang@mindx.edu.vn
Subject: Lớp JS-ADV-HN-2412 - video Lesson 3 không chạy
Nhận lúc: 20:02

Chào team, lớp mình tối nay khoảng 12 bạn báo video Lesson 3 loading mãi không
chạy, cả máy tính và điện thoại. Team kiểm tra giúp mình nhé.
GV Phạm Thu Trang
```

## 3. Phản hồi ban đầu — ACK chung (20:10)

Gửi trên ticket chính, CC GV Trang và học viên Khoa (người báo ở 2 ticket phụ).

```
Subject: RE: Không xem được video bài 3 - Advanced JS trên Denise - PRIORITY Ticket #10

Chào anh/chị,

Team Support đã nhận được 3 phản ánh về việc video Lesson 3 khoá Advanced
JavaScript (lớp JS-ADV-HN-2412) không phát được, ảnh hưởng khoảng 12 học viên.
Các phản ánh đã được gộp vào Ticket #10 và đang được xử lý ở mức PRIORITY.
Team sẽ cập nhật tình hình qua email này trước 20:30.

Để team xử lý nhanh hơn, anh/chị giúp team gửi thêm (nếu có):
1. Link bài học hoặc mã bài học đang lỗi
2. Ảnh chụp màn hình lỗi (VD: "Cannot load media")
3. Thiết bị + mạng đang dùng (wifi/4G) + thời điểm gặp lỗi

Trong lúc chờ, học viên có thể thử:
- Mở bài học bằng cửa sổ ẩn danh (Incognito), tắt trình chặn quảng cáo (adblock)
  hoặc đổi sang trình duyệt khác
- Học tiếp bằng tài liệu PDF/slide của Lesson 3 trên Denise, hoặc chuyển sang
  bài học khác và quay lại Lesson 3 sau

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #10
```

## 4. Thu thập dữ liệu điều tra

| Cần kiểm tra                  | Ở đâu                         | Mục đích                                   |
| ----------------------------- | ----------------------------- | ------------------------------------------ |
| Error rate video endpoint, CDN 4xx/5xx, response time | Monitoring | Lỗi phía server hay không         |
| correlationId / requestId / status code | Log, API gateway    | Mã lỗi cụ thể của request video            |
| Asset tồn tại? permission? signed URL hết hạn? | Storage      | Lỗi nội dung của 1 video                   |
| Lesson khác / khoá khác có lỗi không? | Monitoring + thử trực tiếp | Phạm vi: lesson-specific hay system-wide |

Quy tắc: **chọn branch dựa trên dấu hiệu quan sát được, không phỏng đoán**.

---

## 5. Branch A — Vấn đề nội dung (✅ đã thực hiện trong Odoo)

### Dấu hiệu (giả định)

- Chỉ **Lesson 3** lỗi; tự mở Lesson 2 và Lesson 4 cùng khoá → phát bình thường
- API trả **`403`** cho file video `VID-JSADV-L03` (requestId `req-7f3a91`)
- Lỗi trên cả web và mobile, cả wifi và 4G → **không phải phía người dùng**
- Storage: signed URL của asset hết hạn lúc 19:38 (trùng thời điểm bắt đầu lỗi ~19:40)

→ **Kết luận Branch A**: vì chỉ 1 lesson lỗi + mã 403 + mọi mạng/thiết bị đều lỗi, nguyên nhân nằm ở asset video (signed URL hết hạn / sai permission), không phải hạ tầng hay người dùng.

### Các bước theo 7-step

| Giờ   | Bước              | Hành động                                                               |
| ----- | ----------------- | ----------------------------------------------------------------------- |
| 19:45 | 1. Reception      | Nhận ticket #1 từ CXO                                                   |
| 20:03 | 1. Reception      | Nhận đủ 3 ticket cùng lỗi → nhận diện pattern, chọn ticket chính, liên kết + huỷ 2 ticket phụ |
| 20:10 | 2. Response       | Gửi ACK chung, xin 3 thông tin, đưa workaround                          |
| 20:18 | 3. Diagnosis      | Kiểm tra: chỉ Lesson 3 lỗi, 403 cho `VID-JSADV-L03`, signed URL hết hạn 19:38 → Branch A |
| 20:20 | 3. Diagnosis      | Escalate Content Ops / Dev kèm đầy đủ ID; chuyển Escalated               |
| 20:25 | 5. Communication  | Cập nhật CXO + GV: đã xác định lỗi ở file video, workaround PDF / chuyển bài |
| 20:45 | 4. Resolution     | Content Ops cấp lại signed URL + sửa cấu hình thời hạn link             |
| 20:50 | 4. Resolution     | Tự kiểm tra Lesson 3 phát được trên web + mobile; verify với 2 user mẫu (HV Khoa – iPhone, 1 HV web) |
| 20:55 | 6. Follow-up      | Báo đã xử lý, nhờ GV xác nhận cả lớp xem được; chuyển Waiting Customer  |
| 21:15 | 6. Follow-up      | GV xác nhận cả 12 học viên xem được video                               |
| 21:20 | 7. Trend Analysis | Ghi nguyên nhân gốc, đề xuất alert 403 cho video asset; đóng ticket      |

### Chat escalation Content Ops / Dev (20:20, Teams)

```
@content-ops @dev-team 🟠 PRIORITY – Video Lesson 3 không phát được

Ticket: #10 (gộp 3 ticket)
Tác động: 12 học viên lớp JS-ADV-HN-2412 không xem được video, từ ~19:40
Khoá / bài: Advanced JavaScript – Lesson 3
lessonId: JSADV-L03 | videoAssetId: VID-JSADV-L03
Lỗi: API trả 403 cho file video (requestId: req-7f3a91), "Cannot load media"
Phạm vi: chỉ Lesson 3; Lesson 2 và 4 phát bình thường; lỗi trên cả web/mobile, wifi/4G
Nghi vấn: signed URL của asset hết hạn lúc 19:38 (trùng thời điểm bắt đầu lỗi)
User mẫu: hv.khoa (iPhone, 4G), 1 HV web Chrome 120

Cần: cấp lại signed URL / kiểm tra permission của asset
Support sẽ cập nhật lớp trước 20:30 và verify lại sau khi fix
```

### Email cập nhật (20:25)

```
Subject: RE: ... - PRIORITY Ticket #10 - Cập nhật

Chào anh/chị,

Team đã xác định lỗi nằm ở file video của Lesson 3 (các bài học khác vẫn phát
bình thường) và đã chuyển đội nội dung kỹ thuật xử lý.

Trong lúc chờ, lớp có thể:
- Học Lesson 3 bằng slide/PDF trên Denise
- Hoặc học trước Lesson 4 và quay lại video Lesson 3 sau

Team sẽ cập nhật tiếp trước 20:50.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #10
```

### Email đã xử lý (20:55)

```
Subject: RE: ... - PRIORITY Ticket #10 - Đã xử lý

Chào anh/chị,

Video Lesson 3 đã phát lại bình thường từ 20:45. Team đã tự kiểm tra trên máy
tính và điện thoại, và đã xác nhận với 2 học viên trong lớp.

Nhờ cô Trang xác nhận giúp team khi các bạn trong lớp đã xem được video, hoặc
báo lại nếu còn bạn nào gặp lỗi (kèm ảnh chụp màn hình). Nếu vẫn lỗi, học viên
thử tải lại trang (Ctrl + F5) trước.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #10
```

### Email follow-up & đóng ticket (21:15)

```
Subject: RE: ... - PRIORITY Ticket #10 - Hoàn tất

Chào anh/chị,

Cảm ơn cô Trang đã xác nhận cả lớp đã xem được video Lesson 3. Team xin phép đóng
Ticket #10 (cùng 2 phản ánh đã gộp).

Nguyên nhân: đường dẫn bảo mật của file video Lesson 3 hết hạn, khiến video không
tải được. Đội nội dung đã cấp lại và điều chỉnh cấu hình để tránh lặp lại.

Nếu gặp lại lỗi, anh/chị chỉ cần trả lời email này.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #10
```

### Update trong Odoo (có timestamp)

```
[20:03] RECEPTION – 3 ticket cùng lỗi trong 20 phút → gộp vào ticket chính. Related: #11, #12. CoS Priority (12 HV).
[20:10] RESPONSE – ACK chung, xin 3 thông tin, workaround Incognito / PDF.
[20:18] DIAGNOSIS – Chỉ Lesson 3 lỗi, API 403 cho VID-JSADV-L03, signed URL hết hạn 19:38, lỗi mọi mạng/thiết bị → Branch A.
[20:20] ESCALATION – Content Ops / Dev kèm lessonId, videoAssetId, requestId, user mẫu.
[20:25] COMMUNICATION – Cập nhật lớp + workaround.
[20:45] RESOLUTION – Content Ops cấp lại signed URL, sửa cấu hình thời hạn link.
[20:50] RESOLUTION – Tự kiểm tra + verify 2 user mẫu: OK.
[20:55] FOLLOW-UP – Báo đã xử lý, chờ GV xác nhận.
[21:20] TREND – GV xác nhận 12 HV xem được. Đề xuất alert 403 trên video asset. Đóng ticket.
```

---

## 6. Branch B — Vấn đề hệ thống / CDN

### Dấu hiệu (giả định)

- Nhiều lesson và khoá khác cũng bắt đầu lỗi (Lesson 1–5 Advanced JS, khoá Python Basic…)
- Monitoring: error rate video endpoint tăng từ 0,5% → 40% lúc 19:40, response time tăng mạnh
- CDN / gateway: spike **`502` / `504`**

→ **Kết luận Branch B**: lỗi xảy ra trên nhiều khoá + mã 5xx từ CDN → sự cố hạ tầng. Số người bị ảnh hưởng có thể vượt 25 → **nâng lên Expedite**, escalate DevOps ngay.

### Các bước theo 7-step

| Giờ   | Bước              | Hành động                                                                  |
| ----- | ----------------- | -------------------------------------------------------------------------- |
| 20:03 | 1. Reception      | Gộp 3 ticket vào ticket chính                                              |
| 20:10 | 2. Response       | ACK chung                                                                  |
| 20:15 | 3. Diagnosis      | Monitoring: nhiều khoá lỗi, CDN 502/504 spike → Branch B; nâng Expedite    |
| 20:16 | 3. Diagnosis      | Escalate DevOps/Infra ngay; báo Manager vận hành                            |
| 20:20 | 5. Communication  | **Broadcast** tới các CXO/GV đang có lớp tối nay: sự cố video diện rộng + workaround |
| 20:35 / 20:50 | 5. Communication | Cập nhật mỗi 15 phút (sự cố đã lên Expedite)                     |
| 21:00 | 4. Resolution     | DevOps chuyển traffic sang CDN dự phòng                                    |
| 21:00–21:15 | 4. Resolution | Theo dõi error rate về < 1%; tự phát thử video nhiều khoá; user mẫu xác nhận |
| 21:20 | 6. Follow-up      | Thông báo khôi phục tới tất cả CXO/GV đã nhận broadcast                    |
| 21:50 | 7. Trend Analysis | Theo dõi 30 phút ổn định; dữ liệu post-mortem; đóng ticket                 |

### Chat escalation DevOps (20:16, Teams)

```
@devops @infra 🔴 Video LMS lỗi diện rộng – nghi CDN

Ticket: #10
Tác động: nhiều khoá/lesson không phát được video từ ~19:40 (ban đầu 12 HV
JS-ADV-HN-2412, đang lan sang khoá khác) → đề xuất xử lý mức EXPEDITE
Monitoring: error rate video endpoint 0,5% → 40%, response time tăng mạnh
CDN/gateway: spike 502/504 từ 19:40
Phạm vi: nhiều khoá, cả web/mobile, mọi mạng

Cần: kiểm tra CDN/gateway, phương án chuyển CDN dự phòng
Support cập nhật stakeholders mỗi 15 phút
```

### Broadcast tới CXO / GV (20:20)

```
Subject: [Thông báo] Sự cố phát video trên LMS - đang xử lý

Chào các anh/chị CXO và giảng viên,

Từ khoảng 19:40, video bài học trên LMS đang gặp lỗi không phát được ở nhiều
khoá học. Đội kỹ thuật đã xác định lỗi từ phía hệ thống và đang xử lý khẩn cấp.

Trong lúc chờ, lớp học có thể dùng slide/tài liệu PDF trên Denise hoặc chuyển
sang hoạt động không cần video. Học viên không cần thử lại liên tục.

Team sẽ cập nhật tình hình mỗi 15 phút, lần tiếp theo trước 20:35.

Trân trọng,
MindX Support Team
Ticket #10
```

### Email đã khôi phục (21:20)

```
Subject: [Thông báo] Sự cố phát video trên LMS - đã khôi phục

Chào các anh/chị,

Video trên LMS đã phát lại bình thường từ 21:00. Team đã kiểm tra trên nhiều khoá
học, tỷ lệ lỗi đã trở về mức bình thường, và đã xác nhận với một số học viên.

Nếu lớp anh/chị còn học viên gặp lỗi, vui lòng trả lời email này kèm tên lớp và
ảnh chụp màn hình. Team sẽ tiếp tục theo dõi hệ thống thêm 30 phút.

Trân trọng,
MindX Support Team
Ticket #10
```

### Update trong Odoo (có timestamp)

```
[20:15] DIAGNOSIS – Nhiều khoá lỗi; error rate video 0,5%→40%; CDN 502/504 spike → Branch B. Nâng CoS lên Expedite.
[20:16] ESCALATION – DevOps/Infra + báo Manager vận hành.
[20:20] COMMUNICATION – Broadcast CXO/GV có lớp tối nay.
[20:35] COMMUNICATION – Cập nhật #2: DevOps đang kiểm tra CDN.
[20:50] COMMUNICATION – Cập nhật #3: chuẩn bị chuyển CDN dự phòng.
[21:00] RESOLUTION – Chuyển sang CDN dự phòng; error rate < 1%.
[21:15] RESOLUTION – Tự phát thử nhiều khoá + user mẫu: OK.
[21:20] FOLLOW-UP – Thông báo khôi phục.
[21:50] TREND – 30 phút ổn định; dữ liệu post-mortem; đóng ticket.
```

---

## 7. Branch C — Nguyên nhân phía người dùng

### Dấu hiệu (giả định)

- Chỉ một nhóm nhỏ học viên bị (sau khi xác minh: 4/12 thực sự còn lỗi), cùng dùng 1 extension chặn quảng cáo / cùng 1 nhà mạng
- Mở bằng **Incognito → video phát bình thường**
- Video phát OK trên mobile nhưng lỗi trên desktop của nhóm đó
- Monitoring bình thường, không có 4xx/5xx bất thường

→ **Kết luận Branch C**: hệ thống không lỗi (monitoring sạch, Incognito phát được); lỗi do extension/cache/DNS trên máy người dùng → hướng dẫn phía người dùng, không escalate.

### Các bước theo 7-step

| Giờ   | Bước              | Hành động                                                         |
| ----- | ----------------- | ----------------------------------------------------------------- |
| 20:03 | 1. Reception      | Gộp 3 ticket vào ticket chính                                     |
| 20:10 | 2. Response       | ACK chung + workaround Incognito                                  |
| 20:20 | 3. Diagnosis      | Monitoring sạch; HV phản hồi Incognito xem được; nhóm lỗi dùng cùng adblock → Branch C |
| 20:25 | 4. Resolution     | Gửi hướng dẫn xử lý phía người dùng                               |
| 20:40 | 4. Resolution     | Verify với 2 user mẫu sau khi làm theo hướng dẫn: OK              |
| 20:45 | 6. Follow-up      | Nhờ GV xác nhận cả lớp; chuyển Waiting Customer                   |
| 21:00 | 6. Follow-up      | **Điều kiện đóng: user xác nhận OK** → GV xác nhận                |
| 21:05 | 7. Trend Analysis | Thêm bài KB "Video không phát – kiểm tra phía người dùng"; đóng ticket |

### Email hướng dẫn phía người dùng (20:25)

```
Subject: RE: ... - PRIORITY Ticket #10 - Hướng dẫn xử lý

Chào anh/chị,

Team đã kiểm tra: hệ thống video của LMS đang hoạt động bình thường, và video
Lesson 3 phát được khi mở bằng cửa sổ ẩn danh. Lỗi nhiều khả năng do cài đặt
trên trình duyệt hoặc mạng của một số học viên.

Học viên còn lỗi vui lòng thử lần lượt:
1. Tắt tiện ích chặn quảng cáo (AdBlock, uBlock…) cho trang LMS rồi tải lại trang
2. Xoá cache trình duyệt: Ctrl + Shift + Delete → chọn "Hình ảnh và tệp được lưu
   trong bộ nhớ đệm" → Xoá
3. Đổi DNS sang 8.8.8.8 hoặc thử bằng mạng 4G
4. Nếu vẫn lỗi: gửi team ảnh chụp màn hình + tên trình duyệt + thiết bị

Nhờ cô Trang xác nhận lại giúp team khi các bạn đã xem được video.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #10
```

### Email xác nhận & đóng (21:00)

```
Subject: RE: ... - PRIORITY Ticket #10 - Hoàn tất

Chào anh/chị,

Cảm ơn cô Trang đã xác nhận các bạn đã xem được video sau khi tắt tiện ích chặn
quảng cáo. Team xin phép đóng Ticket #10.

Lưu ý cho lớp: nếu dùng tiện ích chặn quảng cáo, vui lòng thêm trang LMS vào danh
sách cho phép để tránh gặp lại lỗi.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #10
```

### Update trong Odoo (có timestamp)

```
[20:20] DIAGNOSIS – Monitoring bình thường, không 4xx/5xx. Incognito phát được. Nhóm lỗi dùng cùng adblock → Branch C, không escalate.
[20:25] RESOLUTION – Gửi hướng dẫn: tắt adblock, xoá cache, đổi DNS/4G.
[20:40] RESOLUTION – Verify 2 user mẫu: OK.
[20:45] FOLLOW-UP – Chờ GV xác nhận cả lớp.
[21:05] TREND – GV xác nhận OK. Tạo KB "Video không phát – kiểm tra phía người dùng". Đóng ticket.
```

---

## 8. Reflection

- Làm tốt: nhận ra pattern sau 3 ticket trong 20 phút và gộp về 1 ticket chính để mọi người nhận cùng một thông tin; ACK xin đúng 3 thông tin tối thiểu, tránh hỏi qua hỏi lại.
- Khó: chọn branch chỉ dựa trên dấu hiệu (mã lỗi, phạm vi lesson/khoá, Incognito) thay vì đoán theo mô tả "loading mãi" của người dùng.
- Lần sau: luôn kiểm tra 1 lesson khác + 1 khoá khác ngay từ đầu — đây là phép thử nhanh nhất để phân biệt Branch A / B / C.
