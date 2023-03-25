from unittest import TestCase
from typing import List

from faker import Faker
from flask import Flask, template_rendered

from vtasks.flask.main import create_flask_app
from vtasks.sqlalchemy.database import SQLService


class FlaskTemplateCapture:
    def __init__(self, app: Flask) -> None:
        self.recorded_templates: List[str] = []
        self.app = app

    def __enter__(self):
        template_rendered.connect(self.add, self.app)

    def __exit__(self, exc_type, exc_value, traceback):
        template_rendered.disconnect(self.add, self.app)

    def add(self, sender, template, context, **extra):
        self.recorded_templates.append(template.name or "string template")

    def get_recorded_templates(self):
        return self.recorded_templates


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.fake = Faker()
        self.app: Flask = create_flask_app(testing=True)
        self.client = self.app.test_client()
        self.cli = self.app.test_cli_runner()
        self.app.sql_service = SQLService(testing=True, echo=False)

    def assertTemplateUsed(self, template_name: str, recorded_templates: List[str]):
        self.assertIn(template_name, recorded_templates)
