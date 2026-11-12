"""Nội dung ghi chú nội bộ và email trả lời (dựa trên template Scenario 1 – Week 4)."""

from .models import Outcome

LABELS = {
    Outcome.REACTIVATED: "ĐÃ MỞ LẠI TÀI KHOẢN",
    Outcome.PASSWORD_RESET: "ĐÃ GỬI LINK ĐẶT LẠI MẬT KHẨU",
    Outcome.TERMINATED: "NHÂN SỰ ĐÃ NGHỈ VIỆC - CẦN NGƯỜI XEM LẠI",
    Outcome.ESCALATED: "CHUYỂN NGƯỜI XỬ LÝ",
    Outcome.FAILED: "AUTOMATION LỖI - CẦN XỬ LÝ TAY",
}

SIGNATURE = "Trân trọng,\nMindX Support Team"


def note(outcome, now, lines, next_step):
    body = [f"[LOGIN-BOT] {now:%Y-%m-%d %H:%M} - {LABELS[outcome]}"]
    body += [f"- {line}" for line in lines]
    body.append(f"- Bước tiếp theo: {next_step}")
    return "\n".join(body)


def subject(ticket):
    return f"RE: {ticket.subject} - Ticket #{ticket.id}"


def greeting(name):
    return f"Chào {name}," if name else "Chào bạn,"


def email_reactivated(name, ticket_id):
    return "\n".join([
        greeting(name), "",
        "Team đã kiểm tra và thấy tài khoản LMS của bạn bị tạm khóa do không đăng nhập trong 30 ngày.",
        "Sau khi xác nhận thông tin nhân sự, team đã mở lại tài khoản và gửi link đặt lại mật khẩu vào email này.",
        "",
        "Bạn vui lòng:",
        "1. Mở email đặt lại mật khẩu từ LMS và tạo mật khẩu mới.",
        "2. Đăng nhập tại lms.mindx.edu.vn.",
        "3. Trả lời email này để xác nhận đã đăng nhập được, team sẽ đóng ticket.",
        "",
        "Nếu vẫn chưa đăng nhập được, bạn trả lời email này, team sẽ hỗ trợ trực tiếp trong vòng 30 phút.",
        "", SIGNATURE, f"Ticket #{ticket_id}",
    ])


def email_password_reset(name, ticket_id):
    return "\n".join([
        greeting(name), "",
        "Team đã kiểm tra: tài khoản LMS của bạn đang hoạt động bình thường.",
        "Team đã gửi link đặt lại mật khẩu vào email này để bạn tạo mật khẩu mới.",
        "",
        "Bạn vui lòng:",
        "1. Mở email đặt lại mật khẩu từ LMS và tạo mật khẩu mới.",
        "2. Đăng nhập tại lms.mindx.edu.vn (nên thử thêm chế độ ẩn danh nếu trình duyệt lưu mật khẩu cũ).",
        "3. Trả lời email này để xác nhận đã đăng nhập được, team sẽ đóng ticket.",
        "", SIGNATURE, f"Ticket #{ticket_id}",
    ])


def email_acknowledged(name, ticket_id):
    """Dùng cho mọi ca chuyển người xử lý: không nêu lý do nội bộ (VD trạng thái HR)."""
    return "\n".join([
        greeting(name), "",
        "Cảm ơn bạn đã liên hệ. Team đã ghi nhận vấn đề đăng nhập của bạn.",
        "Kỹ thuật viên sẽ kiểm tra và phản hồi bạn trong vòng 30 phút (giờ làm việc).",
        "",
        "Trong lúc chờ, bạn vui lòng thử:",
        "- Đăng nhập bằng chế độ ẩn danh (Incognito).",
        "- Kiểm tra đúng địa chỉ đăng nhập của hệ thống.",
        "", SIGNATURE, f"Ticket #{ticket_id}",
    ])
