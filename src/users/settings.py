import os

APP_NAME = "users"

DEFAULT_SENDER = os.getenv("USERS_DEFAULT_SENDER")

LINK_TO_LOGIN = os.getenv("USERS_LINK_TO_LOGIN")
LINK_TO_CHANGE_EMAIL = os.getenv("USERS_LINK_TO_CHANGE_EMAIL")
LINK_TO_CHANGE_PASSWORD = os.getenv("USERS_LINK_TO_CHANGE_PASSWORD")
LINK_TO_JOIN_GROUP = os.getenv("USERS_LINK_TO_JOIN_GROUP")
