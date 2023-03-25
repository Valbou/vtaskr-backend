from tests import BaseTestCase, FlaskTemplateCapture

from vtasks.users.hmi.flask.email_content import RegisterEmail


class TestRegisterEmail(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.to = self.fake.email(domain="valbou.fr")
        self.first_name = self.fake.first_name()
        self.last_name = self.fake.last_name()

    def test_email_object(self):
        with self.app.app_context():
            recorder = FlaskTemplateCapture(self.app)
            with recorder:
                email = RegisterEmail(
                    to=[self.to],
                    first_name=self.first_name,
                    last_name=self.last_name,
                )
                self.assertTemplateUsed(
                    "emails/simple_text.html", recorder.get_recorded_templates()
                )
                self.assertIn(self.first_name, email.html)
                self.assertIn("data:image/svg+xml;base64,", email.html)
                self.assertIn(self.first_name, email.text)
                self.assertIn(self.to, email.to_emails)
