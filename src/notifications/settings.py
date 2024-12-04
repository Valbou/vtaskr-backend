import os
from enum import Enum

APP_NAME = "notifications"

DEFAULT_SMTP_HOST = os.getenv("DEFAULT_SMTP_HOST")
DEFAULT_SMTP_PORT = os.getenv("DEFAULT_SMTP_PORT")
DEFAULT_SMTP_USER = os.getenv("DEFAULT_SMTP_USER")
DEFAULT_SMTP_PASS = os.getenv("DEFAULT_SMTP_PASS")
DEFAULT_SMTP_SENDER = os.getenv("DEFAULT_SMTP_SENDER")

LINK_TO_LOGIN = os.getenv("NOTIFICATIONS_LINK_TO_LOGIN")
LINK_TO_CHANGE_EMAIL = os.getenv("NOTIFICATIONS_LINK_TO_CHANGE_EMAIL")
LINK_TO_CHANGE_PASSWORD = os.getenv("NOTIFICATIONS_LINK_TO_CHANGE_PASSWORD")
LINK_TO_JOIN_GROUP = os.getenv("NOTIFICATIONS_LINK_TO_JOIN_GROUP")

BASE_NOTIFICATION_EVENTS = [
    "users:register:user",
    "users:login_2fa:user",
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
