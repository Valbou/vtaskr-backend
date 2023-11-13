from unittest import TestCase

from email_validator import EmailSyntaxError

from src.libs.security.validators import (
    PasswordChecker,
    PasswordComplexityError,
    get_valid_email,
)


class TestEmailValidator(TestCase):
    def test_valid_emails(self):
        emails = [
            "test@test.com",
            "test+test@test.com",
        ]
        for email in emails:
            with self.subTest(email):
                result = get_valid_email(email)
                self.assertEqual(result, email)

    def test_invalid_emails(self):
        emails = [
            "test@test",
            "test+test.com",
        ]
        for email in emails:
            with self.subTest(email):
                with self.assertRaises(EmailSyntaxError):
                    get_valid_email(email)


class TestPasswordChecker(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.pwdchk = PasswordChecker()

    def test_valid_password(self):
        passwords = [
            "Ab1#Ab1#Ab1#",
            "test+t3st@test.Com",
        ]  # nosec
        for pwd in passwords:
            with self.subTest(pwd):
                self.pwdchk.check_complexity(pwd)

    def test_invalid_password_length(self):
        pwd = "Ab1#"  # nosec
        with self.assertRaises(PasswordComplexityError):
            self.pwdchk.check_complexity(pwd)

    def test_invalid_password_no_lower_case(self):
        pwd = "AB1#AB1#AB1#"  # nosec
        with self.assertRaises(PasswordComplexityError):
            self.pwdchk.check_complexity(pwd)

    def test_invalid_password_no_upper_case(self):
        pwd = "ab1#ab1#ab1#"  # nosec
        with self.assertRaises(PasswordComplexityError):
            self.pwdchk.check_complexity(pwd)

    def test_invalid_password_no_number(self):
        pwd = "abl#abl#abl#"  # nosec
        with self.assertRaises(PasswordComplexityError):
            self.pwdchk.check_complexity(pwd)

    def test_invalid_password_no_special_char(self):
        pwd = "Ab1xAb1xAb1x"  # nosec
        with self.assertRaises(PasswordComplexityError):
            self.pwdchk.check_complexity(pwd)
