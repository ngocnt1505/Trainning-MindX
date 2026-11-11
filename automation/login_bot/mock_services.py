"""Mock HR system + LMS (MindX không cấp API thật cho bài tập).

    python -m login_bot.mock_services --port 8090

HR:  GET  /hr/employees?email=...           -> 200 {email, name, status, department} | 404
LMS: GET  /lms/accounts?email=...           -> 200 {email, status, last_login} | 404
     POST /lms/accounts/reactivate          {"email"} -> 200 {email, status: "active"} | 404
     POST /lms/accounts/password-reset      {"email"} -> 200 {email, reset_link} | 404
"""

import argparse
import copy
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

DATA_FILE = Path(__file__).with_name("mock_data.json")


class MockState:
    def __init__(self, data):
        self.lock = threading.Lock()
        self.employees = {e["email"].lower(): e for e in data["employees"]}
        self.accounts = {a["email"].lower(): a for a in data["lms_accounts"]}
        self.calls = []


def load_state(path=DATA_FILE):
    return MockState(copy.deepcopy(json.loads(Path(path).read_text(encoding="utf-8"))))


def make_handler(state):
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
            url = urlparse(self.path)
            email = parse_qs(url.query).get("email", [""])[0].lower()
            state.calls.append(("GET", url.path, email))
            table = {"/hr/employees": state.employees, "/lms/accounts": state.accounts}.get(url.path)
            if table is None:
                return self.send_json(404, {"error": "not found"})
            record = table.get(email)
            return self.send_json(200, record) if record else self.send_json(404, {"error": "unknown email"})

        def do_POST(self):
            length = int(self.headers.get("Content-Length") or 0)
            email = json.loads(self.rfile.read(length) or b"{}").get("email", "").lower()
            state.calls.append(("POST", self.path, email))
            with state.lock:
                account = state.accounts.get(email)
                if account is None:
                    return self.send_json(404, {"error": "unknown account"})
                if self.path == "/lms/accounts/reactivate":
                    account["status"] = "active"
                    account.pop("deactivated_reason", None)
                    return self.send_json(200, account)
                if self.path == "/lms/accounts/password-reset":
                    return self.send_json(200, {"email": email, "reset_link": f"https://lms.mindx.edu.vn/reset?u={email}"})
            return self.send_json(404, {"error": "not found"})

    return Handler


def start_server(port=0, state=None):
    """Chạy server ở thread nền (dùng trong test và --demo). Trả về (server, state)."""
    state = state or load_state()
    server = ThreadingHTTPServer(("127.0.0.1", port), make_handler(state))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, state


def main():
    parser = argparse.ArgumentParser(description="Mock HR + LMS API")
    parser.add_argument("--port", type=int, default=8090)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(load_state()))
    print(f"Mock HR + LMS đang chạy tại http://127.0.0.1:{args.port} (Ctrl+C để dừng)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
