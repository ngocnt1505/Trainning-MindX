"""Bộ ticket test dùng chung cho --demo, test end-to-end và seed_odoo (tạo ticket thật trên Odoo).

Mỗi ticket phủ một nhánh trong bảng quyết định. Email dùng domain example.com (giống Week 4)
để không gửi nhầm tới người thật.
"""

from .models import Outcome

SCENARIO_1_EMAIL = (
    "Chào Tech team,\n"
    "Em đang cố đăng nhập vào LMS nhưng cứ bị lỗi \"Invalid username or password\".\n"
    "Em chắc chắn mật khẩu của em đúng. Em cần truy cập tài liệu lớp học cho buổi học hôm nay.\n"
    "Cảm ơn, Giáo viên Nguyễn Văn A"
)

# (tiêu đề, mô tả, email, tên khách hàng, kết quả mong đợi)
DEMO_TICKETS = [
    ("Không thể đăng nhập vào LMS", SCENARIO_1_EMAIL,
     "nguyen.van.a@example.com", "Nguyễn Văn A", Outcome.REACTIVATED),
    ("Quên mật khẩu LMS", "Em quên mật khẩu, nhờ team hỗ trợ.",
     "tran.thi.b@example.com", "Trần Thị B", Outcome.PASSWORD_RESET),
    ("LMS báo tài khoản bị khóa", "Em không vào được LMS, báo tài khoản bị khóa.",
     "le.van.c@example.com", "Lê Văn C", Outcome.TERMINATED),
    ("Không đăng nhập được LMS", "Em là giáo viên mới, không đăng nhập được.",
     "unknown.user@example.com", "Người dùng lạ", Outcome.ESCALATED),
    ("BU KHÔNG ĐĂNG NHẬP VÀO TMS ĐƯỢC", "Không vào được TMS để duyệt công.",
     "pham.thi.d@example.com", "Phạm Thị D", Outcome.ESCALATED),
    ("PNL HỖ TRỢ TÀI KHOẢN DENISE - HV không đăng nhập được", "Học viên lớp GA28 không đăng nhập được Denise.",
     "pham.thi.d@example.com", "Phạm Thị D", Outcome.ESCALATED),
    ("Không đăng nhập được LMS lần đầu", "Em mới vào làm, chưa đăng nhập LMS được lần nào.",
     "hoang.van.e@example.com", "Hoàng Văn E", Outcome.ESCALATED),
    ("KHÔNG THỂ ENROLL HỌC VIÊN", "Không enroll được học viên vào lớp TC-WEB93.",
     "pham.thi.d@example.com", "Phạm Thị D", Outcome.NOT_LOGIN),
]

TEST_TAG = "week5-login-bot-test"
