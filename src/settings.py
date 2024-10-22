import os

from src.libs.security.utils import file_to_base64

APP_NAME = "vTaskr"
DESCRIPTION = "vTaskr is an open-source task manager"
VERSION = "0.1.0"
DOMAIN = "https://api.vtaskr.com"

SECRET_KEY = os.getenv("SECRET_KEY", "fake_YM/92:>Dhqv=7p8+ixY=By?4i(%TU5L;W+4=dboG=")

# Validators config
PASSWORD_MIN_LENGTH = 10
UNUSED_ACCOUNT_DELAY = 7  # 7 days

# Auth token validity
TOKEN_VALIDITY = 60 * 60 * 8  # 8 heures !
TOKEN_TEMP_VALIDITY = 60 * 3  # 3 minutes

# Validity of a request change (email or password)
REQUEST_VALIDITY = 60 * 5
REQUEST_DAYS_HISTORY = 90

# Validity of group invitation
INVITE_VALIDITY = 60 * 60 * 24 * 30  # almost 1 month

# i18n/l10n
AVAILABLE_LANGUAGES = {
    "fr": "Français",
    "en": "English",
}

INSTALLED_APPS = ["libs", "base", "users", "events", "notifications", "tasks"]

LOCALE = os.getenv("LOCALE", "en_GB")
TIMEZONE = os.getenv("TIMEZONE", "Europe/London")

# Emails config
EMAIL_LOGO = f"""data:image/svg+xml;base64,{
    file_to_base64("src/static/vtaskr-logo-light.svg")
}"""

TELEGRAM_BOT = os.getenv("TELEGRAM_BOT")
