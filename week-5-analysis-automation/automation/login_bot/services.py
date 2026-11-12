"""Client HTTP cho HR system và LMS (trong bài dùng mock_services.py thay cho hệ thống thật)."""

import json
import time
import urllib.error
import urllib.parse
import urllib.request

from .models import Employee, LmsAccount


class ServiceError(Exception):
    """HR hoặc LMS không trả lời được sau khi đã thử lại."""


class JsonHttpClient:
    def __init__(self, base_url, timeout=5.0, retries=3, backoff=0.5):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = max(1, retries)
        self.backoff = backoff

    def request(self, method, path, body=None):
        """Trả về dict JSON, hoặc None nếu 404. Lỗi mạng / 5xx được thử lại."""
        url = self.base_url + path
        data = json.dumps(body).encode() if body is not None else None
        last_error = None
        for attempt in range(1, self.retries + 1):
            req = urllib.request.Request(url, data=data, method=method,
                                         headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    return json.loads(resp.read().decode() or "{}")
            except urllib.error.HTTPError as err:
                if err.code == 404:
                    return None
                if err.code < 500:
                    raise ServiceError(f"{method} {url} -> HTTP {err.code}") from err
                last_error = err
            except (urllib.error.URLError, TimeoutError, ConnectionError) as err:
                last_error = err
            if attempt < self.retries:
                time.sleep(self.backoff * attempt)
        raise ServiceError(f"{method} {url} lỗi sau {self.retries} lần thử: {last_error}")


class HrClient:
    def __init__(self, http):
        self.http = http

    def get_employee(self, email):
        data = self.http.request("GET", "/employees?email=" + urllib.parse.quote(email))
        if data is None:
            return None
        return Employee(email=data["email"], name=data.get("name", ""),
                        status=data["status"], department=data.get("department", ""))


class LmsClient:
    def __init__(self, http):
        self.http = http

    def get_account(self, email):
        data = self.http.request("GET", "/accounts?email=" + urllib.parse.quote(email))
        if data is None:
            return None
        return LmsAccount(email=data["email"], status=data["status"], last_login=data.get("last_login", ""))

    def reactivate(self, email):
        data = self.http.request("POST", "/accounts/reactivate", {"email": email})
        if data is None or data.get("status") != "active":
            raise ServiceError(f"LMS không reactivate được {email}: {data}")

    def send_password_reset(self, email):
        """LMS tự gửi email đặt lại mật khẩu; trả về link (để ghi vào note)."""
        data = self.http.request("POST", "/accounts/password-reset", {"email": email})
        if data is None:
            raise ServiceError(f"LMS không gửi được link đặt lại mật khẩu cho {email}")
        return data.get("reset_link", "")


class DryRunLms:
    """Đọc trạng thái tài khoản thật nhưng không reactivate / không gửi link."""

    def __init__(self, inner):
        self.inner = inner
        self.planned = []

    def get_account(self, email):
        return self.inner.get_account(email)

    def reactivate(self, email):
        self.planned.append(("reactivate", email))

    def send_password_reset(self, email):
        self.planned.append(("password-reset", email))
        return "(dry-run)"
