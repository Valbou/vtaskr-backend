from unittest import TestCase

from flask import Flask
from src.libs.dependencies import DependencyInjector
from src.libs.flask.main import create_flask_app


class TestCreateFlaskApp(TestCase):
    def test_create_app(self):
        di = DependencyInjector()

        app = create_flask_app(dependencies=di)

        self.assertIsInstance(app, Flask)
        self.assertIsInstance(app.dependencies, DependencyInjector)
