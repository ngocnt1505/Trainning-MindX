"""Workflow chính: phân tích ticket -> kiểm tra HR -> xử lý -> trả lời -> ghi log.

Bảng quyết định (docs4/automation.md, mục 4):
  không phải lỗi đăng nhập             -> chỉ gắn tag auto-processed
  tài khoản học viên / hệ thống khác LMS
  / thiếu email / không có trong HR
  / không có tài khoản LMS             -> ESCALATED
  HR terminated                        -> TERMINATED (không mở lại tài khoản)
  HR active + LMS deactivated          -> REACTIVATED (mở lại + link đặt lại mật khẩu)
  HR active + LMS active               -> PASSWORD_RESET
  HR/LMS lỗi sau khi thử lại           -> FAILED (người xử lý tiếp)
"""

import json
import logging
import time
from datetime import datetime

from . import messages
from .classifier import classify
from .models import AUTO_TAG, Outcome, Result
from .odoo import OdooError
from .services import ServiceError

OUTCOME_TAGS = {
    Outcome.NOT_LOGIN: [AUTO_TAG],
    Outcome.REACTIVATED: [AUTO_TAG, "auto-reactivated"],
    Outcome.PASSWORD_RESET: [AUTO_TAG, "auto-password-reset"],
    Outcome.TERMINATED: [AUTO_TAG, "auto-escalated"],
    Outcome.ESCALATED: [AUTO_TAG, "auto-escalated"],
    Outcome.FAILED: [AUTO_TAG, "auto-escalated"],
}


class Decision(Exception):
    """Dừng workflow sớm với một kết quả (dùng cho các nhánh chuyển người xử lý)."""

    def __init__(self, outcome, reason):
        super().__init__(reason)
        self.outcome = outcome
        self.reason = reason


class LoginBot:
    def __init__(self, odoo, hr, lms, settings, logger=None, clock=datetime.now):
        self.odoo = odoo
        self.hr = hr
        self.lms = lms
        self.s = settings
        self.log = logger or logging.getLogger("login_bot")
        self.clock = clock

    def run_once(self, limit=50):
        results = []
        for ticket in self.odoo.fetch_unprocessed(limit):
            results.append(self.process(ticket))
        return results

    def process(self, ticket):
        started = time.monotonic()
        try:
            result = self._process(ticket)
        except OdooError as err:
            # Không ghi được vào Odoo: để nguyên ticket, lần chạy sau thử lại.
            result = Result(ticket.id, Outcome.FAILED, f"Lỗi Odoo: {err}")
        self.log.info(json.dumps({
            "ts": self.clock().isoformat(timespec="seconds"),
            "ticket_id": ticket.id,
            "subject": ticket.subject,
            "outcome": result.outcome.value,
            "reason": result.reason,
            "actions": result.actions,
            "duration_ms": round((time.monotonic() - started) * 1000),
        }, ensure_ascii=False))
        return result

    # ------------------------------------------------------------------
    def _process(self, ticket):
        if AUTO_TAG in ticket.tags:
            return Result(ticket.id, Outcome.ALREADY_PROCESSED, "ticket đã được bot xử lý trước đó")

        c = classify(ticket.subject, ticket.description)
        if not c.is_login:
            self.odoo.add_tags(ticket.id, OUTCOME_TAGS[Outcome.NOT_LOGIN])
            return Result(ticket.id, Outcome.NOT_LOGIN, "không phải lỗi đăng nhập", ["tag"])

        found = [f"Phân loại: lỗi đăng nhập (từ khóa: {', '.join(c.keywords)}) - hệ thống: {(c.system or 'không ghi rõ').upper()}"]
        try:
            outcome, reason, next_step = self._decide_and_act(ticket, c, found)
        except Decision as d:
            outcome, reason = d.outcome, d.reason
            next_step = "kỹ thuật viên kiểm tra và xử lý tay theo quy trình Scenario 1"
        except ServiceError as err:
            outcome, reason = Outcome.FAILED, str(err)
            next_step = "kỹ thuật viên xử lý tay; kiểm tra HR/LMS API"

        if outcome != Outcome.REACTIVATED and outcome != Outcome.PASSWORD_RESET:
            found.append(f"Lý do chuyển người xử lý: {reason}")
        return self._apply(ticket, outcome, reason, found, next_step)

    def _decide_and_act(self, ticket, c, found):
        if c.is_student:
            raise Decision(Outcome.ESCALATED, "tài khoản học viên/phụ huynh - không có trong HR")
        if c.system not in (None, "lms"):
            raise Decision(Outcome.ESCALATED, f"đăng nhập {c.system.upper()} - ngoài phạm vi bot (chỉ xử lý LMS)")
        if not ticket.email:
            raise Decision(Outcome.ESCALATED, "ticket không có email người gửi")

        employee = self.hr.get_employee(ticket.email)
        if employee is None:
            raise Decision(Outcome.ESCALATED, f"không tìm thấy {ticket.email} trong HR")
        found.append(f"HR: {employee.email} - {employee.status} ({employee.department})")
        if employee.status == "terminated":
            raise Decision(Outcome.TERMINATED, "nhân sự đã nghỉ việc - KHÔNG mở lại tài khoản, cần quản lý xác nhận")
        if employee.status != "active":
            raise Decision(Outcome.ESCALATED, f"trạng thái HR không xác định: {employee.status}")

        account = self.lms.get_account(ticket.email)
        if account is None:
            raise Decision(Outcome.ESCALATED, "nhân sự active nhưng chưa có tài khoản LMS - cần cấp mới")
        found.append(f"LMS: {account.status} (đăng nhập lần cuối {account.last_login or 'không rõ'})")

        if account.status == "deactivated":
            self.lms.reactivate(ticket.email)
            found.append("Đã reactivate tài khoản LMS")
            self.lms.send_password_reset(ticket.email)
            found.append("Đã gửi link đặt lại mật khẩu")
            return Outcome.REACTIVATED, "HR active + LMS deactivated", "chờ user xác nhận đăng nhập được rồi đóng ticket"

        self.lms.send_password_reset(ticket.email)
        found.append("Tài khoản LMS đang active - đã gửi link đặt lại mật khẩu")
        return Outcome.PASSWORD_RESET, "HR active + LMS active", "chờ user xác nhận đăng nhập được rồi đóng ticket"

    def _apply(self, ticket, outcome, reason, found, next_step):
        actions = []
        # Gắn tag trước để dù bước sau lỗi, ticket không bị xử lý lặp lại ở lần chạy tiếp theo.
        self.odoo.add_tags(ticket.id, OUTCOME_TAGS[outcome])
        actions.append("tag")
        self.odoo.post_note(ticket.id, messages.note(outcome, self.clock(), found, next_step))
        actions.append("note")

        if outcome == Outcome.REACTIVATED:
            body = messages.email_reactivated(ticket.customer, ticket.id)
        elif outcome == Outcome.PASSWORD_RESET:
            body = messages.email_password_reset(ticket.customer, ticket.id)
        else:
            body = messages.email_acknowledged(ticket.customer, ticket.id)
        if ticket.email:
            self._respond(ticket, body)
            actions.append("email" if self.s.send_email else "email-draft")

        stage = self.s.stage_waiting if outcome in (Outcome.REACTIVATED, Outcome.PASSWORD_RESET) else self.s.stage_escalated
        self.odoo.set_stage(ticket.id, stage)
        actions.append(f"stage:{stage}")
        return Result(ticket.id, outcome, reason, actions)

    def _respond(self, ticket, body):
        subject = messages.subject(ticket)
        if self.s.send_email:
            self.odoo.send_email(ticket.id, subject, body)
        else:
            # Mặc định không gửi email thật (giống Week 4): lưu bản email vào ghi chú.
            self.odoo.post_note(ticket.id, f"[EMAIL GỬI USER - bản nháp, LOGIN_BOT_SEND_EMAIL=false]\n"
                                           f"To: {ticket.email}\nSubject: {subject}\n\n{body}")
