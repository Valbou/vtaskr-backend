from unittest import TestCase
from typing import List

from flask import Flask, template_rendered

from vtasks.flask.main import create_flask_app


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


class FlaskTestCase(TestCase):
    defined_http_service: bool = False

    def setUp(self) -> None:
        super().setUp()
        self._define_client()

    def _define_client(self):
        self.app: Flask = create_flask_app(testing=True)
        self.client = self.app.test_client()
        self.cli = self.app.test_cli_runner()
        self.defined_http_service = True

    def assertTemplateUsed(self, template_name: str, recorded_templates: List[str]):
        self.assertIn(template_name, recorded_templates)
