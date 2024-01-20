from flask import Flask
from src.libs.eventbus import EventBusService
from src.libs.notifications import NotificationService
from src.libs.redis.database import NoSQLService
from src.libs.sqlalchemy.database import SQLService

from .libs.flask.main import create_flask_app

app: Flask = create_flask_app(
    sql_class=SQLService,
    nosql_class=NoSQLService,
    notification_class=NotificationService,
    eventbus_class=EventBusService,
)
