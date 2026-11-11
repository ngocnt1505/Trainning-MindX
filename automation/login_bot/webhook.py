"""Trigger kiểu webhook: Odoo gọi vào đây ngay khi có ticket mới.

    python -m login_bot.webhook --port 8070

Cấu hình trong Odoo: Automation Rule trên Helpdesk Ticket, trigger "On creation",
action "Send Webhook Notification", URL = https://<địa chỉ public>/odoo/ticket?token=<LOGIN_BOT_WEBHOOK_TOKEN>
(xem docs4/automation.md mục 6.3). Odoo gửi JSON có "_id"/"id" của ticket; bot đọc lại ticket qua API
rồi xử lý, nên không tin dữ liệu khác trong payload.
"""

import argparse
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .config import load_settings
from .odoo import OdooClient, OdooError


def make_handler(bot, token=""):
    lock = threading.Lock()  # xử lý tuần tự để 2 webhook cùng ticket không chạy song song

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send_json(self, code, body):
            payload = json.dumps(body, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self):
            if urlparse(self.path).path == "/health":
                return self.send_json(200, {"status": "ok"})
            return self.send_json(404, {"error": "not found"})

        def do_POST(self):
            url = urlparse(self.path)
            if url.path != "/odoo/ticket":
                return self.send_json(404, {"error": "not found"})
            sent_token = parse_qs(url.query).get("token", [""])[0] or self.headers.get("X-Login-Bot-Token", "")
            if token and sent_token != token:
                return self.send_json(401, {"error": "sai token"})
            try:
                payload = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
                ticket_id = int(payload.get("_id") or payload.get("id"))
            except (ValueError, TypeError):
                return self.send_json(400, {"error": "payload phải có _id hoặc id của ticket"})
            with lock:
                try:
                    ticket = bot.odoo.get_ticket(ticket_id)
                    if ticket is None:
                        return self.send_json(404, {"error": f"không có ticket {ticket_id}"})
                    result = bot.process(ticket)
                except OdooError as err:
                    return self.send_json(502, {"error": str(err)})
            return self.send_json(200, {"ticket_id": result.ticket_id, "outcome": result.outcome.value,
                                        "reason": result.reason, "actions": result.actions})

    return Handler


def main(argv=None):
    from .run import build_bot, setup_logging

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Webhook nhận ticket mới từ Odoo")
    parser.add_argument("--port", type=int, default=8070)
    args = parser.parse_args(argv)
    settings = load_settings()
    if not settings.has_odoo:
        print("Thiếu cấu hình Odoo trong .env")
        return 2
    bot = build_bot(settings, OdooClient(settings), setup_logging(settings.log_file))
    server = ThreadingHTTPServer(("0.0.0.0", args.port), make_handler(bot, settings.webhook_token))
    print(f"Webhook đang chạy: POST http://localhost:{args.port}/odoo/ticket (Ctrl+C để dừng)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
