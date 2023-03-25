from email_validator import validate_email


def get_valid_email(email: str) -> str:
    validation = validate_email(email, check_deliverability=True)
    return validation.email
