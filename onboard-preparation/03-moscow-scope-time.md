# MoSCoW và các framework quản lý scope / thời gian

Nguyễn Thúy Ngọc · 20/11/2026

## 1. What: MoSCoW là gì

MoSCoW là cách **phân loại yêu cầu theo mức độ bắt buộc** trong một khoảng thời gian cố định. Phương pháp do Dai Clegg (Oracle) đặt ra năm 1994, sau đó trở thành một phần của DSDM (Agile). Tên gồm 4 chữ cái đầu, chữ "o" chỉ để dễ đọc:

| Nhóm | Nghĩa | Câu hỏi để kiểm tra |
| --- | --- | --- |
| **M**ust have | Thiếu thì bản giao **vô nghĩa**, không an toàn hoặc sai quy định | "Không có cái này thì có nên giao không?" → Không giao được thì là Must |
| **S**hould have | Quan trọng, nhưng thiếu thì **vẫn có cách tạm** (workaround) | "Có cách làm tay / tạm thời không?" → Có thì là Should |
| **C**ould have | Có thì tốt, ảnh hưởng nhỏ | "Bỏ đi thì có ai phàn nàn nhiều không?" → Không thì là Could |
| **W**on't have (this time) | Đã thống nhất **không làm lần này** | Ghi rõ ra để không ai mong đợi, và để dành cho lần sau |

## 2. Why: vì sao cần

Trong một dự án có 3 thứ kéo nhau: **phạm vi, thời gian, nguồn lực**. Ở công ty, thời gian thường cố định ("lên production trong 2 tuần") và nguồn lực cũng cố định (chỉ có mình). Vậy thứ duy nhất được phép co giãn là **phạm vi**. MoSCoW cho biết khi phải co thì bỏ cái gì trước.

- Tránh tình trạng làm được 80 % của mọi thứ nhưng không có gì dùng được.
- Thống nhất trước với người yêu cầu nên lúc cắt scope không bị coi là thất hứa.
- Nhóm *Won't* chặn **scope creep** (yêu cầu cứ thêm dần trong lúc làm).

## 3. How it works: các bước

1. **Chốt mục tiêu và timebox.** Ví dụ: "Bot tự xử lý ticket đăng nhập LMS, lên production sau 10 ngày làm việc."
2. **Liệt kê hết yêu cầu,** chưa phân loại.
3. **Ước lượng công** cho từng yêu cầu (ngày người).
4. **Phân loại,** bắt đầu từ giả định *mọi thứ là Won't*, rồi chứng minh vì sao từng cái phải được nâng lên.
5. **Kiểm tra tỷ lệ** (khuyến nghị của DSDM): Must **≤ 60 %** tổng công, Should ~20 %, Could ~20 %. Phần Should và Could chính là **khoảng đệm**: trễ thì bỏ Could, rồi tới Should, còn Must vẫn kịp.
6. **Thống nhất** với người yêu cầu (mentor / quản lý), rồi ghi lại.
7. **Trong lúc làm:** có yêu cầu mới thì phải phân loại lại. Thêm một Must thì phải bỏ hoặc hạ một Must khác.

Lỗi hay gặp:
- Mọi thứ đều là Must. Khi đó MoSCoW không còn tác dụng gì.
- Không ghi *Won't*, nên người yêu cầu vẫn nghĩ là sẽ có.
- Phân loại một lần rồi không xem lại khi tình hình thay đổi.

## 4. Ví dụ 1: feature của login bot (tuần 5) trong 2 tuần

Giả sử ở tuần 5 đi làm, cải tiến được chọn là login bot. Timebox là **10 ngày làm việc**, gồm cả việc lên production.

| # | Feature | Công | Nhóm | Lý do |
| --- | --- | --- | --- | --- |
| 1 | Nhận diện ticket lỗi đăng nhập LMS (từ khóa) | 1 | **Must** | Không nhận diện được thì bot không làm gì |
| 2 | Kiểm tra trạng thái nhân sự trong HR theo email | 1 | **Must** | Là điều kiện an toàn để quyết định mở tài khoản |
| 3 | HR active + LMS bị khóa → mở lại tài khoản | 1 | **Must** | Đây là giá trị chính, chiếm phần lớn ticket đăng nhập |
| 4 | Nghỉ việc / không có trong HR / không rõ → chuyển người xử lý, **không** tự mở | 0,5 | **Must** | Thiếu thì bot có thể mở tài khoản cho người đã nghỉ: không an toàn |
| 5 | Ghi note + tag lên ticket Odoo | 1 | **Must** | Không có thì team không biết bot đã làm gì |
| 6 | Không xử lý lại ticket đã xử lý | 0,5 | **Must** | Thiếu thì bot mở tài khoản / gửi mail lặp lại |
| 7 | Chế độ dry-run để chạy thử trên dữ liệu thật | 0,5 | **Must** | Lên production an toàn (tuần 5 đã nhờ nó bắt được lỗi bot đụng vào ticket tuần 4) |
| 8 | Gửi email trả lời người dùng tự động | 1 | Should | Workaround: kỹ thuật viên gửi theo mẫu có sẵn |
| 9 | HR active + LMS đang mở → gửi link đặt lại mật khẩu | 0,5 | Should | Workaround: chuyển người xử lý |
| 10 | Thử lại khi HR/LMS lỗi tạm thời | 0,5 | Should | Workaround: ticket lỗi được chuyển người, lần chạy sau thử lại |
| 11 | Webhook xử lý ngay khi có ticket | 1 | Could | Polling 5 phút/lần là đủ cho Class Standard |
| 12 | Script thống kê kết quả bot | 0,5 | Could | Xem được bằng report Odoo theo tag `auto-*` |
| 13 | Đăng nhập TMS / Ecount / Mail | — | Won't | Mỗi hệ thống là một adapter mới, để đợt sau (A2) |
| 14 | Tài khoản học viên / phụ huynh | — | Won't | Không có trong HR, luồng khác hẳn |
| 15 | Nhận diện bằng AI thay cho từ khóa | — | Won't | Từ khóa đã đạt precision 100 % |
| 16 | Cảnh báo trước 3 ngày khi sắp khóa (A3) | — | Won't | Thuộc team dev, chỉ gửi đề xuất |

**Kiểm tra tỷ lệ:** Must = 5,5 ngày (55 %). Should = 2 ngày, Could = 1,5 ngày. Còn 1 ngày dự phòng cho deploy và sự cố → đạt.

**Khi bị trễ:** ngày 6 mà Must chưa xong thì bỏ #11, #12, rồi tới #10. Không cắt #4, #6, #7 vì đó là phần an toàn.

## 5. Ví dụ 2: tuần 4, scenario 06 (báo cáo Fixed Deadline)

Ở [scenario 06](../week-4-odoo-helpdesk/scenario-06-deadline.md), mình đã chia scope thành MVP / Nice-to-have / Không lấy. Đó chính là MoSCoW:

| Hạng mục | Đã ghi | Theo MoSCoW |
| --- | --- | --- |
| Số tuyển sinh theo cơ sở × chương trình × tháng, breakdown theo khóa | MVP | Must |
| So sánh cùng kỳ 2025 | Nice-to-have | Should (có ích cho cuộc họp, làm sau bản nháp) |
| Doanh thu theo cơ sở | Nice-to-have | Could (cần thêm duyệt) |
| Tỷ lệ hoàn thành khóa học | Nice-to-have | Could (dữ liệu nằm ở nguồn khác) |
| Danh tính học viên / phụ huynh | Không lấy | Won't (tránh lộ PII) |

Bài học: với yêu cầu có deadline cứng, việc **đầu tiên** là hỏi để chốt Must, không phải bắt tay làm ngay.

## 6. Các framework khác hữu ích

MoSCoW trả lời câu hỏi *"trong việc này, làm phần nào"*. Các framework dưới đây trả lời những câu hỏi còn lại.

| Framework | Trả lời câu hỏi | Cách làm ngắn gọn | Dùng khi nào |
| --- | --- | --- | --- |
| **Impact / Effort matrix** | Chọn **vấn đề nào** để cải tiến? | Đặt mỗi ý tưởng vào ma trận 2×2: tác động cao/thấp × công sức cao/thấp. Làm ô *tác động cao + công thấp* trước (quick win) | Tuần 5 đi làm: chọn 1 cải tiến từ danh sách |
| **RICE** | Như trên, nhưng có điểm số | Điểm = Reach × Impact × Confidence ÷ Effort | Khi có nhiều ý tưởng và cần lý do bằng số để thuyết phục |
| **WBS** (Work Breakdown Structure) | Việc gồm những phần nào? | Chia việc lớn thành việc nhỏ ≤ 1 ngày | Trước khi ước lượng và làm MoSCoW |
| **Ước lượng 3 điểm (PERT)** | Mất bao lâu? | (Lạc quan + 4 × Bình thường + Bi quan) ÷ 6 | Khi chưa chắc về công, tránh ước lượng quá lạc quan |
| **Timeboxing** | Làm đến bao giờ thì dừng? | Cố định thời gian, co phạm vi (đi cùng MoSCoW) | Cả 2 tuần cải tiến, và cả từng việc nhỏ trong ngày |
| **Eisenhower matrix** | Hôm nay làm việc gì trước? | Khẩn cấp × quan trọng → làm ngay / lên lịch / giao người khác / bỏ | Quản lý thời gian cá nhân khi vừa xử lý ticket vừa làm cải tiến |
| **Change control** | Có yêu cầu mới giữa chừng thì sao? | Ghi lại → đánh giá ảnh hưởng tới timebox → phân loại MoSCoW → được duyệt mới làm | Chống scope creep |

Lưu ý: ở tuần 4, **Class of Service** (Standard / Priority / Expedite / Fixed Deadline) là cách ưu tiên **ticket**. Còn MoSCoW và các framework trên là cách ưu tiên **việc trong một dự án**. Hai thứ dùng song song: ticket Expedite đến giữa 2 tuần cải tiến thì xử lý ticket trước, rồi xem lại MoSCoW xem có phải cắt bớt gì không.

## 7. Áp dụng: quy trình 2 tuần cải tiến 

| Bước | Framework | Kết quả |
| --- | --- | --- |
| 1. Chọn vấn đề từ số liệu ticket tháng đầu | Impact / Effort hoặc RICE | 1 vấn đề + lý do bằng số |
| 2. Chia giải pháp thành việc nhỏ | WBS | Danh sách việc ≤ 1 ngày |
| 3. Ước lượng | 3 điểm | Công cho từng việc |
| 4. Cắt scope cho vừa 10 ngày | MoSCoW + Timeboxing | Must ≤ 60 %, có Won't ghi rõ |
| 5. Thống nhất với mentor | | Scope được duyệt |
| 6. Làm hằng ngày | Eisenhower, daily report | Biết hôm nay làm gì, báo tiến độ Must |
| 7. Yêu cầu mới phát sinh | Change control | Không bị trễ vì scope creep |

## Tài liệu tham khảo

1. DSDM / Agile Business Consortium, *MoSCoW Prioritisation*, agilebusiness.org
2. PMI, *A Guide to the Project Management Body of Knowledge (PMBOK Guide)*: WBS, ước lượng 3 điểm, change control
3. Sean McBride (Intercom), *RICE: Simple prioritization for product managers* (2016)
