"""Chạy login bot.

    python -m login_bot.run --demo              # chạy thử offline: mock HR/LMS + Odoo giả lập
    python -m login_bot.run --check-odoo        # kiểm tra kết nối + cấu hình Odoo
    python -m login_bot.run --once --dry-run    # đọc ticket Odoo thật, chỉ in việc sẽ làm
    python -m login_bot.run --once              # xử lý ticket mới 1 lần
    python -m login_bot.run --interval 300      # chạy theo lịch, 5 phút/lần (trigger kiểu polling)
"""

import argparse
import dataclasses
import json
import logging
import sys
import time
from collections import Counter
from pathlib import Path

from .config import load_settings
from .demo_data import DEMO_TICKETS
from .models import Ticket
from .odoo import DryRunOdoo, InMemoryOdoo, OdooClient, OdooError
from .services import DryRunLms, HrClient, JsonHttpClient, LmsClient
from .workflow import LoginBot


def setup_logging(log_file):
    logger = logging.getLogger("login_bot")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    return logger


def build_bot(settings, odoo, logger=None, dry_run=False):
    hr = HrClient(JsonHttpClient(settings.hr_url, settings.timeout, settings.retries))
    lms = LmsClient(JsonHttpClient(settings.lms_url, settings.timeout, settings.retries))
    if dry_run:
        odoo, lms = DryRunOdoo(odoo), DryRunLms(lms)
    return LoginBot(odoo, hr, lms, settings, logger)


def print_results(results):
    for r in results:
        print(f"  #{r.ticket_id:<5} {r.outcome.value:<18} {r.reason}")
    counts = Counter(r.outcome.value for r in results)
    print(f"  => {len(results)} ticket: " + (", ".join(f"{k} {v}" for k, v in sorted(counts.items())) or "không có ticket mới"))


def print_actions(store, ticket_ids):
    for ticket_id in ticket_ids:
        for kind, content in store.get(ticket_id, []):
            print(f"  [#{ticket_id} {kind}] " + content.replace("\n", "\n" + " " * 10))


def run_demo(settings, logger):
    from .mock_services import start_server

    server, _ = start_server(port=0)
    base = f"http://127.0.0.1:{server.server_address[1]}"
    settings = dataclasses.replace(settings, hr_url=base + "/hr", lms_url=base + "/lms", send_email=False)
    odoo = InMemoryOdoo([Ticket(i, s, d, e, n) for i, (s, d, e, n, _) in enumerate(DEMO_TICKETS, start=1)])
    bot = build_bot(settings, odoo, logger)

    print(f"DEMO - mock HR/LMS tại {base}, Odoo giả lập với {len(DEMO_TICKETS)} ticket\n")
    print("Lần chạy 1:")
    results = bot.run_once()
    print_results(results)
    print("\nKiểm tra với kết quả mong đợi:")
    ok = True
    for r, (subject, *_, expected) in zip(results, DEMO_TICKETS):
        match = r.outcome == expected
        ok &= match
        print(f"  {'OK ' if match else 'SAI'} #{r.ticket_id} {subject[:45]:<45} mong đợi {expected.value}, thực tế {r.outcome.value}")
    print("\nLần chạy 2 (phải không xử lý lại ticket nào):")
    print_results(bot.run_once())
    print("\nChi tiết những gì bot ghi lên ticket #1 (Scenario 1) và #3 (nghỉ việc):")
    print_actions(odoo.log, [1, 3])
    print(f"\nKết quả trạng thái: { {i: s for i, s in sorted(odoo.stages.items())} }")
    server.shutdown()
    return 0 if ok else 1


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Login bot - tự xử lý ticket lỗi đăng nhập trên Odoo Helpdesk")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--demo", action="store_true", help="chạy offline với mock HR/LMS và Odoo giả lập")
    mode.add_argument("--check-odoo", action="store_true", help="kiểm tra kết nối và cấu hình Odoo")
    mode.add_argument("--once", action="store_true", help="xử lý ticket mới 1 lần")
    mode.add_argument("--interval", type=int, metavar="GIÂY", help="chạy lặp theo lịch")
    parser.add_argument("--dry-run", action="store_true", help="không ghi gì vào Odoo/LMS, chỉ in việc sẽ làm")
    args = parser.parse_args(argv)

    settings = load_settings()
    logger = setup_logging(settings.log_file)
    if args.demo:
        return run_demo(settings, logger)

    if not settings.has_odoo:
        print("Thiếu ODOO_URL / ODOO_DB / ODOO_USER / ODOO_API_KEY. Copy .env.example thành .env rồi điền.")
        return 2
    client = OdooClient(settings)
    if args.check_odoo:
        try:
            print(json.dumps(client.check(), ensure_ascii=False, indent=2))
            return 0
        except OdooError as err:
            print(f"LỖI: {err}")
            return 1

    if args.dry_run:
        # Dry-run không ghi log để không làm sai thống kê (login_bot.stats).
        logger = logging.getLogger("login_bot.dry_run")
        logger.propagate = False
    bot = build_bot(settings, client, logger, dry_run=args.dry_run)
    while True:
        try:
            results = bot.run_once()
            print(time.strftime("%H:%M:%S"), "- chạy xong:")
            print_results(results)
            if args.dry_run:
                print_actions(bot.odoo.planned, [r.ticket_id for r in results])
                for action, email in bot.lms.planned:
                    print(f"  [LMS] sẽ {action} {email}")
        except OdooError as err:
            print(f"LỖI Odoo: {err}")
            if not args.interval:
                return 1
        if not args.interval:
            return 0
        try:
            time.sleep(args.interval)
        except KeyboardInterrupt:
            return 0


if __name__ == "__main__":
    sys.exit(main())
