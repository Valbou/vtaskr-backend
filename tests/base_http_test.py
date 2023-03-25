from unittest import TestCase

from vtasks.flask.main import app


class FlaskTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()

    def _define_client(self):
        app.testing = True  # handle client exception
        self.client = app.test_client()
