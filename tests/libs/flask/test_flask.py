from unittest import TestCase

from flask import Flask
from src.libs.eventbus import EventBusService
from src.libs.flask.main import create_flask_app
from src.libs.notifications import TestNotificationService
from src.libs.redis.database import TestNoSQLService
from src.libs.sqlalchemy.database import TestSQLService


class TestCreateFlaskApp(TestCase):
    def test_create_app(self):
        app = create_flask_app(
            sql_class=TestSQLService,
            nosql_class=TestNoSQLService,
            notification_class=TestNotificationService,
            eventbus_class=EventBusService,
        )

        self.assertIsInstance(app, Flask)
        self.assertIsInstance(app.sql, TestSQLService)
        self.assertIsInstance(app.nosql, TestNoSQLService)
        self.assertIsInstance(app.notification, TestNotificationService)
        self.assertIsInstance(app.eventbus, EventBusService)
