from unittest import TestCase

from flask import Flask

from vtasks.flask.main import create_flask_app


class TestCreateFlaskApp(TestCase):
    def test_create_app(self):
        app = create_flask_app(testing=True)
        self.assertIsInstance(app, Flask)
