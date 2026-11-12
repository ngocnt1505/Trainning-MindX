"""Tạo bộ ticket test (demo_data.py) trên Odoo thật để test end-to-end.

    python -m login_bot.seed_odoo
"""

import sys

from .config import load_settings
from .demo_data import DEMO_TICKETS, TEST_TAG
from .odoo import OdooClient, OdooError


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    settings = load_settings()
    if not settings.has_odoo:
        print("Thiếu cấu hình Odoo trong .env")
        return 2
    client = OdooClient(settings)
    try:
        for subject, description, email, customer, expected in DEMO_TICKETS:
            ticket_id = client.create_ticket(subject, description, email, customer, tags=[TEST_TAG])
            print(f"Tạo ticket #{ticket_id}: {subject}  (mong đợi: {expected.value})")
    except OdooError as err:
        print(f"LỖI: {err}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
