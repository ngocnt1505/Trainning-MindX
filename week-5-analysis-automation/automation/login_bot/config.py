"""Cấu hình đọc từ biến môi trường hoặc file automation/.env (xem .env.example)."""

import os
from dataclasses import dataclass
from pathlib import Path

AUTOMATION_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    odoo_url: str = ""
    odoo_db: str = ""
    odoo_user: str = ""
    odoo_api_key: str = ""
    odoo_lang: str = "vi_VN"
    odoo_team_id: int = 0
    hr_url: str = "http://127.0.0.1:8090/hr"
    lms_url: str = "http://127.0.0.1:8090/lms"
    send_email: bool = False
    stage_new: str = "Mới"
    stage_waiting: str = "Waiting Customer"
    stage_escalated: str = "Escalated"
    skip_tags: tuple = ("week5-sample",)
    timeout: float = 5.0
    retries: int = 3
    webhook_token: str = ""
    log_file: str = str(AUTOMATION_DIR / "logs" / "login_bot.log")

    @property
    def has_odoo(self):
        return all([self.odoo_url, self.odoo_db, self.odoo_user, self.odoo_api_key])


def read_env_file(path):
    values = {}
    if not Path(path).exists():
        return values
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def load_settings(env=None, env_file=AUTOMATION_DIR / ".env"):
    values = read_env_file(env_file)
    values.update(os.environ if env is None else env)
    get = values.get
    defaults = Settings()
    return Settings(
        odoo_url=get("ODOO_URL", "").rstrip("/"),
        odoo_db=get("ODOO_DB", ""),
        odoo_user=get("ODOO_USER", ""),
        odoo_api_key=get("ODOO_API_KEY", ""),
        odoo_lang=get("ODOO_LANG", defaults.odoo_lang),
        odoo_team_id=int(get("ODOO_TEAM_ID", "0") or 0),
        hr_url=get("HR_API_URL", defaults.hr_url).rstrip("/"),
        lms_url=get("LMS_API_URL", defaults.lms_url).rstrip("/"),
        send_email=get("LOGIN_BOT_SEND_EMAIL", "false").lower() == "true",
        stage_new=get("ODOO_STAGE_NEW", defaults.stage_new),
        stage_waiting=get("ODOO_STAGE_WAITING", defaults.stage_waiting),
        stage_escalated=get("ODOO_STAGE_ESCALATED", defaults.stage_escalated),
        skip_tags=tuple(t.strip() for t in get("LOGIN_BOT_SKIP_TAGS", ",".join(defaults.skip_tags)).split(",") if t.strip()),
        timeout=float(get("LOGIN_BOT_TIMEOUT", defaults.timeout)),
        retries=int(get("LOGIN_BOT_RETRIES", defaults.retries)),
        webhook_token=get("LOGIN_BOT_WEBHOOK_TOKEN", ""),
        log_file=get("LOGIN_BOT_LOG_FILE", defaults.log_file),
    )
