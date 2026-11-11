import socket
import unittest

from login_bot.mock_services import start_server
from login_bot.services import HrClient, JsonHttpClient, LmsClient, ServiceError


def free_port_with_nothing_listening():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class MockServicesTest(unittest.TestCase):
    def setUp(self):
        self.server, self.state = start_server(port=0)
        base = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.hr = HrClient(JsonHttpClient(base + "/hr", timeout=2, retries=1))
        self.lms = LmsClient(JsonHttpClient(base + "/lms", timeout=2, retries=1))

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def test_hr_returns_employee_status(self):
        self.assertEqual(self.hr.get_employee("nguyen.van.a@example.com").status, "active")
        self.assertEqual(self.hr.get_employee("le.van.c@example.com").status, "terminated")

    def test_hr_lookup_ignores_email_case(self):
        self.assertIsNotNone(self.hr.get_employee("Nguyen.Van.A@Example.com"))

    def test_unknown_email_returns_none(self):
        self.assertIsNone(self.hr.get_employee("ai.do@example.com"))
        self.assertIsNone(self.lms.get_account("ai.do@example.com"))

    def test_reactivate_changes_account_status(self):
        email = "nguyen.van.a@example.com"
        self.assertEqual(self.lms.get_account(email).status, "deactivated")
        self.lms.reactivate(email)
        self.assertEqual(self.lms.get_account(email).status, "active")

    def test_password_reset_returns_link(self):
        self.assertIn("reset", self.lms.send_password_reset("tran.thi.b@example.com"))

    def test_reactivating_unknown_account_raises(self):
        with self.assertRaises(ServiceError):
            self.lms.reactivate("ai.do@example.com")


class RetryTest(unittest.TestCase):
    def test_unreachable_service_raises_after_retries(self):
        client = JsonHttpClient(f"http://127.0.0.1:{free_port_with_nothing_listening()}", timeout=1, retries=2, backoff=0)
        with self.assertRaises(ServiceError) as ctx:
            HrClient(client).get_employee("x@example.com")
        self.assertIn("2 lần thử", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
