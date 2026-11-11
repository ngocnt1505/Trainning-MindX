"""End-to-end offline: mock HR/LMS chạy qua HTTP thật + Odoo giả lập + webhook HTTP."""

import dataclasses
import json
import logging
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
import threading

from login_bot.config import Settings
from login_bot.demo_data import DEMO_TICKETS
from login_bot.mock_services import start_server
from login_bot.models import Ticket
from login_bot.odoo import InMemoryOdoo
from login_bot.run import build_bot
from login_bot.stats import summarize
from login_bot.webhook import make_handler


class CaptureLog(logging.Handler):
    def __init__(self):
        super().__init__()
        self.lines = []

    def emit(self, record):
        self.lines.append(record.getMessage())


def demo_odoo():
    return InMemoryOdoo([Ticket(i, s, d, e, n) for i, (s, d, e, n, _) in enumerate(DEMO_TICKETS, start=1)])


class EndToEndTest(unittest.TestCase):
    def setUp(self):
        self.services, self.state = start_server(port=0)
        base = f"http://127.0.0.1:{self.services.server_address[1]}"
        self.settings = Settings(hr_url=base + "/hr", lms_url=base + "/lms", timeout=2, retries=1)
        self.capture = CaptureLog()
        self.logger = logging.getLogger(f"e2e.{id(self)}")
        self.logger.handlers = [self.capture]
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

    def tearDown(self):
        self.services.shutdown()
        self.services.server_close()

    def test_polling_run_handles_every_branch(self):
        odoo = demo_odoo()
        bot = build_bot(self.settings, odoo, self.logger)
        results = bot.run_once()
        self.assertEqual([r.outcome for r in results], [t[-1] for t in DEMO_TICKETS])
        self.assertEqual(self.state.accounts["nguyen.van.a@example.com"]["status"], "active")
        self.assertEqual(self.state.accounts["le.van.c@example.com"]["status"], "deactivated")
        self.assertEqual(bot.run_once(), [])

    def test_stats_from_log(self):
        build_bot(self.settings, demo_odoo(), self.logger).run_once()
        stats = summarize(self.capture.lines)
        self.assertEqual(stats["tickets_checked"], 8)
        self.assertEqual(stats["login_tickets"], 7)
        self.assertEqual(stats["automated"], 2)
        self.assertEqual(stats["manual_minutes_saved"], [10, 20])

    def test_hr_down_marks_ticket_failed(self):
        settings = dataclasses.replace(self.settings, hr_url="http://127.0.0.1:1/hr")
        odoo = InMemoryOdoo([Ticket(1, *DEMO_TICKETS[0][:4])])
        result = build_bot(settings, odoo, self.logger).run_once()[0]
        self.assertEqual(result.outcome.value, "failed")
        self.assertEqual(odoo.stages[1], "Escalated")
        self.assertEqual(self.state.accounts["nguyen.van.a@example.com"]["status"], "deactivated")


class WebhookTest(unittest.TestCase):
    def setUp(self):
        self.services, _ = start_server(port=0)
        base = f"http://127.0.0.1:{self.services.server_address[1]}"
        settings = Settings(hr_url=base + "/hr", lms_url=base + "/lms", timeout=2, retries=1)
        logger = logging.getLogger(f"webhook.{id(self)}")
        logger.handlers = [logging.NullHandler()]
        logger.propagate = False
        self.odoo = demo_odoo()
        bot = build_bot(settings, self.odoo, logger)
        self.webhook = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(bot, token="s3cret"))
        threading.Thread(target=self.webhook.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.webhook.server_address[1]}/odoo/ticket"

    def tearDown(self):
        for server in (self.webhook, self.services):
            server.shutdown()
            server.server_close()

    def post(self, body, query="?token=s3cret"):
        req = urllib.request.Request(self.url + query, data=json.dumps(body).encode(), method="POST",
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status, json.loads(resp.read())
        except urllib.error.HTTPError as err:
            return err.code, json.loads(err.read())

    def test_odoo_payload_triggers_processing(self):
        status, body = self.post({"_model": "helpdesk.ticket", "_id": 1, "id": 1, "name": "..."})
        self.assertEqual(status, 200)
        self.assertEqual(body["outcome"], "reactivated")
        self.assertEqual(self.odoo.stages[1], "Waiting Customer")

    def test_repeated_webhook_does_not_process_twice(self):
        self.post({"_id": 2})
        status, body = self.post({"_id": 2})
        self.assertEqual(body["outcome"], "already_processed")

    def test_wrong_token_is_rejected(self):
        status, _ = self.post({"_id": 1}, query="?token=sai")
        self.assertEqual(status, 401)
        self.assertNotIn(1, self.odoo.stages)

    def test_missing_id_is_bad_request(self):
        self.assertEqual(self.post({"name": "x"})[0], 400)

    def test_unknown_ticket_is_not_found(self):
        self.assertEqual(self.post({"_id": 999})[0], 404)


if __name__ == "__main__":
    unittest.main()
