import unittest

from login_bot.classifier import classify, normalize


class NormalizeTest(unittest.TestCase):
    def test_removes_vietnamese_accents_and_lowercases(self):
        self.assertEqual(normalize("KHÔNG ĐĂNG NHẬP được"), "khong dang nhap duoc")


class ClassifyTest(unittest.TestCase):
    def test_scenario_1_email_is_an_lms_login_issue(self):
        c = classify("Không thể đăng nhập vào LMS", 'bị lỗi "Invalid username or password"')
        self.assertTrue(c.is_login)
        self.assertEqual(c.system, "lms")
        self.assertTrue(c.in_scope)

    def test_english_ticket_is_detected(self):
        self.assertTrue(classify("Cannot log in", "my account is locked").is_login)

    def test_real_subjects_from_sample_are_login_issues(self):
        for subject in ["LỖI ĐĂNG NHẬP HỆ THỐNG NỘI BỘ", "Tài khoản E Count bị khoá",
                        "Nhờ hỗ trợ cấp lại mật khẩu LMS cho giáo viên Đinh Ngọc Tài",
                        "KHÔNG TRUY CẬP VÔ TMS ĐƯỢC", "Re: Không đăng nhập được CRM"]:
            with self.subTest(subject=subject):
                self.assertTrue(classify(subject).is_login)

    def test_system_without_name_is_in_scope(self):
        c = classify("LỖI ĐĂNG NHẬP HỆ THỐNG NỘI BỘ")
        self.assertIsNone(c.system)
        self.assertTrue(c.in_scope)

    def test_other_systems_are_out_of_scope(self):
        cases = {"BU KHÔNG ĐĂNG NHẬP VÀO TMS ĐƯỢC": "tms", "Re: Không đăng nhập được CRM": "crm",
                 "Tài khoản E Count bị khoá": "ecount", "BU QUÊN MẬT KHẨU EMAIL TMS": "tms"}
        for subject, system in cases.items():
            with self.subTest(subject=subject):
                c = classify(subject)
                self.assertEqual(c.system, system)
                self.assertFalse(c.in_scope)

    def test_subject_system_wins_over_description(self):
        self.assertEqual(classify("Không đăng nhập được LMS", "trước đó em vẫn dùng CRM bình thường").system, "lms")

    def test_student_accounts_are_out_of_scope(self):
        c = classify("PNL HỖ TRỢ TÀI KHOẢN DENISE - HV không đăng nhập được")
        self.assertTrue(c.is_login)
        self.assertTrue(c.is_student)
        self.assertFalse(c.in_scope)

    def test_non_login_tickets_from_sample_are_ignored(self):
        for subject in ["KHÔNG THỂ ENROLL HỌC VIÊN", "TMS không hiển thị công", "CẤP TÀI KHOẢN NHÂN SỰ I4137",
                        "Lỗi Add payment", "BU PXL I KHÔNG TẠO ĐƯỢC PHIẾU DROPOUT"]:
            with self.subTest(subject=subject):
                self.assertFalse(classify(subject).is_login)


if __name__ == "__main__":
    unittest.main()
