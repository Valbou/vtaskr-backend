import os

APP_NAME = "notifications"

DEFAULT_SMTP_HOST = os.getenv("DEFAULT_SMTP_HOST")
DEFAULT_SMTP_PORT = os.getenv("DEFAULT_SMTP_PORT")
DEFAULT_SMTP_USER = os.getenv("DEFAULT_SMTP_USER")
DEFAULT_SMTP_PASS = os.getenv("DEFAULT_SMTP_PASS")
DEFAULT_SMTP_SENDER = os.getenv("DEFAULT_SMTP_SENDER")
