"""Phân nhóm ticket trong week-5/data/sample.xlsx theo loại vấn đề.

Chạy từ thư mục gốc của repo (chỉ dùng thư viện chuẩn của Python):

    python docs4/reports/classify_tickets.py

Kết quả:
    docs4/reports/tickets-classified.csv  - từng ticket kèm nhóm
    docs4/reports/group-summary.csv       - số liệu tổng hợp theo nhóm
    docs4/reports/odoo-import.csv         - file import vào Odoo Helpdesk để làm report
"""

import collections
import csv
import re
import unicodedata
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "week-5" / "data" / "sample.xlsx"
OUT_DIR = Path(__file__).resolve().parent

LOGIN = "Không đăng nhập được / quên mật khẩu / bị khóa"
ACCOUNT = "Cấp mới / chuyển tài khoản, email"
STUDENT = "Trạng thái / Thông tin học viên"
TEST = "(Ticket test - loại)"

# Luật theo từ khóa (tiêu đề đã bỏ dấu, viết thường). Luật đầu tiên khớp sẽ được dùng.
RULES = [
    ("Điểm thưởng / Đổi quà", r"diem thuong|doi qua|cong diem|tick diem"),
    ("TMS / Chấm công / Điểm danh", r"tms|cham cong|bu cong|bang cong|hien thi cong|diem danh"),
    (LOGIN, r"dang nhap|mat khau|mat khau|tai khoan|truy cap|bi khoa|activation"),
    (STUDENT, r"mail"),
    ("Enroll / Xếp lớp học viên", r"enroll|vao lop|slot|add gv|tim ra lop|add hoc vien|hoc phan|run lai buoi demo|gio hoc|^tk-rob|^tdm-c4k"),
    ("Lead / Thanh toán / Order (CRM)", r"lead|payment|patment|confirm|order|oder|giao dich|dong tien|qr thanh toan|giam gia|gia hoa don|upsale|^sale$|xuat du lieu|doi duoc trang thai"),
    ("Hợp đồng điện tử (E-contract)", r"hop dong|econtract"),
    ("Phiếu Dropout", r"drop ?out"),
    ("CRM gọi điện / SMS", r"goi duoc|tin nhan|cuoc goi"),
    ("Đặt phòng (Crystal)", r"phong|crystal"),
    (STUDENT, r"trang thai hoc vien|ten hv|ten dung|compass"),
]

# Sửa tay sau khi đọc lại từng ticket (lý do ghi trong docs4/analysis.md, mục 2).
OVERRIDES = {
    "222": LOGIN,     # tag "HV không đăng nhập được"
    "172": LOGIN,     # cấp lại mật khẩu mail
    "241": LOGIN, "253": LOGIN, "265": LOGIN,  # không vào được TMS, không phải lỗi chấm công
    "129": ACCOUNT, "174": ACCOUNT, "230": ACCOUNT, "259": ACCOUNT,
    "237": ACCOUNT, "248": ACCOUNT, "276": ACCOUNT, "308": ACCOUNT,
    "286": STUDENT, "288": STUDENT,  # sửa tên HV trong enrollment
    "58": TEST,
}


# Tag ngắn cho từng nhóm khi import vào Odoo (tag Odoo không được chứa dấu phẩy).
GROUP_TAGS = {
    "Lead / Thanh toán / Order (CRM)": "grp-lead-payment",
    "Enroll / Xếp lớp học viên": "grp-enroll",
    "TMS / Chấm công / Điểm danh": "grp-tms",
    LOGIN: "grp-login",
    ACCOUNT: "grp-account",
    STUDENT: "grp-student-info",
    "Hợp đồng điện tử (E-contract)": "grp-econtract",
    "Điểm thưởng / Đổi quà": "grp-reward",
    "CRM gọi điện / SMS": "grp-crm-call",
    "Phiếu Dropout": "grp-dropout",
    "Đặt phòng (Crystal)": "grp-room",
    "Khác": "grp-other",
}
ODOO_PRIORITY = {"Low priority": "0", "Medium priority": "1", "High priority": "2", "Urgent": "3"}
ODOO_STAGE = {"New": "Mới", "First Response Sent": "Đang thực hiện", "In Progress": "Đang thực hiện",
              "Resolved": "Đã xử lý"}
SAMPLE_TAG = "week5-sample"


def strip_accents(text):
    text = text.replace("Đ", "D").replace("đ", "d")
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn").lower().strip()


def read_rows(path):
    """Đọc sheet đầu tiên của file xlsx thành list[dict cột -> giá trị]."""
    with zipfile.ZipFile(path) as z:
        shared = [
            "".join(re.findall(r"<t[^>]*>(.*?)</t>", si, re.S))
            for si in re.findall(r"<si>(.*?)</si>", z.read("xl/sharedStrings.xml").decode(), re.S)
        ]
        sheet = z.read("xl/worksheets/sheet1.xml").decode()
    rows = []
    for row in re.findall(r"<row[^>]*>(.*?)</row>", sheet, re.S):
        cells = {}
        for col, attrs, body in re.findall(r'<c r="([A-Z]+)\d+"([^>]*?)(?:/>|>(.*?)</c>)', row, re.S):
            value = re.search(r"<v>(.*?)</v>", body or "")
            value = value.group(1) if value else ""
            if 't="s"' in attrs and value:
                value = shared[int(value)]
            if value:
                cells[col] = value.replace("&amp;", "&")
        rows.append(cells)
    return rows


def parse_tickets(rows):
    """Export của Odoo được nhóm theo giai đoạn: dòng 'Resolved (91)' là tiêu đề nhóm,
    dòng chỉ có cột N là tag thứ 2, 3... của ticket ngay phía trên."""
    tickets, stage = [], None
    for cells in rows[1:]:
        if "K" in cells:
            tickets.append({
                "id": cells["L"],
                "subject": cells["K"].strip(),
                "customer": cells.get("M", ""),
                "tags": [cells["N"]] if "N" in cells else [],
                "priority": cells.get("Q", ""),
                "stage": stage,
            })
        elif "A" in cells:
            stage = cells["A"].rsplit(" (", 1)[0]
        elif "N" in cells:
            tickets[-1]["tags"].append(cells["N"])
    return tickets


def classify(ticket):
    if ticket["id"] in OVERRIDES:
        return OVERRIDES[ticket["id"]]
    subject = strip_accents(ticket["subject"])
    for group, pattern in RULES:
        if re.search(pattern, subject):
            return group
    return "Khác"


def main():
    tickets = [t for t in parse_tickets(read_rows(SOURCE)) if t["stage"] != "Cancelled"]
    for t in tickets:
        t["group"] = classify(t)
    tickets = [t for t in tickets if t["group"] != TEST]

    with open(OUT_DIR / "tickets-classified.csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "subject", "customer", "tags", "priority", "stage", "group"])
        for t in tickets:
            writer.writerow([t["id"], t["subject"], t["customer"], "; ".join(t["tags"]),
                             t["priority"], t["stage"], t["group"]])

    # Header dùng tên kỹ thuật của field để màn hình Import của Odoo tự map cột.
    with open(OUT_DIR / "odoo-import.csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "partner_name", "priority", "stage_id", "tag_ids", "description"])
        for t in tickets:
            tags = [SAMPLE_TAG, GROUP_TAGS[t["group"]], *(x for x in t["tags"] if "," not in x)]
            writer.writerow([t["subject"], t["customer"], ODOO_PRIORITY.get(t["priority"], "0"),
                             ODOO_STAGE.get(t["stage"], "Mới"), ",".join(dict.fromkeys(tags)),
                             f"Ticket #{t['id']} trong week-5/data/sample.xlsx"])

    groups = collections.defaultdict(list)
    for t in tickets:
        groups[t["group"]].append(t)
    total = len(tickets)
    with open(OUT_DIR / "group-summary.csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["group", "tickets", "percent", "distinct_senders", "urgent_or_high", "not_resolved"])
        for group, items in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            row = [group, len(items), f"{len(items) / total:.0%}",
                   len({t["customer"] for t in items}),
                   sum(t["priority"] in ("Urgent", "High priority") for t in items),
                   sum(t["stage"] != "Resolved" for t in items)]
            writer.writerow(row)
            print(*row, sep=" | ")
    print("Tổng:", total)


if __name__ == "__main__":
    main()
