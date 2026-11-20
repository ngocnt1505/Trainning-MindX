# Hexagonal Architecture + TDD

Nguyễn Thúy Ngọc · 20/11/2026

## 1. What: Hexagonal là gì

Hexagonal Architecture, còn gọi là **Ports & Adapters**, do Alistair Cockburn đưa ra năm 2005. Ý tưởng chỉ có một câu:

> Nghiệp vụ nằm ở giữa và không biết gì về thế giới bên ngoài. Mọi thứ bên ngoài (giao diện, database, API, email) nói chuyện với nghiệp vụ qua **cổng (port)**, và mỗi công nghệ cụ thể là một **bộ chuyển (adapter)** cắm vào cổng đó.

```
        BÊN GỌI VÀO (driving)                          BÊN BỊ GỌI (driven)

  CLI ─────┐                                            ┌──── Odoo XML-RPC
  Webhook ─┤──► [port vào] ─►  ┌───────────┐ ─► [port ra] ├──── HR API
  Test ────┘                   │ NGHIỆP VỤ │             ├──── LMS API
                               │  (core)   │             └──── Fake (khi test)
                               └───────────┘
```

Hình lục giác chỉ để vẽ cho có nhiều cạnh cắm adapter. Con số 6 không có ý nghĩa gì.

## 2. Why: vì sao cần

| Vấn đề khi trộn nghiệp vụ với công nghệ | Hexagonal giải quyết thế nào |
| --- | --- |
| Muốn test luật nghiệp vụ phải dựng Odoo, HR, LMS thật | Test core với adapter giả (fake), chạy trong vài mili giây |
| Đổi Odoo sang hệ thống khác thì phải sửa cả nghiệp vụ | Chỉ viết adapter mới, core giữ nguyên |
| Một luật nghiệp vụ nằm rải rác trong CLI, webhook, cron | Luật chỉ nằm ở core; CLI, webhook, cron đều gọi cùng một port |
| Đọc code khó biết đâu là luật, đâu là kỹ thuật | Core chỉ có luật, đọc như đọc bảng quyết định |

## 3. How it works: các thành phần

| Thành phần | Là gì | Ví dụ trong login bot |
| --- | --- | --- |
| **Core** (domain + use case) | Luật nghiệp vụ, không import thư viện mạng / database | "HR terminated thì không mở lại tài khoản" |
| **Port vào** (driving / primary) | Cách bên ngoài ra lệnh cho core | `bot.process(ticket)` |
| **Port ra** (driven / secondary) | Core cần gì từ bên ngoài, do **core định nghĩa** | "cho tôi trạng thái nhân sự theo email" |
| **Adapter vào** | Biến input của một công nghệ thành lời gọi port vào | `run.py` (CLI), `webhook.py` (HTTP) |
| **Adapter ra** | Cài đặt port ra bằng một công nghệ cụ thể | `OdooClient`, `HrClient`, `InMemoryOdoo` |

**Luật phụ thuộc:** mũi tên `import` chỉ đi từ ngoài vào trong. Adapter biết core, còn core không biết adapter. Core cần một thứ ở bên ngoài thì tự khai báo port, rồi adapter cài đặt port đó (đảo ngược phụ thuộc, *Dependency Inversion*).

**Lắp ráp (composition root):** có một chỗ duy nhất quyết định dùng adapter nào, ví dụ `build_bot()` trong `run.py`. Chạy thật thì truyền `OdooClient`, chạy demo thì truyền `InMemoryOdoo`, chạy thử an toàn thì truyền `DryRunOdoo`.

## 4. How: các bước làm

1. Viết luật nghiệp vụ thành bảng quyết định (tuần 5 đã có trong `automation.md` mục 4).
2. Liệt kê core cần gì từ bên ngoài, đặt tên theo **ngôn ngữ nghiệp vụ** (`status_of(email)`), không theo công nghệ (`GET /api/hr/v1/employees`).
3. Khai báo các port đó thành interface.
4. Viết core bằng TDD với adapter giả (mục 5).
5. Viết adapter thật, test riêng bằng integration test.
6. Lắp ráp ở composition root.

## 5. Hexagonal + TDD

Hai thứ này hợp nhau vì Hexagonal cho TDD **một chỗ để test nhanh**, còn TDD thì giữ cho core sạch: muốn test được không cần mạng thì buộc phải tách port ra.

| Cấp test (tuần 1) | Test cái gì | Dùng adapter nào |
| --- | --- | --- |
| Unit | Core, từng nhánh của bảng quyết định | Fake (trong bộ nhớ) |
| Integration / contract | Từng adapter thật có đúng hành vi port không | Adapter thật + server giả hoặc sandbox |
| End-to-end | Cả luồng từ adapter vào tới adapter ra | Adapter thật, môi trường test |

### Ví dụ: TDD một luật của login bot

**Bước 1. Port**, do core khai báo:

```python
# core/ports.py
from typing import Protocol, Optional

class HrDirectory(Protocol):
    def status_of(self, email: str) -> Optional[str]: ...   # "active" | "terminated" | None

class LmsAccounts(Protocol):
    def is_active(self, email: str) -> bool: ...
    def reactivate(self, email: str) -> None: ...
```

**Bước 2. Red**: viết test trước, dùng fake.

```python
# tests/test_handle_login.py
class FakeHr:
    def __init__(self, data): self.data = data
    def status_of(self, email): return self.data.get(email)

class FakeLms:
    def __init__(self, active): self.active, self.reactivated = active, []
    def is_active(self, email): return email in self.active
    def reactivate(self, email): self.reactivated.append(email)

def test_terminated_staff_is_not_reactivated():
    hr, lms = FakeHr({"a@mindx.edu.vn": "terminated"}), FakeLms(active=set())
    assert handle_login("a@mindx.edu.vn", hr, lms) == "TERMINATED"
    assert lms.reactivated == []          # luật an toàn: không được mở lại

def test_active_staff_with_locked_account_is_reactivated():
    hr, lms = FakeHr({"b@mindx.edu.vn": "active"}), FakeLms(active=set())
    assert handle_login("b@mindx.edu.vn", hr, lms) == "REACTIVATED"
    assert lms.reactivated == ["b@mindx.edu.vn"]
```

**Bước 3. Green**: viết core vừa đủ cho test qua.

```python
# core/handle_login.py
def handle_login(email, hr, lms):
    status = hr.status_of(email)
    if status is None:
        return "ESCALATED"
    if status == "terminated":
        return "TERMINATED"
    if lms.is_active(email):
        return "PASSWORD_RESET"
    lms.reactivate(email)
    return "REACTIVATED"
```

**Bước 4. Refactor**, rồi làm tiếp dòng tiếp theo của bảng quyết định.

Các test này không cần Odoo, HR hay LMS thật. Adapter thật (`HrClient` gọi HTTP) có test riêng chạy với mock server.

### Contract test: một bộ test cho nhiều adapter

Tuần 3 đã làm điều này với `kb`: *"mock và HTTP phải giống hệt nhau"*. Viết **một** bộ test cho port rồi chạy cho mọi adapter (Fake, HTTP). Nhờ vậy, fake dùng khi unit test không bị lệch so với hệ thống thật. Nếu fake sai thì mọi unit test qua cũng vô nghĩa.

## 6. So sánh với Clean Architecture

Clean Architecture (Robert C. Martin, 2012) chia hệ thống thành 4 vòng tròn đồng tâm: **Entities → Use Cases → Interface Adapters → Frameworks & Drivers**, và phụ thuộc chỉ được hướng vào trong.

| | Hexagonal | Clean Architecture |
| --- | --- | --- |
| Ý tưởng gốc | Core tách khỏi bên ngoài qua port/adapter | Giống vậy, phụ thuộc chỉ hướng vào trong |
| Bên trong core | **Không quy định** chia thế nào | Chia rõ: Entities (luật chung) và Use Cases (luật của từng tình huống) |
| Hình dung | Trong / ngoài, bên gọi vào (trái) / bên bị gọi (phải) | Các vòng tròn lồng nhau |
| Số khái niệm | Ít: core, port, adapter | Nhiều hơn: entity, use case, interactor, presenter, gateway, controller |
| Hợp với | Tool nhỏ, service tích hợp nhiều hệ thống (bot, CLI) | Ứng dụng lớn, nhiều use case, nhiều người cùng làm |

**Kết luận:** hai cái chung một nguyên lý (Dependency Inversion, core không biết hạ tầng). Clean Architecture có thể coi là Hexagonal chia thêm tầng bên trong. Onion Architecture (Jeffrey Palermo, 2008) cũng cùng họ này. Với cải tiến phải xong trong 2 tuần, dùng Hexagonal là đủ. Chỉ chia thêm tầng khi core lớn lên.

## 7. Áp dụng vào hệ thống tuần 4–5

### Login bot tuần 5 đã gần Hexagonal

| Vai trò | File hiện tại | Nhận xét |
| --- | --- | --- |
| Core | `workflow.py` (`LoginBot`), `classifier.py`, `models.py` | `LoginBot(odoo, hr, lms)` nhận adapter từ ngoài vào, không tự tạo ✅ |
| Port ra | Ngầm định qua duck typing | Chưa khai báo thành interface. Nên thêm `Protocol` như mục 5 để thấy rõ hợp đồng |
| Adapter ra | `OdooClient`, `InMemoryOdoo`, `DryRunOdoo`, `HrClient`, `LmsClient` | 3 adapter Odoo cho cùng một port, đúng tinh thần Hexagonal ✅ |
| Adapter vào | `run.py` (CLI / polling), `webhook.py` | Cùng gọi `bot.process()` ✅ |
| Composition root | `build_bot()` trong `run.py` | ✅ |
| Chỗ chưa sạch | Core gọi `odoo.set_stage(...)`, `odoo.add_tags(...)` với tên stage và tag của Odoo | Core đang biết khái niệm của Odoo. Sạch hơn là port nghiệp vụ, ví dụ `tickets.mark_escalated(id, reason)`, để adapter Odoo tự đổi sang stage/tag |

### Mở rộng theo action plan tuần 5

| Hành động | Làm theo Hexagonal |
| --- | --- |
| A2: thêm TMS / Ecount / Mail | Mỗi hệ thống là **một adapter mới** của port `Accounts` (`is_active`, `reactivate`). Core và bảng quyết định không đổi, test core giữ nguyên |
| B1: gộp sự cố (≥ 3 ticket cùng hệ thống trong 1 giờ, quy trình S05 tuần 4) | Luật gộp là **core thuần**, nhận danh sách ticket và trả về nhóm. TDD hoàn toàn bằng dữ liệu giả. Odoo chỉ là adapter để đọc ticket và ghi `Duplicate of #…` |
| Phân loại Class of Service (tuần 4) | Hàm core `class_of_service(so_nguoi_anh_huong, co_deadline)` để trả về Standard / Priority / Expedite / Fixed Deadline. Dùng chung được cho bot, report, form Odoo |
| Đổi Odoo sang helpdesk khác | Viết adapter mới cho port `Tickets`, không sửa core |

## 8. Khi nào không nên dùng

- Script chạy một lần, hoặc CRUD đơn giản không có luật nghiệp vụ: thêm port chỉ làm code dài hơn.
- Không tạo port cho thứ chưa bao giờ thay và cũng không cần giả khi test.
- Dấu hiệu làm quá tay: port chỉ chuyển tiếp nguyên lời gọi, và core không có luật gì.

## Tài liệu tham khảo

1. Alistair Cockburn, *Hexagonal Architecture* (2005), alistair.cockburn.us/hexagonal-architecture
2. Robert C. Martin, *The Clean Architecture* (2012), blog.cleancoder.com; sách *Clean Architecture* (2017)
3. Steve Freeman, Nat Pryce, *Growing Object-Oriented Software, Guided by Tests* (2009). TDD từ ngoài vào, kết hợp với ports & adapters
4. Jeffrey Palermo, *The Onion Architecture* (2008)
