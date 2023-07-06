from unittest import TestCase

from flask import Flask

from vtaskr.libs.flask.main import create_flask_app
from vtaskr.libs.notifications import TestNotificationService
from vtaskr.libs.redis.database import TestNoSQLService
from vtaskr.libs.sqlalchemy.database import TestSQLService


class TestCreateFlaskApp(TestCase):
    def test_create_app(self):
        app = create_flask_app(
            sql_class=TestSQLService,
            nosql_class=TestNoSQLService,
            notification_class=TestNotificationService,
        )

        self.assertIsInstance(app, Flask)
        self.assertIsInstance(app.sql, TestSQLService)
        self.assertIsInstance(app.nosql, TestNoSQLService)
        self.assertIsInstance(app.notification, TestNotificationService)
