"""Nhận diện ticket lỗi đăng nhập bằng từ khóa (tiếng Việt đã bỏ dấu + tiếng Anh)."""

import re
import unicodedata
from dataclasses import dataclass

LOGIN_PATTERNS = {
    "dang nhap": r"dang nhap",
    "login": r"\blog ?in\b|\bsign ?in\b",
    "mat khau": r"mat khau",
    "password": r"password",
    "bi khoa": r"bi khoa|khoa tai khoan|\blocked\b",
    "deactivated": r"deactivat|vo hieu hoa",
    "khong vao duoc": r"khong (the )?vao (duoc )?(he thong|lms|tms|crm|tai khoan)|khong vao duoc",
    "khong truy cap": r"khong (the )?truy cap",
    "tai khoan loi": r"tai khoan (bi )?loi",
}

STUDENT_PATTERN = r"\bhv\b|hoc vien|hoc sinh|phu huynh|cho be\b|denise"

# Hệ thống được nhắc tới trong ticket. Bot chỉ xử lý LMS (hoặc không ghi rõ hệ thống).
SYSTEM_PATTERNS = {
    "lms": r"\blms\b",
    "tms": r"\btms\b",
    "crm": r"\bcrm\b",
    "ecount": r"\be ?count\b",
    "mail": r"outlook|(mat khau|tai khoan|hop thu) e?mail|\be?mail (cong viec|noi bo)",
}
SUPPORTED_SYSTEMS = {None, "lms"}


@dataclass(frozen=True)
class Classification:
    is_login: bool
    keywords: tuple
    system: str = None
    is_student: bool = False

    @property
    def in_scope(self):
        return self.is_login and not self.is_student and self.system in SUPPORTED_SYSTEMS


def normalize(text):
    text = (text or "").replace("Đ", "D").replace("đ", "d")
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", text.lower())


def detect_system(text):
    if re.search(SYSTEM_PATTERNS["lms"], text):
        return "lms"
    for name, pattern in SYSTEM_PATTERNS.items():
        if re.search(pattern, text):
            return name
    return None


def classify(subject, description=""):
    subject_text = normalize(subject)
    text = f"{subject_text} {normalize(description)}"
    keywords = tuple(name for name, pattern in LOGIN_PATTERNS.items() if re.search(pattern, text))
    if not keywords:
        return Classification(is_login=False, keywords=())
    # Ưu tiên hệ thống ghi ở tiêu đề; mô tả hay nhắc tới hệ thống khác một cách ngẫu nhiên.
    system = detect_system(subject_text) or detect_system(text)
    return Classification(
        is_login=True,
        keywords=keywords,
        system=system,
        is_student=bool(re.search(STUDENT_PATTERN, text)),
    )
