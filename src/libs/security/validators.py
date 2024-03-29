from gettext import gettext as _
from string import ascii_lowercase, ascii_uppercase, digits, punctuation

from email_validator import validate_email

from src.settings import PASSWORD_MIN_LENGTH


def get_valid_email(email: str) -> str | None:
    validation = validate_email(email, check_deliverability=True)
    return validation.email


class PasswordComplexityError(Exception):
    pass


class PasswordChecker:
    errors: list[str] = []

    def check_complexity(self, password: str) -> bool:
        self.errors = []
        result = all(
            [
                self._check_length(password),
                self._search_lowercase_letter(password),
                self._search_uppercase_letter(password),
                self._search_number(password),
                self._search_special_char(password),
            ]
        )
        if not result and len(self.errors):
            raise PasswordComplexityError(" ".join(self.errors))
        else:
            return True

    def _check_length(self, password: str) -> bool:
        if len(password) >= PASSWORD_MIN_LENGTH:
            return True
        self.errors.append(
            _(f"At least {PASSWORD_MIN_LENGTH} characters are required.")
        )
        return False

    def _search_lowercase_letter(self, password: str) -> bool:
        for letter in password:
            if letter in ascii_lowercase:
                return True
        self.errors.append(_("At least one lower case letter is required."))
        return False

    def _search_uppercase_letter(self, password: str) -> bool:
        for letter in password:
            if letter in ascii_uppercase:
                return True
        self.errors.append(_("At least one upper case letter is required."))
        return False

    def _search_number(self, password: str) -> bool:
        for letter in password:
            if letter in digits:
                return True
        self.errors.append(_("At least one number is required."))
        return False

    def _search_special_char(self, password: str) -> bool:
        for letter in password:
            if letter in punctuation + " ":
                return True
        self.errors.append(_("At least one special character is required."))
        return False
