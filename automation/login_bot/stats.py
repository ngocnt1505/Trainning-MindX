"""Thống kê hiệu quả bot từ file log (dùng cho mục "trước/sau" khi thuyết trình).

    python -m login_bot.stats [đường_dẫn_log]
"""

import json
import sys
from collections import Counter

from .config import load_settings
from .models import AUTOMATED_OUTCOMES, Outcome

MANUAL_MINUTES = (5, 10)  # thời gian xử lý tay 1 ticket đăng nhập (tasks.md Week 5)


def summarize(lines):
    records = [json.loads(line) for line in lines if line.strip()]
    records = [r for r in records if r["outcome"] != Outcome.ALREADY_PROCESSED.value]
    counts = Counter(r["outcome"] for r in records)
    login = sum(n for k, n in counts.items() if k != Outcome.NOT_LOGIN.value)
    automated = sum(counts[o.value] for o in AUTOMATED_OUTCOMES)
    durations = [r["duration_ms"] for r in records if r["outcome"] in {o.value for o in AUTOMATED_OUTCOMES}]
    return {
        "tickets_checked": len(records),
        "login_tickets": login,
        "automated": automated,
        "automation_rate": round(automated / login, 2) if login else 0,
        "by_outcome": dict(counts),
        "avg_bot_seconds": round(sum(durations) / len(durations) / 1000, 2) if durations else 0,
        "manual_minutes_saved": [automated * m for m in MANUAL_MINUTES],
    }


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0] if argv else load_settings().log_file
    with open(path, encoding="utf-8") as f:
        print(json.dumps(summarize(f), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
