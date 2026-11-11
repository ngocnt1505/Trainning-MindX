"""Đo bộ nhận diện lỗi đăng nhập trên 118 ticket thật của sample.xlsx.

Nhãn đúng = nhóm "Không đăng nhập được / quên mật khẩu / bị khóa" do người phân loại
(docs4/reports/tickets-classified.csv). Chạy từ thư mục automation/:

    python evaluate_classifier.py
"""

import csv
import sys
from collections import Counter
from pathlib import Path

from login_bot.classifier import classify

CSV = Path(__file__).resolve().parent.parent / "docs4" / "reports" / "tickets-classified.csv"
LOGIN_GROUP = "Không đăng nhập được / quên mật khẩu / bị khóa"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    tp, fp, fn = [], [], []
    routes = Counter()
    for row in rows:
        c = classify(row["subject"])
        actual = row["group"] == LOGIN_GROUP
        if c.is_login and actual:
            tp.append(row)
        elif c.is_login:
            fp.append(row)
        elif actual:
            fn.append(row)
        if c.is_login:
            routes["bot xử lý (LMS / không ghi rõ hệ thống)" if c.in_scope else
                   "học viên -> chuyển người" if c.is_student else
                   f"hệ thống {c.system.upper()} -> chuyển người"] += 1

    precision = len(tp) / (len(tp) + len(fp)) if tp or fp else 0
    recall = len(tp) / (len(tp) + len(fn)) if tp or fn else 0
    print(f"Ticket: {len(rows)} | nhãn lỗi đăng nhập: {len(tp) + len(fn)}")
    print(f"Đúng (TP): {len(tp)} | Báo nhầm (FP): {len(fp)} | Bỏ sót (FN): {len(fn)}")
    print(f"Precision: {precision:.0%} | Recall: {recall:.0%}")
    for name, items in (("Báo nhầm", fp), ("Bỏ sót", fn)):
        for row in items:
            print(f"  {name}: #{row['id']} {row['subject']}  [{row['group']}]")
    print("Ticket bot nhận là lỗi đăng nhập sẽ đi nhánh:")
    for route, n in routes.most_common():
        print(f"  {n:3}  {route}")


if __name__ == "__main__":
    main()
