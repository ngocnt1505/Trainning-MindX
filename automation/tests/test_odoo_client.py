"""Kiểm tra OdooClient gọi đúng External API (dùng server XML-RPC giả, không cần Odoo thật)."""

import unittest
import xmlrpc.client

from login_bot.config import Settings
from login_bot.odoo import OdooClient, OdooError, html_to_text, text_to_html

SETTINGS = Settings(odoo_url="https://demo.odoo.com", odoo_db="demo", odoo_user="bot@example.com",
                    odoo_api_key="good-key", odoo_team_id=1)


class FakeOdooServer:
    """Đóng vai cả /xmlrpc/2/common và /xmlrpc/2/object."""

    def __init__(self):
        self.calls = []
        self.tags = {"auto-processed": 11, "week5-sample": 12, "CRM": 13}
        self.fail_message_create = False

    def proxy(self, url, allow_none=True):
        return self

    def version(self):
        return {"server_version": "18.0"}

    def authenticate(self, db, user, key, ctx):
        return 7 if key == "good-key" else False

    def execute_kw(self, db, uid, key, model, method, args, kwargs):
        self.calls.append((model, method, args, kwargs))
        if (model, method) == ("helpdesk.tag", "search"):
            name = args[0][0][2]
            return [self.tags[name]] if name in self.tags else []
        if (model, method) == ("helpdesk.tag", "create"):
            self.tags[args[0]["name"]] = 99
            return 99
        if (model, method) == ("helpdesk.tag", "read"):
            return [{"id": i, "name": n} for n, i in self.tags.items() if i in args[0]]
        if (model, method) == ("helpdesk.ticket", "search_read"):
            return [{"id": 6, "name": "Không thể đăng nhập vào LMS", "description": "<p>Lỗi &quot;Invalid&quot;<br>dòng 2</p>",
                     "partner_email": "a@example.com", "partner_name": "Nguyễn Văn A", "tag_ids": [13]}]
        if (model, method) == ("helpdesk.stage", "search"):
            return {"Escalated": [5], "Mới": [1]}.get(args[0][0][2], [])
        if (model, method) == ("ir.model.data", "search_read"):
            return [{"id": 1, "res_id": 2}]
        if (model, method) == ("mail.message", "create"):
            if self.fail_message_create:
                raise xmlrpc.client.Fault(1, "Access denied")
            return 500
        if (model, method) == ("helpdesk.ticket", "read"):
            return [{"id": args[0][0], "partner_id": [42, "Nguyễn Văn A"]}]
        return True

    def find(self, model, method):
        return [c for c in self.calls if c[0] == model and c[1] == method]


class OdooClientTest(unittest.TestCase):
    def setUp(self):
        self.server = FakeOdooServer()
        self.client = OdooClient(SETTINGS, server_proxy=self.server.proxy)

    def test_wrong_api_key_raises_clear_error(self):
        client = OdooClient(Settings(odoo_url="x", odoo_db="d", odoo_user="u", odoo_api_key="bad"), self.server.proxy)
        with self.assertRaises(OdooError):
            client.get_ticket(1)

    def test_fetch_only_new_tickets_excluding_processed_and_sample(self):
        tickets = self.client.fetch_unprocessed()
        _, _, args, kwargs = self.server.find("helpdesk.ticket", "search_read")[0]
        domain = args[0]
        self.assertIn(("stage_id", "=", 1), domain)
        self.assertIn(("team_id", "=", 1), domain)
        self.assertIn(("tag_ids", "not in", [11, 12]), domain)
        self.assertEqual(kwargs["context"], {"lang": "vi_VN"})
        self.assertEqual(tickets[0].email, "a@example.com")
        self.assertEqual(tickets[0].tags, ("CRM",))
        self.assertEqual(tickets[0].description, 'Lỗi "Invalid"\ndòng 2')

    def test_note_is_created_as_internal_html_message(self):
        self.client.post_note(6, "dòng 1\n<dòng 2>")
        _, _, args, _ = self.server.find("mail.message", "create")[0]
        self.assertEqual(args[0]["res_id"], 6)
        self.assertEqual(args[0]["subtype_id"], 2)
        self.assertEqual(args[0]["body"], "<p>dòng 1<br/>&lt;dòng 2&gt;</p>")

    def test_note_falls_back_to_message_post(self):
        self.server.fail_message_create = True
        self.client.post_note(6, "nội dung")
        _, _, args, kwargs = self.server.find("helpdesk.ticket", "message_post")[0]
        self.assertEqual(args, [[6]])
        self.assertEqual(kwargs["subtype_xmlid"], "mail.mt_note")

    def test_send_email_posts_comment_to_customer(self):
        self.client.send_email(6, "RE: x", "nội dung")
        _, _, _, kwargs = self.server.find("helpdesk.ticket", "message_post")[0]
        self.assertEqual(kwargs["subtype_xmlid"], "mail.mt_comment")
        self.assertEqual(kwargs["partner_ids"], [42])

    def test_add_tags_creates_missing_tag_and_links_it(self):
        self.client.add_tags(6, ["auto-processed", "auto-reactivated"])
        _, _, args, _ = self.server.find("helpdesk.ticket", "write")[0]
        self.assertEqual(args, [[6], {"tag_ids": [(4, 11), (4, 99)]}])

    def test_set_stage_uses_stage_id(self):
        self.client.set_stage(6, "Escalated")
        _, _, args, _ = self.server.find("helpdesk.ticket", "write")[0]
        self.assertEqual(args, [[6], {"stage_id": 5}])

    def test_missing_stage_raises(self):
        with self.assertRaises(OdooError):
            self.client.set_stage(6, "Waiting Customer")


class HtmlTest(unittest.TestCase):
    def test_round_trip(self):
        self.assertEqual(html_to_text(text_to_html("a & b\nc")), "a & b\nc")

    def test_empty_description(self):
        self.assertEqual(html_to_text(False), "")


if __name__ == "__main__":
    unittest.main()
