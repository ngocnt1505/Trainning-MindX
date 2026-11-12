# Week 5 — Phân tích pattern ticket

Mục tiêu: tìm các vấn đề lặp lại trong ticket Technical Support, đo mức ảnh hưởng và chọn vấn đề phù hợp để tự động hóa.

## 1. Nguồn dữ liệu

| Hạng mục | Giá trị |
| --- | --- |
| File | [data/sample.xlsx](data/sample.xlsx) — export Helpdesk Odoo, team Technical Support |
| Tổng số dòng ticket | 131 |
| Loại bỏ | 12 ticket *Cancelled* (đều là ticket test) + #58 "Tech test email 1" |
| **Dữ liệu phân tích** | **118 ticket** |
| Các trường có | Tiêu đề, khách hàng, tags, mức ưu tiên, giai đoạn |
| Các trường **không** có | Ngày tạo/đóng, thời gian xử lý, mô tả, người xử lý (chỉ 2 ticket có) |

## 2. Phương pháp

1. **Làm sạch**: export của Odoo nhóm ticket theo giai đoạn (`New (6)`, `Resolved (91)`...) và tách mỗi tag thêm ra một dòng riêng. Script chuyển dòng nhóm thành cột `stage` và gộp tag về đúng ticket.
2. **Phân nhóm theo tiêu đề**: bỏ dấu tiếng Việt, tìm từ khóa (VD `tms|cham cong|bu cong` → *TMS / Chấm công*). Luật đầu tiên khớp được dùng.
3. **Đọc lại và sửa tay** 15 ticket bị xếp nhầm, VD:
   - #295 "BU **cộng điểm**..." bị bắt nhầm thành "bù công" → chuyển sang *Điểm thưởng*.
   - #241, #253, #265 "không vào được TMS / quên mật khẩu TMS" → lỗi **đăng nhập**, không phải lỗi chấm công.
   - #286, #288 "sửa tên trong enrollment" → sai *thông tin học viên*, không phải lỗi enroll.
4. **Đo ảnh hưởng** mỗi nhóm: số ticket, số người gửi khác nhau, số ticket Urgent/High, số ticket chưa xử lý xong.

Chạy lại (chỉ cần Python, không cần thư viện ngoài):

```
python reports/classify_tickets.py
```

Kết quả: [reports/tickets-classified.csv](reports/tickets-classified.csv) (từng ticket + nhóm) và [reports/group-summary.csv](reports/group-summary.csv) (tổng hợp).

## 3. Tổng quan

| Giai đoạn | Số ticket | | Mức ưu tiên | Số ticket |
| --- | --- | --- | --- | --- |
| Resolved | 91 | | Urgent | 40 |
| First Response Sent | 17 | | High | 42 |
| New | 5 | | Medium | 8 |
| In Progress | 5 | | Low | 28 |

## 4. Top 5 vấn đề lặp lại

| # | Nhóm | Ticket | % | Người gửi khác nhau | Urgent + High | Chưa xong |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Lead / Thanh toán / Order (CRM) | 24 | 20% | 19 | 18 | 8 |
| 2 | Enroll / Xếp lớp học viên | 20 | 17% | 14 | 15 | 4 |
| 3 | TMS / Chấm công / Điểm danh | 19 | 16% | 18 | 15 | 0 |
| 4 | Không đăng nhập được / quên mật khẩu / bị khóa | 14 | 12% | 8 | 7 | 2 |
| 5 | Cấp mới / chuyển tài khoản, email | 8 | 7% | 7 | 7 | 2 |

Nhóm nhỏ hơn: Thông tin học viên 7 · Hợp đồng điện tử 7 · Điểm thưởng 5 · CRM gọi điện/SMS 4 · Dropout 4 · Đặt phòng 4 · Khác 2.

**5 nhóm đầu chiếm 85/118 ticket (72%).**

Ví dụ tiêu đề mỗi nhóm:

- **Lead / Thanh toán**: "Lỗi Add payment" (#226), "Hỗ trợ gỡ payment" (#125, #186), "chuyển đổi trạng thái Lead" (#46, #150, #187, #245), "Lead kế toán báo không Confirmed được" (#305).
- **Enroll**: "KHÔNG THỂ ENROLL HỌC VIÊN" (#267, #274), "LỖI ENROLL" (#47, #224), "Không add được GV vào lớp" (#37, #290).
- **TMS**: "TMS không hiển thị công" (#228, #232, #238), "Lỗi phần mềm chấm công" (#152, #194), "Lỗi khi yêu cầu bù công" (#215, #235).
- **Đăng nhập**: "LỖI ĐĂNG NHẬP HỆ THỐNG NỘI BỘ" (#162, #165), "Tài khoản E Count bị khoá" (#220), "cấp lại mật khẩu LMS cho giáo viên" (#41), "Không đăng nhập được CRM" (#143).
- **Cấp tài khoản**: "CẤP TÀI KHOẢN NHÂN SỰ I4137" (#248), "CẤP MAIL OUTLOOK" (#174, #230), "chuyển tài khoản LMS/CRM từ STL sang CSL" (#276).

## 5. Phát hiện thêm

### 5.1 Lỗi TMS có dấu hiệu là một sự cố chung bị báo thành nhiều ticket

10 ticket TMS nằm trong dải số **#227 → #239** (13 số liên tiếp), cùng nội dung "không hiển thị công / không hiện thông tin", có ticket ghi rõ "**lỗi TMS từ ngày 31**" (#233, #234). Đây nhiều khả năng là **một sự cố toàn hệ thống vào cuối tháng** (lúc duyệt công), nhưng được xử lý như 10 ticket Standard riêng lẻ. Theo Class of Service ở Week 4, đáng ra nên gộp thành 1 ticket chính mức Priority/Expedite.

### 5.2 Ticket trùng lặp

Ít nhất **9 cặp** ticket cùng người gửi, cùng nội dung:

| Cặp | Nội dung |
| --- | --- |
| #286 / #288 | Sửa tên HV trong enrollment |
| #72 / #336 | BU PXL không tạo được phiếu dropout |
| #104 / #296 | Số lượng Ecount và Denise không khớp |
| #174 / #230 | Cấp mail Outlook |
| #233 / #234 | Lỗi TMS từ ngày 31 |
| #260 / #318 | CRM không bấm gọi được |
| #267 / #274 | Không thể enroll học viên |
| #243 / #246 | Lỗi enroll lớp HDT-JSB75 |
| #125 / #186 | Hỗ trợ gỡ payment |

→ 9 ticket (8%) có thể tránh được. Một số cặp là **lỗi tái phát sau khi đã đóng** (VD #72 rồi #336, #260 rồi #318), cho thấy lần đầu chỉ xử lý triệu chứng.

### 5.3 Chất lượng phân loại thấp

- **52/118 ticket (44%) không có tag hệ thống nào** (không có CRM/LMS/TMS...), nên report theo tag trên Odoo bị thiếu gần một nửa.
- **82/118 ticket (69%) là Urgent hoặc High**: mức ưu tiên đang bị đánh quá tay, mất tác dụng phân loại.
- **10 ticket** chuyển tiếp từ Freshdesk có khách hàng là `support@mindx-help.freshdesk.com` → mất thông tin người gửi thật.
- Chỉ **2/118** ticket có người được giao → chưa đo được hiệu suất team.

## 6. Nguyên nhân gốc của 3 vấn đề đầu

> Dữ liệu không có mô tả ticket nên dưới đây là **giả thuyết** dựa trên tiêu đề, cần xác minh với team vận hành hoặc team dev.

| Vấn đề | Giả thuyết nguyên nhân | Bằng chứng | Đề xuất |
| --- | --- | --- | --- |
| **Lead / Thanh toán** (24) | Quy trình payment → confirm → chuyển trạng thái lead không tự chạy đúng; BU không tự sửa được khi nhập sai (add trùng, sai giá) | Lead "đã add payment vẫn nằm ở L5A" (#225); 4 ticket chỉ xin "chuyển trạng thái lead"; nhiều ticket "gỡ / hủy payment" (#125, #186, #249, #278) | Báo dev kiểm tra luồng tự chuyển trạng thái; cho phép kế toán tự hủy payment trong giới hạn; viết KB "xử lý payment nhập sai" |
| **Enroll** (20) | BU không tìm thấy lớp hoặc lớp hết slot; thiếu hướng dẫn tự enroll | "Không tìm ra lớp" (#246, #290), "mở slot enroll" (#60), "không có slot học phần" (#39); BU Thủ Dầu Một gửi 3 ticket enroll (#47, #61, #224) | Viết KB "các bước enroll + lỗi thường gặp"; kiểm tra quy tắc mở slot |
| **TMS** (19) | Sự cố hệ thống cuối tháng (5.1) cộng lỗi tính công | 10 ticket dồn trong #227–#239; "đi đúng ca nhưng bị báo đi trễ" (#152) | Gộp sự cố thành 1 ticket; báo dev root cause; trang thông báo sự cố để giáo viên không phải gửi ticket |

## 7. Vấn đề được chọn để tự động hóa: Đăng nhập / tài khoản bị khóa

- **Đủ nhiều**: 14 ticket (12%). Tính cả nhóm cấp/chuyển tài khoản thì **22 ticket (19%)**, ngang nhóm lớn nhất.
- **Quy trình xử lý lặp lại và rõ ràng**: kiểm tra HR → mở lại tài khoản hoặc ghi chú → trả lời (Scenario 1, Week 4).
- **Tốn thời gian tay**: 5–10 phút/ticket theo đề → 14 ticket ≈ **70–140 phút** chỉ để làm việc lặp lại.
- **Nguyên nhân gốc** (khóa tài khoản sau 30 ngày không dùng) nằm trong code, cần team dev sửa → phù hợp cách làm Operating Engineer: tự động hóa trước, đề xuất sửa code sau.
- **Giới hạn cần biết**: 4/14 ticket (#141, #222, #255, #294) là tài khoản **học viên** trên Denise, không có trong HR → automation phải chuyển cho người xử lý. Các ticket từ Freshdesk thiếu email người gửi → cũng phải chuyển cho người xử lý.
- **Kiểm chứng trên dữ liệu thật** ([TEST-RESULTS.md](TEST-RESULTS.md) mục 4): bộ phân loại của bot nhận đúng 11/14 ticket đăng nhập, không báo nhầm ticket nào; nhưng chỉ 4 ticket là LMS → cần mở rộng sang TMS/Ecount ([action-plan.md](action-plan.md) A2).

Thiết kế và code: [automation.md](automation.md).

## 8. Khuyến nghị

1. **Tự động hóa ticket đăng nhập** của nhân sự (mục 7).
2. **Gộp sự cố**: khi ≥ 3 ticket cùng hệ thống trong thời gian ngắn → tạo 1 ticket sự cố chính, các ticket khác đánh dấu trùng (như S05 ở Week 4).
3. **Bắt buộc chọn tag hệ thống** khi tạo ticket để report theo danh mục có ý nghĩa.
4. **Chuẩn hóa mức ưu tiên** theo Class of Service (số người bị ảnh hưởng), không theo cảm nhận của người gửi.
5. **Viết KB** cho 3 nhóm lớn (payment, enroll, TMS) để BU tự xử lý các ca đơn giản.

Kế hoạch chi tiết (người phụ trách, thời hạn, chỉ số đo): [action-plan.md](action-plan.md).

## 9. Report trên Odoo

118 ticket được import vào Odoo Helpdesk (`choi.odoo.com`) từ [reports/odoo-import.csv](reports/odoo-import.csv), mỗi ticket có tag `week5-sample` và tag nhóm `grp-*` ([w5-00-import-118.pdf](images/w5-00-import-118.pdf)). Report làm ở **Hỗ trợ → Báo cáo → Phân tích phiếu hỗ trợ**, lưu vào *Yêu thích*.

| Report | Thiết lập | Kết quả | Bằng chứng |
| --- | --- | --- | --- |
| Tổng hợp ticket | Lọc `week5-sample` · biểu đồ cột theo Giai đoạn | 5 Mới · 22 Đang thực hiện · 91 Đã xử lý = 118 | [w5-01-summary.pdf](images/w5-01-summary.pdf) |
| Tổng hợp toàn helpdesk | Pivot Giai đoạn × Mức độ ưu tiên, **không lọc** | 126 = 118 ticket mẫu + 8 ticket Week 4 (2 ticket *Đã hủy* là ticket trùng #11, #12 của S05) | [w5-01-summary-pivot.pdf](images/w5-01-summary-pivot.pdf) |
| Theo nhóm vấn đề | Lọc `week5-sample` · Pivot theo Thẻ | grp-lead-payment 24 · grp-enroll 20 · grp-tms 19 · grp-login 14 · grp-account 8… — khớp mục 4 | [w5-02-category.pdf](images/w5-02-category.pdf) |
| Hiệu suất team | Phân công cho × Giai đoạn, toàn helpdesk (đọc qua API) | Bảng dưới | — |
| Xu hướng số lượng | Lọc `week5-sample` · Cohort theo Ngày tạo | Cả 118 ticket cùng ngày tạo 11/11/2026 (ngày import) → không có xu hướng thật | [w5-04-trend.pdf](images/w5-04-trend.pdf) |

Hiệu suất team (toàn bộ 126 ticket trên Odoo, đọc qua API ngày 11/11/2026):

| Phân công cho | Mới | Đang thực hiện | Đã xử lý | Đã hủy | Tổng |
| --- | --- | --- | --- | --- | --- |
| Nguyễn Thúy Ngọc | | | 6 | | 6 |
| (Chưa giao) | 5 | 22 | 91 | 2 | 120 |

→ 120/126 ticket chưa có người được giao: report hiệu suất team **chưa có ý nghĩa** cho tới khi bắt buộc phân công khi nhận ticket (khớp phát hiện 5.3).

## 10. Hạn chế

- Không có ngày tạo ticket → **không làm được report xu hướng theo thời gian** từ file này (report Cohort ở mục 9 xác nhận điều này); nhận định ở 5.1 dựa trên số ticket liên tiếp.
- File import **không có cột "Phân công cho"** (file gốc chỉ có 2/118 ticket có người được giao, đều là người không có tài khoản trên Odoo trial).
- Không có thời gian xử lý → thời gian team tốn chỉ ước tính được cho nhóm đăng nhập (theo đề bài).
- Phân nhóm dựa trên **tiêu đề**; ticket có tiêu đề mơ hồ (#189 "SALE", #209 "TK-ROB-SEMII03") được xếp theo tag hoặc mã lớp, có thể sai.
