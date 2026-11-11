# Kết quả kiểm tra — Week 5

Tài liệu này ghi lại kết quả chạy thật để người đọc kiểm chứng được mà không cần tự chạy lại. Lệnh tái hiện ghi ở từng mục.

| | |
| --- | --- |
| Ngày chạy | 2026-11-11 |
| Python | 3.13.1 (chỉ dùng thư viện chuẩn) |
| Hệ điều hành | Windows 11 |
| Commit gốc | `48c955e` + thay đổi Week 5 (chưa commit lúc chạy) |

## 1. Tóm tắt

| Hạng mục | Kết quả |
| --- | --- |
| Unit + integration test (`python -m unittest -v`) | **51 / 51 pass** (khoảng 14 giây) |
| Demo end-to-end offline (`python -m login_bot.run --demo`) | **8 / 8 nhánh đúng kết quả mong đợi**; lần chạy 2 không xử lý lại ticket nào |
| Webhook (test HTTP thật) | Payload Odoo → xử lý; gọi lại → `already_processed`; token sai → 401 |
| Bộ phân loại trên 118 ticket thật | **Precision 100 %, Recall 79 %** (mục 4) |
| Phân tích dữ liệu (`python docs4/reports/classify_tickets.py`) | Tái tạo đúng 118 ticket, 12 nhóm |
| End-to-end với Odoo thật (ticket #250–#257) | **8 / 8 đúng**; chạy lại → 0 ticket; ticket Week 4 không bị đụng tới (mục 6) |

## 2. Test tự động

```
cd automation
python -m unittest -v
```

| File | Số test | Kiểm tra gì |
| --- | --- | --- |
| `test_classifier.py` | 9 | Nhận diện lỗi đăng nhập (VN/EN, tiêu đề thật trong sample), hệ thống, tài khoản học viên |
| `test_workflow.py` | 17 | Từng dòng của bảng quyết định; HR/LMS/Odoo lỗi; không xử lý lặp; dry-run; log JSON; email thật vs bản nháp |
| `test_services.py` | 7 | Client HTTP với mock HR/LMS thật; không phân biệt hoa thường email; thử lại khi mất kết nối |
| `test_odoo_client.py` | 10 | Gọi đúng External API: domain lọc ticket, tạo note, gửi email, gắn tag, đổi giai đoạn, sai API key |
| `test_end_to_end.py` | 8 | Polling qua HTTP với 8 ticket demo; thống kê từ log; HR sập; webhook HTTP (200/400/401/404, gọi lặp) |

Output:

```
test_english_ticket_is_detected ... ok
test_non_login_tickets_from_sample_are_ignored ... ok
test_other_systems_are_out_of_scope ... ok
test_real_subjects_from_sample_are_login_issues ... ok
test_scenario_1_email_is_an_lms_login_issue ... ok
test_student_accounts_are_out_of_scope ... ok
test_subject_system_wins_over_description ... ok
test_system_without_name_is_in_scope ... ok
test_removes_vietnamese_accents_and_lowercases ... ok
test_hr_down_marks_ticket_failed ... ok
test_polling_run_handles_every_branch ... ok
test_stats_from_log ... ok
test_missing_id_is_bad_request ... ok
test_odoo_payload_triggers_processing ... ok
test_repeated_webhook_does_not_process_twice ... ok
test_unknown_ticket_is_not_found ... ok
test_wrong_token_is_rejected ... ok
test_empty_description ... ok
test_round_trip ... ok
test_add_tags_creates_missing_tag_and_links_it ... ok
test_fetch_only_new_tickets_excluding_processed_and_sample ... ok
test_missing_stage_raises ... ok
test_note_falls_back_to_message_post ... ok
test_note_is_created_as_internal_html_message ... ok
test_send_email_posts_comment_to_customer ... ok
test_set_stage_uses_stage_id ... ok
test_wrong_api_key_raises_clear_error ... ok
test_hr_lookup_ignores_email_case ... ok
test_hr_returns_employee_status ... ok
test_password_reset_returns_link ... ok
test_reactivate_changes_account_status ... ok
test_reactivating_unknown_account_raises ... ok
test_unknown_email_returns_none ... ok
test_unreachable_service_raises_after_retries ... ok
test_dry_run_changes_nothing ... ok
test_email_is_sent_through_odoo_when_enabled ... ok
test_every_decision_is_logged_as_json ... ok
test_ticket_is_processed_only_once ... ok
test_active_employee_with_active_account_gets_password_reset_only ... ok
test_active_employee_with_deactivated_account_is_reactivated ... ok
test_employee_without_lms_account_is_escalated ... ok
test_hr_outage_fails_safely ... ok
test_lms_outage_fails_safely ... ok
test_non_login_ticket_is_only_tagged ... ok
test_odoo_outage_leaves_ticket_for_next_run ... ok
test_other_system_is_escalated_without_calling_hr ... ok
test_reply_to_terminated_employee_does_not_reveal_hr_status ... ok
test_student_account_is_escalated ... ok
test_terminated_employee_is_never_reactivated ... ok
test_ticket_without_email_is_escalated_and_gets_no_email ... ok
test_unknown_email_in_hr_is_escalated ... ok

----------------------------------------------------------------------
Ran 51 tests in 13.950s

OK
```

Lần chạy đầu có 2 test lỗi do **logger trong test chưa đặt mức INFO** nên không ghi log (lỗi ở code test, không phải ở bot); đã sửa và chạy lại toàn bộ.

## 3. Demo end-to-end offline

```
cd automation
python -m login_bot.run --demo
```

Mock HR/LMS chạy qua HTTP thật; Odoo là bản giả lập trong bộ nhớ. Bộ 8 ticket ([demo_data.py](../automation/login_bot/demo_data.py)) phủ mọi nhánh của bảng quyết định:

```
Lần chạy 1:
  #1     reactivated        HR active + LMS deactivated
  #2     password_reset     HR active + LMS active
  #3     terminated         nhân sự đã nghỉ việc - KHÔNG mở lại tài khoản, cần quản lý xác nhận
  #4     escalated          không tìm thấy unknown.user@example.com trong HR
  #5     escalated          đăng nhập TMS - ngoài phạm vi bot (chỉ xử lý LMS)
  #6     escalated          tài khoản học viên/phụ huynh - không có trong HR
  #7     escalated          nhân sự active nhưng chưa có tài khoản LMS - cần cấp mới
  #8     not_login          không phải lỗi đăng nhập
  => 8 ticket: escalated 4, not_login 1, password_reset 1, reactivated 1, terminated 1

Kiểm tra với kết quả mong đợi:
  OK  #1 Không thể đăng nhập vào LMS                   mong đợi reactivated, thực tế reactivated
  OK  #2 Quên mật khẩu LMS                             mong đợi password_reset, thực tế password_reset
  OK  #3 LMS báo tài khoản bị khóa                     mong đợi terminated, thực tế terminated
  OK  #4 Không đăng nhập được LMS                      mong đợi escalated, thực tế escalated
  OK  #5 BU KHÔNG ĐĂNG NHẬP VÀO TMS ĐƯỢC               mong đợi escalated, thực tế escalated
  OK  #6 PNL HỖ TRỢ TÀI KHOẢN DENISE - HV không đăng n mong đợi escalated, thực tế escalated
  OK  #7 Không đăng nhập được LMS lần đầu              mong đợi escalated, thực tế escalated
  OK  #8 KHÔNG THỂ ENROLL HỌC VIÊN                     mong đợi not_login, thực tế not_login

Lần chạy 2 (phải không xử lý lại ticket nào):
  => 0 ticket: không có ticket mới
```

Những gì bot ghi lên ticket #1 (đúng Scenario 1 của Week 4):

```
[#1 tags] auto-processed, auto-reactivated
[#1 note] [LOGIN-BOT] 2026-11-11 21:42 - ĐÃ MỞ LẠI TÀI KHOẢN
          - Phân loại: lỗi đăng nhập (từ khóa: dang nhap, mat khau, password) - hệ thống: LMS
          - HR: nguyen.van.a@example.com - active (Giáo viên - HN)
          - LMS: deactivated (đăng nhập lần cuối 2026-09-25)
          - Đã reactivate tài khoản LMS
          - Đã gửi link đặt lại mật khẩu
          - Bước tiếp theo: chờ user xác nhận đăng nhập được rồi đóng ticket
[#1 note] [EMAIL GỬI USER - bản nháp, LOGIN_BOT_SEND_EMAIL=false]
          To: nguyen.van.a@example.com
          Subject: RE: Không thể đăng nhập vào LMS - Ticket #1
          Chào Nguyễn Văn A,
          Team đã kiểm tra và thấy tài khoản LMS của bạn bị tạm khóa do không đăng nhập trong 30 ngày.
          Sau khi xác nhận thông tin nhân sự, team đã mở lại tài khoản và gửi link đặt lại mật khẩu vào email này.
          ...
[#1 stage] Waiting Customer
```

Ticket #3 (nhân sự đã nghỉ việc): ghi chú `NHÂN SỰ ĐÃ NGHỈ VIỆC - CẦN NGƯỜI XEM LẠI`, **tài khoản vẫn deactivated**, chuyển *Escalated*; email cho user chỉ xác nhận đã nhận, không nêu trạng thái HR.

Thống kê từ log của lần demo (`python -m login_bot.stats`):

```json
{
  "tickets_checked": 8,
  "login_tickets": 7,
  "automated": 2,
  "automation_rate": 0.29,
  "by_outcome": {"reactivated": 1, "password_reset": 1, "terminated": 1, "escalated": 4, "not_login": 1},
  "avg_bot_seconds": 0.1,
  "manual_minutes_saved": [10, 20]
}
```

Bộ demo cố ý có nhiều ca phải chuyển người để kiểm tra từng nhánh, nên tỷ lệ 29 % ở đây **không** phải tỷ lệ thực tế.

## 4. Bộ phân loại trên dữ liệu thật

```
cd automation
python evaluate_classifier.py
```

So kết quả của `classifier.py` (chỉ dùng tiêu đề) với nhãn do người phân loại trong [reports/tickets-classified.csv](reports/tickets-classified.csv):

```
Ticket: 118 | nhãn lỗi đăng nhập: 14
Đúng (TP): 11 | Báo nhầm (FP): 0 | Bỏ sót (FN): 3
Precision: 100% | Recall: 79%
  Bỏ sót: #222 HỖ TRỢ LINK BÀI TẬP CHO BÉ LỚP GA28  [Không đăng nhập được / quên mật khẩu / bị khóa]
  Bỏ sót: #294 PNL HỖ TRỢ TÀI KHOẢN DENISE  [Không đăng nhập được / quên mật khẩu / bị khóa]
  Bỏ sót: #141 Fwd: NPS | Hỗ trợ tài khoản Denise của HV |  [Không đăng nhập được / quên mật khẩu / bị khóa]
Ticket bot nhận là lỗi đăng nhập sẽ đi nhánh:
    4  bot xử lý (LMS / không ghi rõ hệ thống)
    3  hệ thống TMS -> chuyển người
    2  hệ thống ECOUNT -> chuyển người
    1  hệ thống MAIL -> chuyển người
    1  hệ thống CRM -> chuyển người
```

Nhận xét:

- **Không báo nhầm** → bot không đụng vào ticket không liên quan (rủi ro lớn nhất của automation).
- 3 ticket bỏ sót đều là **tài khoản học viên trên Denise**, tiêu đề không có từ "đăng nhập". Bot gắn tag `auto-processed` và để nguyên giai đoạn, người xử lý vẫn thấy và xử lý như bình thường.
- Chỉ 4/11 ticket thuộc phạm vi LMS → lý do đề xuất mở rộng connector TMS/Ecount ([automation.md](automation.md) mục 9, [action-plan.md](action-plan.md)).

## 5. Phân tích dữ liệu

```
python docs4/reports/classify_tickets.py
```

Ra đúng 118 ticket, 12 nhóm như [analysis.md](analysis.md) mục 4, và file `odoo-import.csv` 118 dòng.

## 6. End-to-end với Odoo thật

Chạy ngày 2026-11-11 trên `choi.odoo.com` (Odoo 20.0+e) với mock HR/LMS ở cổng 8090.

```
python -m login_bot.run --check-odoo        # server 20.0+e, uid 2, tìm thấy giai đoạn Waiting Customer / Escalated
python -m login_bot.mock_services           # cửa sổ riêng
python -m login_bot.seed_odoo               # tạo ticket #250–#257
python -m login_bot.run --once --dry-run    # 23:21 - xem trước, không ghi gì
python -m login_bot.run --once              # 23:23 - chạy thật
python -m login_bot.run --once              # 23:23 - chạy lại
```

Ảnh terminal: [kết nối Odoo](images/w5-term-01-check-odoo.png) · [tạo ticket #250–#257](images/w5-term-02-seed-odoo.png).

Output chạy thật:

```
23:23:01 - chạy xong:
  #250   reactivated        HR active + LMS deactivated
  #251   password_reset     HR active + LMS active
  #252   terminated         nhân sự đã nghỉ việc - KHÔNG mở lại tài khoản, cần quản lý xác nhận
  #253   escalated          không tìm thấy unknown.user@example.com trong HR
  #254   escalated          đăng nhập TMS - ngoài phạm vi bot (chỉ xử lý LMS)
  #255   escalated          tài khoản học viên/phụ huynh - không có trong HR
  #256   escalated          nhân sự active nhưng chưa có tài khoản LMS - cần cấp mới
  #257   not_login          không phải lỗi đăng nhập
  => 8 ticket: escalated 4, not_login 1, password_reset 1, reactivated 1, terminated 1

23:23:10 - chạy xong:
  => 0 ticket: không có ticket mới
```

Kiểm tra lại trên Odoo (đọc qua API sau khi chạy) và trạng thái mock LMS:

| Ticket | Tiêu đề | Mong đợi | Thực tế trên Odoo | Bằng chứng |
| --- | --- | --- | --- | --- |
| #250 | Không thể đăng nhập vào LMS | reactivated → Waiting Customer | ✅ Waiting Customer · `auto-reactivated` · LMS chuyển `active` | [w5-bot-250.pdf](images/w5-bot-250.pdf) |
| #251 | Quên mật khẩu LMS | password_reset → Waiting Customer | ✅ Waiting Customer · `auto-password-reset` | — |
| #252 | LMS báo tài khoản bị khóa | terminated → Escalated, **không mở lại** | ✅ Escalated · `auto-escalated` · LMS vẫn `deactivated` | [w5-bot-252.pdf](images/w5-bot-252.pdf) |
| #253 | Không đăng nhập được LMS | escalated (không có trong HR) | ✅ Escalated | — |
| #254 | BU KHÔNG ĐĂNG NHẬP VÀO TMS ĐƯỢC | escalated (ngoài phạm vi) | ✅ Escalated | [w5-bot-254.pdf](images/w5-bot-254.pdf) |
| #255 | PNL HỖ TRỢ TÀI KHOẢN DENISE - HV… | escalated (học viên) | ✅ Escalated | — |
| #256 | Không đăng nhập được LMS lần đầu | escalated (chưa có tài khoản) | ✅ Escalated | — |
| #257 | KHÔNG THỂ ENROLL HỌC VIÊN | not_login, giữ nguyên giai đoạn | ✅ vẫn ở Mới · chỉ có `auto-processed` | [w5-bot-257.pdf](images/w5-bot-257.pdf) |

- Ghi chú `[LOGIN-BOT]` và bản nháp email được lưu là **ghi chú nội bộ** (subtype *Notes*), xuống dòng đúng, không lộ thẻ HTML.
- Email *"Dear …, Your request has been received"* lúc 23:18 trong chatter là **email tự động của Odoo khi tạo ticket**, không phải của bot.
- Thống kê (`python -m login_bot.stats`): 8 ticket, 7 lỗi đăng nhập, 2 bot tự xử lý, trung bình **0,82 giây/ticket** (gồm cả thời gian gọi Odoo qua mạng).

### Lỗi phát hiện khi chạy thử trên Odoo thật (đã sửa trước khi chạy thật)

| Lỗi | Phát hiện thế nào | Sửa |
| --- | --- | --- |
| Bot lấy cả **8 ticket Week 4 (#6–#13)** vì chỉ loại giai đoạn "gập" trong Kanban, mà *Đã xử lý* không gập → ticket #6 (lỗi đăng nhập Week 4) sẽ bị ghi chú và chuyển Escalated | Đọc danh sách `fetch_unprocessed()` trên Odoo thật trước khi chạy | Chỉ lấy ticket ở giai đoạn **Mới** (`ODOO_STAGE_NEW`); sau khi sửa chỉ còn đúng #250–#257, #6 vẫn *Đã xử lý* |
| Lần `--dry-run` vẫn ghi vào file log → `stats` đếm gấp đôi | Đọc `logs/login_bot.log` sau dry-run | Dry-run dùng logger riêng, không ghi file |

Cả hai lỗi đều không được unit test bắt, vì chúng phụ thuộc cấu hình thật của Odoo — lý do phải chạy `--dry-run` trên hệ thống thật trước khi bật bot.
