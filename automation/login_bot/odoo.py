"""Tích hợp Odoo Helpdesk qua External API (XML-RPC), kèm bản giả lập in-memory cho test/demo.

Cả hai class có cùng interface để workflow không cần biết đang chạy với Odoo thật hay giả.
"""

import dataclasses
import html
import re
import xmlrpc.client
from collections import defaultdict

from .models import AUTO_TAG, Ticket


class OdooError(Exception):
    """Không gọi được Odoo (sai cấu hình, mất mạng, lỗi quyền...)."""


def text_to_html(text):
    return "<p>" + "<br/>".join(html.escape(line) for line in text.splitlines()) + "</p>"


def html_to_text(value):
    if not value:
        return ""
    value = re.sub(r"<br\s*/?>|</p>", "\n", value)
    return html.unescape(re.sub(r"<[^>]+>", "", value)).strip()


class OdooClient:
    TICKET_FIELDS = ["name", "description", "partner_email", "partner_name", "tag_ids"]

    def __init__(self, settings, server_proxy=xmlrpc.client.ServerProxy):
        self.s = settings
        self.common = server_proxy(f"{settings.odoo_url}/xmlrpc/2/common", allow_none=True)
        self.models = server_proxy(f"{settings.odoo_url}/xmlrpc/2/object", allow_none=True)
        self.uid = None
        self._tag_ids = {}
        self._stage_ids = {}
        self._note_subtype = None

    # --- hạ tầng -------------------------------------------------------
    def _login(self):
        if self.uid is None:
            try:
                self.uid = self.common.authenticate(self.s.odoo_db, self.s.odoo_user, self.s.odoo_api_key, {})
            except (xmlrpc.client.Error, OSError) as err:
                raise OdooError(f"Không kết nối được {self.s.odoo_url}: {err}") from err
            if not self.uid:
                raise OdooError("Đăng nhập Odoo thất bại: kiểm tra ODOO_DB / ODOO_USER / ODOO_API_KEY")
        return self.uid

    def call(self, model, method, args, kwargs=None):
        kwargs = dict(kwargs or {})
        kwargs.setdefault("context", {"lang": self.s.odoo_lang})
        try:
            return self.models.execute_kw(self.s.odoo_db, self._login(), self.s.odoo_api_key,
                                          model, method, args, kwargs)
        except (xmlrpc.client.Error, OSError) as err:
            raise OdooError(f"{model}.{method} lỗi: {err}") from err

    def tag_id(self, name, create=False):
        if name not in self._tag_ids:
            found = self.call("helpdesk.tag", "search", [[("name", "=", name)]], {"limit": 1})
            if found:
                self._tag_ids[name] = found[0]
            elif create:
                self._tag_ids[name] = self.call("helpdesk.tag", "create", [{"name": name}])
            else:
                return None
        return self._tag_ids[name]

    def stage_id(self, name):
        if name not in self._stage_ids:
            domain = [("name", "=", name)]
            if self.s.odoo_team_id:
                domain.append(("team_ids", "in", [self.s.odoo_team_id]))
            found = self.call("helpdesk.stage", "search", [domain], {"limit": 1})
            if not found:
                raise OdooError(f"Không có giai đoạn '{name}' trong Helpdesk (xem ODOO_STAGE_* trong .env)")
            self._stage_ids[name] = found[0]
        return self._stage_ids[name]

    def note_subtype_id(self):
        if self._note_subtype is None:
            found = self.call("ir.model.data", "search_read",
                              [[("module", "=", "mail"), ("name", "=", "mt_note")]], {"fields": ["res_id"]})
            self._note_subtype = found[0]["res_id"] if found else False
        return self._note_subtype

    def _to_tickets(self, records):
        tag_ids = sorted({i for r in records for i in r["tag_ids"]})
        names = {t["id"]: t["name"] for t in self.call("helpdesk.tag", "read", [tag_ids], {"fields": ["name"]})} if tag_ids else {}
        return [Ticket(id=r["id"], subject=r["name"] or "", description=html_to_text(r["description"]),
                       email=r["partner_email"] or "", customer=r["partner_name"] or "",
                       tags=tuple(names.get(i, "") for i in r["tag_ids"])) for r in records]

    # --- interface dùng bởi workflow ----------------------------------
    def fetch_unprocessed(self, limit=50):
        # Chỉ ticket mới đến: không đụng vào ticket đang/đã có người xử lý.
        domain = [("stage_id", "=", self.stage_id(self.s.stage_new))]
        if self.s.odoo_team_id:
            domain.append(("team_id", "=", self.s.odoo_team_id))
        excluded = [i for i in (self.tag_id(n) for n in (AUTO_TAG, *self.s.skip_tags)) if i]
        if excluded:
            domain.append(("tag_ids", "not in", excluded))
        records = self.call("helpdesk.ticket", "search_read", [domain],
                            {"fields": self.TICKET_FIELDS, "order": "id asc", "limit": limit})
        return self._to_tickets(records)

    def get_ticket(self, ticket_id):
        records = self.call("helpdesk.ticket", "search_read", [[("id", "=", int(ticket_id))]],
                            {"fields": self.TICKET_FIELDS})
        return self._to_tickets(records)[0] if records else None

    def post_note(self, ticket_id, text):
        """Ghi chú nội bộ (không gửi email cho khách)."""
        values = {"model": "helpdesk.ticket", "res_id": ticket_id, "body": text_to_html(text),
                  "message_type": "comment", "subtype_id": self.note_subtype_id()}
        try:
            self.call("mail.message", "create", [values])
        except OdooError:
            # Một số bản Odoo không cho tạo mail.message trực tiếp: dùng message_post (body hiển thị dạng text).
            self.call("helpdesk.ticket", "message_post", [[ticket_id]],
                      {"body": text, "message_type": "comment", "subtype_xmlid": "mail.mt_note"})

    def send_email(self, ticket_id, subject, text):
        """Gửi email thật cho khách qua chatter của ticket."""
        partner = self.call("helpdesk.ticket", "read", [[ticket_id]], {"fields": ["partner_id"]})[0]["partner_id"]
        self.call("helpdesk.ticket", "message_post", [[ticket_id]],
                  {"body": text, "subject": subject, "message_type": "comment",
                   "subtype_xmlid": "mail.mt_comment", "partner_ids": [partner[0]] if partner else []})

    def add_tags(self, ticket_id, names):
        ids = [self.tag_id(n, create=True) for n in names]
        self.call("helpdesk.ticket", "write", [[ticket_id], {"tag_ids": [(4, i) for i in ids]}])

    def set_stage(self, ticket_id, stage_name):
        self.call("helpdesk.ticket", "write", [[ticket_id], {"stage_id": self.stage_id(stage_name)}])

    # --- tiện ích: tạo ticket test, kiểm tra kết nối -------------------
    def create_ticket(self, subject, description, email, customer, tags=()):
        values = {"name": subject, "description": text_to_html(description),
                  "partner_email": email, "partner_name": customer,
                  "tag_ids": [(6, 0, [self.tag_id(t, create=True) for t in tags])]}
        if self.s.odoo_team_id:
            values["team_id"] = self.s.odoo_team_id
        return self.call("helpdesk.ticket", "create", [values])

    def check(self):
        version = self.common.version()
        uid = self._login()
        count = self.call("helpdesk.ticket", "search_count", [[]])
        stages = {name: self.stage_id(name) for name in (self.s.stage_new, self.s.stage_waiting, self.s.stage_escalated)}
        return {"server_version": version.get("server_version"), "uid": uid,
                "ticket_count": count, "stages": stages, "note_subtype_id": self.note_subtype_id()}


class InMemoryOdoo:
    """Odoo giả lập: dùng trong unit test và chế độ --demo (không cần mạng)."""

    def __init__(self, tickets=(), skip_tags=()):
        self.tickets = {t.id: t for t in tickets}
        self.skip_tags = set(skip_tags)
        self.stages = {}
        self.log = defaultdict(list)  # ticket_id -> [(loại, nội dung)]

    def fetch_unprocessed(self, limit=50):
        pending = [t for _, t in sorted(self.tickets.items())
                   if AUTO_TAG not in t.tags and not self.skip_tags & set(t.tags)]
        return pending[:limit]

    def get_ticket(self, ticket_id):
        return self.tickets.get(int(ticket_id))

    def post_note(self, ticket_id, text):
        self.log[ticket_id].append(("note", text))

    def send_email(self, ticket_id, subject, text):
        self.log[ticket_id].append(("email", f"{subject}\n{text}"))

    def add_tags(self, ticket_id, names):
        ticket = self.tickets[ticket_id]
        new = tuple(n for n in names if n not in ticket.tags)
        self.tickets[ticket_id] = dataclasses.replace(ticket, tags=ticket.tags + new)
        self.log[ticket_id].append(("tags", ", ".join(names)))

    def set_stage(self, ticket_id, stage_name):
        self.stages[ticket_id] = stage_name
        self.log[ticket_id].append(("stage", stage_name))

    def create_ticket(self, subject, description, email, customer, tags=()):
        new_id = max(self.tickets, default=0) + 1
        self.tickets[new_id] = Ticket(new_id, subject, description, email, customer, tuple(tags))
        return new_id


class DryRunOdoo:
    """Đọc ticket thật nhưng không ghi gì vào Odoo; chỉ ghi lại việc *sẽ* làm."""

    def __init__(self, inner):
        self.inner = inner
        self.planned = defaultdict(list)

    def fetch_unprocessed(self, limit=50):
        return self.inner.fetch_unprocessed(limit)

    def get_ticket(self, ticket_id):
        return self.inner.get_ticket(ticket_id)

    def post_note(self, ticket_id, text):
        self.planned[ticket_id].append(("note", text))

    def send_email(self, ticket_id, subject, text):
        self.planned[ticket_id].append(("email", f"{subject}\n{text}"))

    def add_tags(self, ticket_id, names):
        self.planned[ticket_id].append(("tags", ", ".join(names)))

    def set_stage(self, ticket_id, stage_name):
        self.planned[ticket_id].append(("stage", stage_name))
