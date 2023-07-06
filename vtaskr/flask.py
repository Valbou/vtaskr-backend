from flask import Flask

from vtaskr.libs.notifications import NotificationService
from vtaskr.libs.redis.database import NoSQLService
from vtaskr.libs.sqlalchemy.database import SQLService

from .libs.flask.main import create_flask_app

app: Flask = create_flask_app(
    sql_class=SQLService,
    nosql_class=NoSQLService,
    notification_class=NotificationService,
)
