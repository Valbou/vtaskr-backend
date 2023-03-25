from unittest import TestCase

from vtasks.flask.main import create_flask_app


class FlaskTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._define_client()

    def _define_client(self):
        app = create_flask_app(testing=True)
        self.client = app.test_client()
        self.cli = app.test_cli_runner()
