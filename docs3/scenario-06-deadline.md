# Scenario 06 — Báo cáo tuyển sinh cần gấp (Fixed Deadline)

## 1. Phân loại

- Class of Service: **Fixed Deadline**
- Lý do: có **deadline cứng** 09:00 ngày 05/11 (cuộc họp của Director, không dời được); giá trị của báo cáo mất đi nếu giao sau mốc này. Ưu tiên được quyết định theo **thời gian**, không theo số người bị ảnh hưởng.
- Vì sao không phải class khác: không có sự cố hay người dùng bị chặn nên không phải Priority/Expedite; không phải Standard vì có mốc thời gian bắt buộc và business impact cao (trình bày cho Director).
- Mục tiêu: chốt **scope tối thiểu (MVP)** đủ dùng cho cuộc họp, phần còn lại là nice-to-have.

## 2. Ticket Odoo

- Link: https://choi.odoo.com/odoo/helpdesk/1/tickets/13
- Tiêu đề: `Fixed Deadline - Enrollment report for Director (Due 09:00 05/11)`
- Thẻ: `cos-fixed-deadline`, `type-report-request`, `reporting`, `enrollment`, `director`
- Mức ưu tiên: 2 sao (High)
- Khách hàng: Director — `director@example.com` (email giả lập)
- Phân công: Nguyễn Thùy Ngọc
- Deadline cứng: **09:00 thứ Năm 05/11**

- Bản ghi đầy đủ (form + chatter): [images/s06-full.pdf](images/s06-full.pdf) _(bổ sung sau)_

### Rủi ro ghi nhận khi tiếp nhận

| Rủi ro                    | Mô tả                                                            | Cách giảm thiểu                                  |
| ------------------------- | ---------------------------------------------------------------- | ------------------------------------------------ |
| Định nghĩa metric chưa rõ | "Tuyển sinh" = đăng ký hay đã đóng học phí?                      | Hỏi rõ trong ACK                                 |
| Dữ liệu nhạy cảm (PII)    | Danh tính học viên/phụ huynh, doanh thu                          | Chỉ lấy số liệu tổng hợp; xin duyệt quản lý     |
| Nhiều nguồn dữ liệu       | Enrollment (CRM), revenue (kế toán), completion (LMS)            | Ưu tiên enrollment cho MVP                       |
| Query nặng                | Dữ liệu nhiều cơ sở, nhiều tháng                                 | Chạy ngoài giờ cao điểm, lọc đúng khoảng thời gian |
| Thời gian                 | Còn ~1,5 ngày làm việc                                          | Bản nháp sớm + buffer trước deadline            |

## 3. Scope đã chốt

| Hạng mục                                         | Loại          | Ghi chú                                  |
| ------------------------------------------------ | ------------- | ---------------------------------------- |
| Số tuyển sinh theo **cơ sở × chương trình × tháng** | **MVP**     | Tuyển sinh = học viên **đã đóng học phí** |
| Breakdown theo **khoá học**                      | **MVP**       |                                          |
| Khoảng thời gian 01/01/2026 – 31/10/2026         | **MVP**       | Theo xác nhận của Director               |
| So sánh cùng kỳ 2025                             | Nice-to-have  | Làm nếu còn thời gian sau bản nháp       |
| Doanh thu theo cơ sở (tổng hợp)                  | Nice-to-have  | Cần duyệt của quản lý                    |
| Tỷ lệ hoàn thành khoá học                        | Nice-to-have  | Nằm ở LMS, khác nguồn → để sau           |
| Danh tính học viên / phụ huynh                   | **Không lấy** | Không cần cho họp, tránh PII             |

### Template dữ liệu đề xuất (gửi Director xác nhận)

| Tháng   | Cơ sở            | Chương trình   | Khoá học        | Số tuyển sinh (đã đóng phí) |
| ------- | ---------------- | -------------- | --------------- | --------------------------- |
| 2026-01 | Nguyễn Chí Thanh | Coding Teen    | Web Basic       | 42                          |
| 2026-01 | Nguyễn Chí Thanh | Coding Teen    | Python Basic    | 35                          |
| …       | …                | …              | …               | …                           |

+ Sheet tổng hợp: tổng theo cơ sở, tổng theo chương trình, biểu đồ theo tháng.

## 4. Timeline

| Thời điểm      | Bước (7-step)     | Hành động                                                                  | Ghi chú / Quyết định                          |
| -------------- | ----------------- | -------------------------------------------------------------------------- | --------------------------------------------- |
| 03/11 – 14:00  | —                 | Nhận email của Director                                                    | Deadline 09:00 05/11                          |
| 03/11 – 14:08  | 1. Reception      | Triage: Fixed Deadline; mục tiêu chốt MVP                                  | < 10 phút                                     |
| 03/11 – 14:20  | 1. Reception      | Tạo ticket: deadline, impact, phạm vi dự kiến, rủi ro                      | < 15 phút                                     |
| 03/11 – 14:30  | 2. Response       | Gửi ACK + 4 câu hỏi chốt scope; chuyển Waiting Customer                    | < 30 phút                                     |
| 03/11 – 15:30  | 3. Diagnosis      | Director trả lời: 01/01–31/10/2026, không cần danh tính, ưu tiên cơ sở + chương trình, tuyển sinh = đã đóng phí | |
| 03/11 – 16:00  | 3. Diagnosis      | Đánh giá khả thi; gửi template + scope MVP / nice-to-have + timeline       | Bản nháp 15:00 04/11, bản chốt 17:00 04/11   |
| 03/11 – 16:30  | 3. Diagnosis      | Director xác nhận scope và timeline                                        | Scope đã chốt                                 |
| 03/11 – 16:45  | 4. Resolution     | Xin duyệt quản lý trực tiếp về phạm vi dữ liệu + doanh thu                 |                                               |
| 03/11 – 17:30  | 4. Resolution     | Quản lý duyệt: enrollment tổng hợp OK; doanh thu chỉ ở mức tổng theo cơ sở | Không xuất PII                                |
| 04/11 – 09:00  | 4. Resolution     | Bắt đầu trích xuất từ CRM; chuyển Đang thực hiện                           |                                               |
| 04/11 – 11:00  | 5. Communication  | **Phát sinh**: dữ liệu tháng 09 cơ sở Đà Nẵng thiếu do lỗi đồng bộ CRM → raise sớm + 2 phương án | Raise ngay, không chờ đến deadline |
| 04/11 – 11:30  | 5. Communication  | Director chọn phương án A (lấy số liệu từ admin cơ sở, chốt trước 14:00)   |                                               |
| 04/11 – 14:00  | 4. Resolution     | Nhận số liệu từ admin cơ sở Đà Nẵng, đối chiếu và ghép vào báo cáo         |                                               |
| 04/11 – 15:00  | 5. Communication  | Gửi bản nháp để Director review                                            | Đúng mốc                                      |
| 04/11 – 16:00  | 5. Communication  | Director góp ý: thêm dòng tổng + biểu đồ theo tháng                        |                                               |
| 04/11 – 17:00  | 4. Resolution     | Bàn giao bản chốt (link + file) kèm định nghĩa metric và giới hạn dữ liệu; chuyển Waiting Customer | Trước deadline 16 tiếng |
| 05/11 – 10:30  | 6. Follow-up      | Sau cuộc họp: hỏi báo cáo đã đáp ứng chưa, có cần bổ sung nice-to-have không | Director xác nhận đủ dùng                  |
| 05/11 – 10:45  | 7. Trend Analysis | Đề xuất dashboard tự phục vụ cho báo cáo định kỳ; báo Dev lỗi đồng bộ CRM Đà Nẵng; đóng ticket | Đã xử lý                      |

## 5. Email / Chat drafts

### 5.1 ACK + câu hỏi chốt scope (03/11 – 14:30)

```
Subject: RE: Cần báo cáo tuyển sinh trước 09:00 sáng ngày kia - Ticket #13

Chào anh/chị,

Team Support đã nhận yêu cầu báo cáo tuyển sinh cho cuộc họp lúc 09:00 thứ Năm
05/11 (Ticket #13). Để kịp deadline, team cần chốt phạm vi báo cáo ngay hôm nay.
Anh/chị giúp team trả lời 4 câu sau:

1. Khoảng thời gian: dữ liệu từ tháng nào đến tháng nào (VD: tháng này, cả năm
   2026, hay có so sánh với 2025)?
2. Định nghĩa "tuyển sinh": tính học viên đã đăng ký hay chỉ học viên đã đóng
   học phí?
3. Thông tin trong báo cáo: chỉ cần số liệu tổng hợp, hay cần danh sách chi tiết
   (có danh tính học viên)? Có cần doanh thu / tỷ lệ hoàn thành không?
4. Phần ưu tiên: nếu cần làm trước một phần, anh/chị ưu tiên lọc theo cơ sở,
   chương trình hay khoá học nào?

Sau khi nhận được phản hồi, team sẽ gửi lại mẫu báo cáo và timeline cụ thể để
anh/chị xác nhận trong hôm nay.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #13
```

### 5.2 Chốt scope + đàm phán MVP / nice-to-have (03/11 – 16:00)

```
Subject: RE: Báo cáo tuyển sinh - Xác nhận phạm vi và timeline - Ticket #13

Chào anh/chị,

Cảm ơn anh/chị đã phản hồi. Team đề xuất phạm vi báo cáo như sau:

PHẦN CHÍNH (đảm bảo có trước cuộc họp):
- Số học viên tuyển sinh (đã đóng học phí) từ 01/01/2026 đến 31/10/2026
- Lọc theo cơ sở + chương trình + tháng, có breakdown theo khoá học
- Sheet tổng hợp theo cơ sở và theo chương trình

PHẦN BỔ SUNG (làm nếu còn thời gian, không ảnh hưởng phần chính):
- So sánh cùng kỳ 2025
- Doanh thu tổng hợp theo cơ sở (cần phê duyệt dữ liệu tài chính)

Không bao gồm: danh tính học viên/phụ huynh (không cần cho cuộc họp và để bảo
mật dữ liệu cá nhân). Tỷ lệ hoàn thành khoá học nằm ở hệ thống khác, team đề
xuất làm sau cuộc họp nếu anh/chị cần.

Mẫu báo cáo: team đính kèm file mẫu (các cột: Tháng | Cơ sở | Chương trình |
Khoá học | Số tuyển sinh).

Timeline:
- 15:00 thứ Tư 04/11: gửi bản nháp để anh/chị góp ý
- 17:00 thứ Tư 04/11: gửi bản chốt
- Sáng thứ Năm 05/11: dự phòng để chỉnh sửa gấp trước 09:00 nếu cần

Anh/chị xác nhận giúp team phạm vi và timeline trên trước 17:00 hôm nay nhé.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #13
```

### 5.3 Xin phê duyệt quản lý trực tiếp (03/11 – 16:45)

```
Subject: [Xin duyệt] Trích xuất dữ liệu tuyển sinh cho báo cáo của Director - Ticket #13

Chào anh/chị,

Em đang xử lý yêu cầu báo cáo tuyển sinh của Director cho cuộc họp 09:00 thứ
Năm 05/11 (Ticket #13). Em xin duyệt phạm vi trích xuất dữ liệu như sau:

Dữ liệu cần trích xuất:
- Số học viên tuyển sinh (đã đóng học phí), 01/01–31/10/2026, tổng hợp theo cơ
  sở / chương trình / khoá học / tháng — nguồn CRM
- (Bổ sung) Doanh thu tổng hợp theo cơ sở — nguồn kế toán

Bảo mật:
- KHÔNG xuất danh tính học viên/phụ huynh, chỉ số liệu tổng hợp
- File chỉ chia sẻ cho Director qua link nội bộ có phân quyền

Cần anh/chị quyết định:
1. Duyệt trích xuất số liệu tuyển sinh tổng hợp
2. Duyệt / không duyệt phần doanh thu theo cơ sở

Để kịp deadline, nhờ anh/chị phản hồi giúp em trong hôm nay. Em cảm ơn!

Nguyễn Thùy Ngọc – Support
```

### 5.4 Raise vấn đề phát sinh + phương án (04/11 – 11:00)

```
Subject: RE: Báo cáo tuyển sinh - Vấn đề phát sinh cần anh/chị chọn phương án - Ticket #13

Chào anh/chị,

Trong quá trình trích xuất, team phát hiện dữ liệu tuyển sinh tháng 09 của cơ
sở Đà Nẵng bị thiếu do lỗi đồng bộ hệ thống. Các cơ sở và tháng khác đã đầy đủ,
timeline tổng thể không thay đổi.

Phương án:
A. Lấy số liệu tháng 09 trực tiếp từ admin cơ sở Đà Nẵng (đã liên hệ, dự kiến
   có trước 14:00 hôm nay), team đối chiếu rồi ghép vào báo cáo.
B. Giữ nguyên dữ liệu hệ thống và ghi chú rõ trong báo cáo "Đà Nẵng tháng 09
   chưa đầy đủ".

Đề xuất: phương án A. Nếu đến 14:00 chưa có số liệu, team sẽ chuyển sang
phương án B để không ảnh hưởng mốc bản nháp 15:00.

Anh/chị chọn giúp team phương án trước 12:00 nhé.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #13
```

### 5.5 Gửi bản nháp (04/11 – 15:00)

```
Subject: RE: Báo cáo tuyển sinh - Bản nháp để góp ý - Ticket #13

Chào anh/chị,

Team gửi anh/chị bản nháp báo cáo tuyển sinh: [link file nội bộ]

Bản nháp đã bao gồm toàn bộ phần chính; số liệu Đà Nẵng tháng 09 đã được bổ
sung từ admin cơ sở theo phương án A.

Anh/chị góp ý giúp team trước 16:30 để team hoàn thiện bản chốt lúc 17:00.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #13
```

### 5.6 Bàn giao bản chốt (04/11 – 17:00)

```
Subject: RE: Báo cáo tuyển sinh - Bản chốt cho cuộc họp 05/11 - Ticket #13

Chào anh/chị,

Team gửi anh/chị bản chốt báo cáo tuyển sinh cho cuộc họp 09:00 ngày mai:
- Link: [link file nội bộ – chỉ anh/chị có quyền xem]
- File đính kèm: Bao_cao_tuyen_sinh_2026-01_den_2026-10.xlsx

Nội dung: số tuyển sinh theo cơ sở × chương trình × tháng, breakdown theo khoá
học, sheet tổng hợp có dòng tổng và biểu đồ theo tháng (theo góp ý của anh/chị).

Lưu ý khi đọc số liệu:
- "Tuyển sinh" = học viên đã đóng học phí, tính theo ngày đóng phí
- Dữ liệu từ 01/01/2026 đến 31/10/2026
- Đà Nẵng tháng 09 lấy từ số liệu của admin cơ sở (hệ thống bị lỗi đồng bộ)
- Không bao gồm danh tính học viên

Phần bổ sung (so sánh 2025, doanh thu) team có thể làm sau cuộc họp nếu anh/chị
cần. Sáng mai trước 09:00 team vẫn hỗ trợ nếu cần chỉnh sửa gấp.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #13
```

### 5.7 Follow-up sau cuộc họp (05/11 – 10:30)

```
Subject: RE: Báo cáo tuyển sinh - Follow-up - Ticket #13

Chào anh/chị,

Cảm ơn anh/chị đã phản hồi báo cáo đã đáp ứng nhu cầu cho cuộc họp sáng nay.
Team xin phép đóng Ticket #13.

Nếu anh/chị cần phần bổ sung (so sánh cùng kỳ 2025, doanh thu theo cơ sở) hoặc
cập nhật báo cáo này định kỳ, anh/chị trả lời email này để team mở yêu cầu mới.

Trân trọng,
Nguyễn Thùy Ngọc
MindX Support Team
Ticket #13
```

## 6. Trend Analysis

- Báo cáo tuyển sinh là nhu cầu định kỳ → đề xuất dashboard tự phục vụ (filter cơ sở / chương trình / thời gian) để giảm yêu cầu gấp.
- Báo Dev lỗi đồng bộ CRM của cơ sở Đà Nẵng tháng 09 để sửa tận gốc.
- Lưu lại template báo cáo + định nghĩa metric "tuyển sinh = đã đóng học phí" vào KB.

## 7. Reflection

- Làm tốt: hỏi đúng 4 câu để chốt scope ngay ngày đầu; tách rõ MVP và nice-to-have; xin duyệt dữ liệu nhạy cảm trước khi trích xuất; raise vấn đề phát sinh sớm kèm phương án và mốc chuyển phương án dự phòng.
- Khó: cân bằng giữa deadline gấp và quy trình phê duyệt dữ liệu.
- Lần sau: đặt timeline có buffer ngay từ đầu (bản chốt trước deadline ít nhất nửa ngày) và gửi bản nháp sớm để giảm rủi ro hiểu sai yêu cầu.
