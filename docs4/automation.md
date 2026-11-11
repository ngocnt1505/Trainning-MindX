# Login bot — Automation cho Scenario 1: Lỗi đăng nhập

Code: [automation/](../automation/) · Kết quả test: [TEST-RESULTS.md](TEST-RESULTS.md) · Bài KB: [kb-login.md](kb-login.md)

## 1. Vấn đề

| | |
| --- | --- |
| Ticket | Giáo viên/nhân sự không đăng nhập được LMS ("Invalid username or password") |
| Nguyên nhân gốc | Quy tắc trong code: tài khoản **tự bị khóa sau 30 ngày không đăng nhập** |
| Xử lý tay hiện nay | Đọc ticket → kiểm tra HR → mở lại tài khoản + đặt lại mật khẩu (hoặc ghi chú nếu đã nghỉ việc) → email trả lời. **5–10 phút/ticket** |
| Tần suất (dữ liệu thật) | 14/118 ticket (12%) là lỗi đăng nhập; tính cả cấp/chuyển tài khoản là 22 ticket (19%) — [analysis.md](analysis.md) |

## 2. Vì sao chọn automation thay vì sửa code (cách làm Operating Engineer)

| Tiêu chí (tasks.md) | Đánh giá cho lỗi đăng nhập |
| --- | --- |
| Lặp lại, lặp đi lặp lại | ✅ 12% số ticket, cùng một quy trình xử lý |
| Xử lý tay được nhưng tốn thời gian | ✅ 5–10 phút/ticket, đều là thao tác lặp lại |
| Sửa gốc cần đổi code (team dev) | ✅ Quy tắc 30 ngày nằm trong code của LMS — support không sửa được |
| Cần giải pháp ngay | ✅ Giáo viên cần vào LMS để dạy **ngay hôm đó** |
| Automation xử lý được ≥ 80% ca | ⚠️ Với ca LMS đúng phạm vi thì có; trên dữ liệu thật hiện chỉ ~30% (mục 9) |

| | Automation (Operating Engineer) | Sửa code (Software Engineer) |
| --- | --- | --- |
| Thời gian làm | Vài giờ – 1 ngày | Vài ngày – vài tuần (sửa + test + deploy) |
| Cần đổi code LMS | Không | Có |
| Giải quyết | Triệu chứng, ngay lập tức | Gốc rễ, lâu dài |
| Rủi ro | Mở lại nhầm tài khoản → giảm bằng kiểm tra HR | Ảnh hưởng chính sách bảo mật |

**Kết luận:** làm automation để giảm tải ngay, **đồng thời** đề xuất team dev xem lại quy tắc 30 ngày (VD: gửi email cảnh báo trước 3 ngày, hoặc chỉ khóa khi HR báo nghỉ việc) — xem [action-plan.md](action-plan.md).

## 3. Luồng xử lý

```
 Odoo Helpdesk                      login_bot                            HR API        LMS API
 ─────────────                      ─────────                            ──────        ───────
 Ticket mới ──(A) polling mỗi 5'──┐
            └─(B) webhook ────────┤
                                  ▼
                       1. Phân tích ticket (classifier.py)
                          từ khóa: đăng nhập / mật khẩu / bị khóa / login...
                          ├─ không phải lỗi đăng nhập ──► gắn tag auto-processed, dừng
                          ├─ học viên / hệ thống khác LMS / thiếu email ──► CHUYỂN NGƯỜI
                          ▼
                       2. Kiểm tra HR ─────────────────────────────────► GET /employees?email=
                          ├─ không có trong HR ──► CHUYỂN NGƯỜI
                          ├─ terminated ──► NGHỈ VIỆC: ghi chú, KHÔNG mở lại
                          ▼ active
                       3. Kiểm tra LMS ─────────────────────────────────────────────► GET /accounts?email=
                          ├─ chưa có tài khoản ──► CHUYỂN NGƯỜI (cần cấp mới)
                          ├─ deactivated ──► reactivate + gửi link đặt lại mật khẩu ──► POST /reactivate, /password-reset
                          └─ active ──► gửi link đặt lại mật khẩu ────────────────────► POST /password-reset
                                  ▼
                       4. Ghi vào Odoo: tag → ghi chú kết quả → email trả lời → đổi giai đoạn
                       5. Ghi log JSON (logs/login_bot.log)
```

## 4. Bảng quyết định

| # | Điều kiện | Bot làm | Tag | Giai đoạn | Email cho user |
| --- | --- | --- | --- | --- | --- |
| 1 | Không phải lỗi đăng nhập | Không làm gì thêm | `auto-processed` | giữ nguyên | — |
| 2 | Tài khoản học viên/phụ huynh (HV, Denise…) | Ghi chú lý do | `auto-escalated` | Escalated | Xác nhận đã nhận |
| 3 | Đăng nhập TMS / CRM / Ecount / Mail | Ghi chú "ngoài phạm vi" | `auto-escalated` | Escalated | Xác nhận đã nhận |
| 4 | Ticket không có email | Ghi chú | `auto-escalated` | Escalated | — (không có địa chỉ) |
| 5 | Email không có trong HR | Ghi chú | `auto-escalated` | Escalated | Xác nhận đã nhận |
| 6 | HR: **terminated** | Ghi chú "cần quản lý xác nhận", **không mở lại** | `auto-escalated` | Escalated | Xác nhận đã nhận (không nêu lý do nội bộ) |
| 7 | HR active, chưa có tài khoản LMS | Ghi chú "cần cấp mới" | `auto-escalated` | Escalated | Xác nhận đã nhận |
| 8 | HR active, LMS **deactivated** | **Reactivate + gửi link đặt lại mật khẩu** | `auto-reactivated` | Waiting Customer | Đã mở lại, hướng dẫn đăng nhập |
| 9 | HR active, LMS active | **Gửi link đặt lại mật khẩu** | `auto-password-reset` | Waiting Customer | Hướng dẫn đặt lại mật khẩu |
| 10 | HR/LMS lỗi sau 3 lần thử | Ghi chú "automation lỗi", **không mở lại** | `auto-escalated` | Escalated | Xác nhận đã nhận |
| 11 | Odoo lỗi khi ghi | Không gắn tag → lần chạy sau thử lại | — | — | — |

Nguyên tắc an toàn:

- **Chỉ mở lại tài khoản khi HR xác nhận active.** Mọi trường hợp không chắc chắn đều chuyển người xử lý (lỗi thường gặp ở Week 4: "bật lại account mà không xem trạng thái nhân sự").
- **Bot không đóng ticket**: ticket chuyển sang *Waiting Customer*, người xử lý chỉ đóng khi user xác nhận đã đăng nhập được (giống quy trình Week 4).
- **Email cho người đã nghỉ việc không nêu lý do** (trạng thái HR là thông tin nội bộ).
- **Không xử lý lặp**: gắn tag `auto-processed` *trước* các bước khác, polling và webhook đều bỏ qua ticket đã có tag.

## 5. Cấu trúc code

| File | Vai trò |
| --- | --- |
| [classifier.py](../automation/login_bot/classifier.py) | Nhận diện lỗi đăng nhập (bỏ dấu tiếng Việt + từ khóa), xác định hệ thống, phát hiện tài khoản học viên |
| [services.py](../automation/login_bot/services.py) | Client HTTP cho HR và LMS: timeout, thử lại 3 lần, 404 → "không có" |
| [mock_services.py](../automation/login_bot/mock_services.py) + [mock_data.json](../automation/login_bot/mock_data.json) | Mock HR + LMS API (MindX không cấp API thật cho bài tập) |
| [odoo.py](../automation/login_bot/odoo.py) | `OdooClient` (External API XML-RPC), `InMemoryOdoo` (giả lập cho test/demo), `DryRunOdoo` |
| [workflow.py](../automation/login_bot/workflow.py) | Bảng quyết định ở mục 4 + ghi Odoo + log |
| [messages.py](../automation/login_bot/messages.py) | Nội dung ghi chú và email (theo template Scenario 1 – Week 4) |
| [run.py](../automation/login_bot/run.py) | Lệnh chạy: `--demo`, `--check-odoo`, `--once`, `--interval`, `--dry-run` |
| [webhook.py](../automation/login_bot/webhook.py) | HTTP endpoint nhận webhook từ Odoo |
| [seed_odoo.py](../automation/login_bot/seed_odoo.py) | Tạo 8 ticket test trên Odoo thật |
| [stats.py](../automation/login_bot/stats.py) | Thống kê hiệu quả từ log |
| [tests/](../automation/tests/) | 51 test (`unittest`, không cần cài thư viện) |

Chỉ dùng thư viện chuẩn của Python 3.10+, không cần `pip install`.

## 6. Tích hợp Odoo

### 6.1 Kết nối API

Bot dùng **Odoo External API (XML-RPC)**: `/xmlrpc/2/common` để đăng nhập, `/xmlrpc/2/object` để gọi `execute_kw`.

| Việc | Model / method |
| --- | --- |
| Lấy ticket mới | `helpdesk.ticket.search_read`, domain: giai đoạn **Mới** (`ODOO_STAGE_NEW`), đúng nhóm, **không** có tag `auto-processed` / `week5-sample` — không bao giờ đụng vào ticket đang/đã có người xử lý |
| Ghi chú nội bộ | `mail.message.create` (subtype *Note*); nếu không được phép thì dùng `helpdesk.ticket.message_post` với `mail.mt_note` |
| Gửi email thật (`LOGIN_BOT_SEND_EMAIL=true`) | `helpdesk.ticket.message_post`, subtype `mail.mt_comment`, gửi tới khách hàng của ticket |
| Gắn tag | `helpdesk.tag.search/create` + `helpdesk.ticket.write` `{tag_ids: [(4, id)]}` |
| Đổi giai đoạn | `helpdesk.stage.search` theo tên + `helpdesk.ticket.write` `{stage_id}` |

Cấu hình (file `automation/.env`, mẫu: [.env.example](../automation/.env.example)):

1. Odoo → avatar → **Hồ sơ của tôi → Bảo mật tài khoản → New API Key** → copy vào `ODOO_API_KEY`.
2. `ODOO_URL=https://choi.odoo.com`, `ODOO_DB` = tên database (thường là `choi`), `ODOO_USER` = email đăng nhập Odoo.
3. `ODOO_TEAM_ID` = số trên URL Helpdesk (`/odoo/helpdesk/1/...` → `1`).
4. Giai đoạn `Waiting Customer` và `Escalated` đã tạo ở Week 4; tên khác thì sửa `ODOO_STAGE_*`.
5. Kiểm tra: `python -m login_bot.run --check-odoo`.

> Mặc định `LOGIN_BOT_SEND_EMAIL=false`: email trả lời được lưu thành **ghi chú** trên ticket, giống cách làm Week 4 (khách hàng dùng email giả lập `@example.com`).

### 6.2 Trigger A — Chạy theo lịch (mặc định)

```
python -m login_bot.run --interval 300      # mỗi 5 phút
```

Chọn làm mặc định vì Odoo trial nằm trên cloud, **không gọi được vào máy local**; polling chỉ cần máy chạy bot gọi ra Odoo. Ticket được xử lý trong ≤ 5 phút, nằm trong mục tiêu phản hồi 30 phút của Week 4.

Chạy nền trên Windows: Task Scheduler → *Create Basic Task* → *Daily*, lặp lại mỗi 5 phút → Action: `python -m login_bot.run --once`, *Start in* = thư mục `automation`. Trên Linux: cron `*/5 * * * * cd /path/automation && python -m login_bot.run --once`.

### 6.3 Trigger B — Webhook (xử lý ngay khi ticket được tạo)

1. Chạy `python -m login_bot.webhook --port 8070` trên máy có địa chỉ public (server, hoặc máy local + `ngrok http 8070`).
2. Odoo → **Cài đặt → Kỹ thuật → Automation Rules** (bật chế độ developer) → **Mới**:
   - Model: *Helpdesk Ticket* · Trigger: *On creation*
   - Action: *Send Webhook Notification* · URL: `https://<địa-chỉ>/odoo/ticket?token=<LOGIN_BOT_WEBHOOK_TOKEN>`
   - Fields: `id`, `name`
3. Odoo gửi JSON có `_id` của ticket → bot **đọc lại ticket qua API** (không tin dữ liệu trong payload) → xử lý → trả `{"outcome": ...}`.

Webhook từ chối token sai (401), payload thiếu id (400), ticket không tồn tại (404). Nếu webhook lỗi, polling vẫn bắt được ticket ở lần chạy sau, nên **có thể bật cả hai**.

## 7. Log và giám sát

Mỗi ticket ghi một dòng JSON vào `automation/logs/login_bot.log`:

```json
{"ts": "2026-11-11T21:42:04", "ticket_id": 1, "subject": "Không thể đăng nhập vào LMS", "outcome": "reactivated",
 "reason": "HR active + LMS deactivated", "actions": ["tag", "note", "email-draft", "stage:Waiting Customer"], "duration_ms": 171}
```

`python -m login_bot.stats` tính: số ticket, số ticket đăng nhập, tỷ lệ tự xử lý, thời gian bot, số phút tiết kiệm (5–10 phút/ticket). Trên Odoo: lọc tag `auto-reactivated` / `auto-password-reset` / `auto-escalated` để theo dõi.

Chỉ số theo dõi sau khi chạy: tỷ lệ tự xử lý, số ticket bot đã xử lý nhưng user vẫn phản hồi "chưa được", số lần `failed`.

## 8. Chạy thử

```
cd automation
python -m unittest -v                      # 51 test
python -m login_bot.run --demo             # demo offline 8 nhánh, không cần Odoo
python -m login_bot.mock_services          # (cửa sổ 1) mock HR + LMS ở cổng 8090
python -m login_bot.seed_odoo              # (cửa sổ 2) tạo 8 ticket test trên Odoo
python -m login_bot.run --once --dry-run   # xem bot SẼ làm gì, không ghi gì
python -m login_bot.run --once             # xử lý thật
```

## 9. Giới hạn và hướng mở rộng

- **HR và LMS là mock** (MindX không cấp API cho bài tập). Muốn chạy thật chỉ cần đổi `HR_API_URL` / `LMS_API_URL` sang API thật có cùng dạng dữ liệu, hoặc viết lại `HrClient` / `LmsClient`.
- **Phạm vi hiện tại chỉ LMS.** Chạy bộ phân loại trên 118 ticket thật ([TEST-RESULTS.md](TEST-RESULTS.md) mục 4): 11 ticket được nhận là lỗi đăng nhập, nhưng chỉ **4** là LMS hoặc không ghi rõ hệ thống; 7 ticket còn lại là TMS (3), Ecount (2), Mail (1), CRM (1). Quy trình kiểm tra HR giống hệt nhau, chỉ khác bước mở lại tài khoản → **mở rộng thêm connector cho TMS và Ecount sẽ nâng tỷ lệ bot xử lý từ ~30% lên ~80%**.
- **Phân loại bằng từ khóa**: precision 100%, recall 79% trên dữ liệu thật. 3 ticket bị bỏ sót đều là tài khoản học viên — vốn cũng phải chuyển người, nên không gây hại. Có thể thay bằng mô hình NLP khi có nhiều dữ liệu hơn.
- Tách tài khoản trùng email, tài khoản nhiều hệ thống, hay yêu cầu "chuyển cơ sở" vẫn cần người xử lý.
