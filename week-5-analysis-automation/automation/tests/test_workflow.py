import json
import logging
import unittest
from datetime import datetime

from login_bot.config import Settings
from login_bot.models import AUTO_TAG, Employee, LmsAccount, Outcome, Ticket
from login_bot.odoo import DryRunOdoo, InMemoryOdoo, OdooError
from login_bot.services import DryRunLms, ServiceError
from login_bot.workflow import LoginBot

EMAIL = "gv@example.com"


class FakeHr:
    def __init__(self, employee=None, error=None):
        self.employee, self.error, self.calls = employee, error, 0

    def get_employee(self, email):
        self.calls += 1
        if self.error:
            raise self.error
        return self.employee


class FakeLms:
    def __init__(self, account=None, error=None):
        self.account, self.error = account, error
        self.reactivated, self.resets = [], []

    def get_account(self, email):
        if self.error:
            raise self.error
        return self.account

    def reactivate(self, email):
        self.reactivated.append(email)

    def send_password_reset(self, email):
        self.resets.append(email)
        return "https://lms/reset"


class BrokenOdoo(InMemoryOdoo):
    def add_tags(self, ticket_id, names):
        raise OdooError("mất kết nối")


def login_ticket(**overrides):
    values = dict(id=1, subject="Không thể đăng nhập vào LMS", description="Invalid username or password",
                  email=EMAIL, customer="Nguyễn Văn A")
    values.update(overrides)
    return Ticket(**values)


class Recorder(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(json.loads(record.getMessage()))


def make_bot(odoo, hr, lms, **settings):
    logger = logging.getLogger(f"test.{id(odoo)}")
    logger.handlers = [Recorder()]
    logger.setLevel(logging.INFO)
    logger.propagate = False
    bot = LoginBot(odoo, hr, lms, Settings(**settings), logger, clock=lambda: datetime(2026, 11, 11, 9, 5))
    return bot, logger.handlers[0]


ACTIVE = Employee(EMAIL, "Nguyễn Văn A", "active", "Giáo viên")
TERMINATED = Employee(EMAIL, "Nguyễn Văn A", "terminated", "Giáo viên")
DEACTIVATED = LmsAccount(EMAIL, "deactivated", "2026-09-25")
ACTIVE_ACCOUNT = LmsAccount(EMAIL, "active", "2026-11-10")


class DecisionTest(unittest.TestCase):
    def run_bot(self, ticket=None, hr=None, lms=None, **settings):
        odoo = InMemoryOdoo([ticket or login_ticket()])
        lms = lms or FakeLms(DEACTIVATED)
        bot, recorder = make_bot(odoo, hr or FakeHr(ACTIVE), lms, **settings)
        result = bot.process(odoo.fetch_unprocessed()[0])
        return result, odoo, lms, recorder

    def test_active_employee_with_deactivated_account_is_reactivated(self):
        result, odoo, lms, _ = self.run_bot()
        self.assertEqual(result.outcome, Outcome.REACTIVATED)
        self.assertEqual(lms.reactivated, [EMAIL])
        self.assertEqual(lms.resets, [EMAIL])
        self.assertEqual(odoo.stages[1], "Waiting Customer")
        self.assertIn("auto-reactivated", odoo.tickets[1].tags)

    def test_active_employee_with_active_account_gets_password_reset_only(self):
        result, _, lms, _ = self.run_bot(lms=FakeLms(ACTIVE_ACCOUNT))
        self.assertEqual(result.outcome, Outcome.PASSWORD_RESET)
        self.assertEqual(lms.reactivated, [])
        self.assertEqual(lms.resets, [EMAIL])

    def test_terminated_employee_is_never_reactivated(self):
        result, odoo, lms, _ = self.run_bot(hr=FakeHr(TERMINATED))
        self.assertEqual(result.outcome, Outcome.TERMINATED)
        self.assertEqual(lms.reactivated, [])
        self.assertEqual(odoo.stages[1], "Escalated")
        notes = [text for kind, text in odoo.log[1] if kind == "note"]
        self.assertIn("NGHỈ VIỆC", notes[0])

    def test_reply_to_terminated_employee_does_not_reveal_hr_status(self):
        _, odoo, _, _ = self.run_bot(hr=FakeHr(TERMINATED))
        email = [text for kind, text in odoo.log[1] if kind == "note" and "EMAIL GỬI USER" in text][0]
        self.assertNotIn("nghỉ việc", email.lower())

    def test_unknown_email_in_hr_is_escalated(self):
        result, _, lms, _ = self.run_bot(hr=FakeHr(None))
        self.assertEqual(result.outcome, Outcome.ESCALATED)
        self.assertIn("không tìm thấy", result.reason)
        self.assertEqual(lms.reactivated, [])

    def test_employee_without_lms_account_is_escalated(self):
        result, *_ = self.run_bot(lms=FakeLms(None))
        self.assertEqual(result.outcome, Outcome.ESCALATED)
        self.assertIn("chưa có tài khoản LMS", result.reason)

    def test_other_system_is_escalated_without_calling_hr(self):
        hr = FakeHr(ACTIVE)
        result, *_ = self.run_bot(ticket=login_ticket(subject="BU KHÔNG ĐĂNG NHẬP VÀO TMS ĐƯỢC", description=""), hr=hr)
        self.assertEqual(result.outcome, Outcome.ESCALATED)
        self.assertEqual(hr.calls, 0)

    def test_student_account_is_escalated(self):
        result, *_ = self.run_bot(ticket=login_ticket(subject="HV không đăng nhập được Denise"))
        self.assertEqual(result.outcome, Outcome.ESCALATED)

    def test_ticket_without_email_is_escalated_and_gets_no_email(self):
        result, odoo, _, _ = self.run_bot(ticket=login_ticket(email=""))
        self.assertEqual(result.outcome, Outcome.ESCALATED)
        self.assertNotIn("email-draft", result.actions)

    def test_non_login_ticket_is_only_tagged(self):
        result, odoo, _, _ = self.run_bot(ticket=login_ticket(subject="KHÔNG THỂ ENROLL HỌC VIÊN", description=""))
        self.assertEqual(result.outcome, Outcome.NOT_LOGIN)
        self.assertEqual(odoo.tickets[1].tags, (AUTO_TAG,))
        self.assertNotIn(1, odoo.stages)

    def test_hr_outage_fails_safely(self):
        result, odoo, lms, _ = self.run_bot(hr=FakeHr(error=ServiceError("HR timeout")))
        self.assertEqual(result.outcome, Outcome.FAILED)
        self.assertEqual(lms.reactivated, [])
        self.assertEqual(odoo.stages[1], "Escalated")
        self.assertIn("AUTOMATION LỖI", odoo.log[1][1][1])

    def test_lms_outage_fails_safely(self):
        result, *_ = self.run_bot(lms=FakeLms(error=ServiceError("LMS 503")))
        self.assertEqual(result.outcome, Outcome.FAILED)

    def test_odoo_outage_leaves_ticket_for_next_run(self):
        odoo = BrokenOdoo([login_ticket()])
        bot, _ = make_bot(odoo, FakeHr(ACTIVE), FakeLms(DEACTIVATED))
        result = bot.process(odoo.tickets[1])
        self.assertEqual(result.outcome, Outcome.FAILED)
        self.assertNotIn(AUTO_TAG, odoo.tickets[1].tags)


class BehaviourTest(unittest.TestCase):
    def test_ticket_is_processed_only_once(self):
        odoo = InMemoryOdoo([login_ticket()])
        lms = FakeLms(DEACTIVATED)
        bot, _ = make_bot(odoo, FakeHr(ACTIVE), lms)
        self.assertEqual(len(bot.run_once()), 1)
        self.assertEqual(bot.run_once(), [])
        self.assertEqual(bot.process(odoo.tickets[1]).outcome, Outcome.ALREADY_PROCESSED)
        self.assertEqual(lms.reactivated, [EMAIL])

    def test_email_is_sent_through_odoo_when_enabled(self):
        odoo = InMemoryOdoo([login_ticket()])
        bot, _ = make_bot(odoo, FakeHr(ACTIVE), FakeLms(DEACTIVATED), send_email=True)
        result = bot.run_once()[0]
        self.assertIn("email", result.actions)
        email = [text for kind, text in odoo.log[1] if kind == "email"][0]
        self.assertTrue(email.startswith("RE: Không thể đăng nhập vào LMS - Ticket #1"))

    def test_every_decision_is_logged_as_json(self):
        odoo = InMemoryOdoo([login_ticket()])
        bot, recorder = make_bot(odoo, FakeHr(ACTIVE), FakeLms(DEACTIVATED))
        bot.run_once()
        record = recorder.records[0]
        self.assertEqual(record["ticket_id"], 1)
        self.assertEqual(record["outcome"], "reactivated")
        self.assertIn("duration_ms", record)

    def test_dry_run_changes_nothing(self):
        odoo = InMemoryOdoo([login_ticket()])
        lms = FakeLms(DEACTIVATED)
        dry_odoo, dry_lms = DryRunOdoo(odoo), DryRunLms(lms)
        bot, _ = make_bot(dry_odoo, FakeHr(ACTIVE), dry_lms)
        result = bot.run_once()[0]
        self.assertEqual(result.outcome, Outcome.REACTIVATED)
        self.assertEqual(lms.reactivated, [])
        self.assertEqual(odoo.log, {})
        self.assertIn(("reactivate", EMAIL), dry_lms.planned)
        self.assertTrue(dry_odoo.planned[1])


if __name__ == "__main__":
    unittest.main()
