from unittest import TestCase

from flask import Flask

from vtaskr.libs.flask.main import create_flask_app
from vtaskr.libs.redis.database import NoSQLService
from vtaskr.libs.sqlalchemy.database import SQLService


class TestCreateFlaskApp(TestCase):
    def test_create_app(self):
        app = create_flask_app(testing=True)
        self.assertIsInstance(app, Flask)
        self.assertIsInstance(app.sql, SQLService)
        self.assertIsInstance(app.nosql, NoSQLService)
