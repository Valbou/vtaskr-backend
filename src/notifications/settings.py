import os
from enum import Enum

APP_NAME = "notifications"

DEFAULT_SMTP_HOST = os.getenv("DEFAULT_SMTP_HOST")
DEFAULT_SMTP_PORT = os.getenv("DEFAULT_SMTP_PORT")
DEFAULT_SMTP_USER = os.getenv("DEFAULT_SMTP_USER")
DEFAULT_SMTP_PASS = os.getenv("DEFAULT_SMTP_PASS")
DEFAULT_SMTP_SENDER = os.getenv("DEFAULT_SMTP_SENDER")

BASE_NOTIFICATION_EVENTS = [
    "users:register:user",
    "users:login_2fa:user",
    "users:login:user",
    "users:delete:user",
    "users:change_email:user",
    "users:change_password:user",
    "users:invite:user",
    "users:invite_cancelled:user",
    "users:invite_accepted:user",
]


class MessageType(Enum):
    EMAIL = "email"
    SMS = "sms"
    TELEGRAM = "telegram"
