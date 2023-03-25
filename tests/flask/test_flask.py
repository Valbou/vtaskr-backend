from unittest import TestCase

from flask import Flask

from vtasks.sqlalchemy.database import SQLService
from vtasks.redis.database import NoSQLService
from vtasks.flask.main import create_flask_app


class TestCreateFlaskApp(TestCase):
    def test_create_app(self):
        app = create_flask_app(testing=True)
        self.assertIsInstance(app, Flask)
        self.assertIsInstance(app.sql, SQLService)
        self.assertIsInstance(app.nosql, NoSQLService)
