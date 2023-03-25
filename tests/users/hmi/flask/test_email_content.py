from tests import BaseTestCase, FlaskTemplateCapture

from vtasks.base.config import LINK_TO_CHANGE_EMAIL, LINK_TO_CHANGE_PASSWORD
from vtasks.users.hmi.flask.email_content import (
    RegisterEmail,
    LoginEmail,
    ChangeEmailToOldEmail,
    ChangeEmailToNewEmail,
    ChangePasswordEmail,
)


class TestRegisterEmail(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.to = self.fake.email(domain="valbou.fr")
        self.first_name = self.fake.first_name()

    def test_email_object(self):
        with self.app.app_context():
            recorder = FlaskTemplateCapture(self.app)
            with recorder:
                email = RegisterEmail(
                    to=[self.to],
                    first_name=self.first_name,
                )
                self.assertTemplateUsed(
                    "emails/simple_text.html", recorder.get_recorded_templates()
                )
                self.assertIn(self.first_name, email.html)
                self.assertIn("data:image/svg+xml;base64,", email.html)
                self.assertIn(self.first_name, email.text)
                self.assertIn(self.to, email.to_emails)


class TestLoginEmail(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.to = self.fake.email(domain="valbou.fr")
        self.first_name = self.fake.first_name()
        self.code = self.fake.password()

    def test_email_object(self):
        with self.app.app_context():
            recorder = FlaskTemplateCapture(self.app)
            with recorder:
                email = LoginEmail(
                    to=[self.to],
                    first_name=self.first_name,
                    code=self.code,
                )
                self.assertTemplateUsed(
                    "emails/simple_text.html", recorder.get_recorded_templates()
                )
                self.assertIn(self.first_name, email.html)
                self.assertIn(self.code, email.html)
                self.assertIn("data:image/svg+xml;base64,", email.html)
                self.assertIn(self.first_name, email.text)
                self.assertIn(self.code, email.text)
                self.assertIn(self.to, email.to_emails)


class TestChangeEmailOldEmail(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.to = self.fake.email(domain="valbou.fr")
        self.first_name = self.fake.first_name()
        self.code = self.fake.password()

    def test_email_object(self):
        with self.app.app_context():
            recorder = FlaskTemplateCapture(self.app)
            with recorder:
                email = ChangeEmailToOldEmail(
                    to=[self.to],
                    first_name=self.first_name,
                    code=self.code,
                )
                self.assertTemplateUsed(
                    "emails/simple_text.html", recorder.get_recorded_templates()
                )
                self.assertIn(self.first_name, email.html)
                self.assertIn(self.code, email.html)
                self.assertIn("data:image/svg+xml;base64,", email.html)
                self.assertIn(self.first_name, email.text)
                self.assertIn(self.code, email.text)
                self.assertIn(self.to, email.to_emails)


class TestChangeEmailNewEmail(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.to = self.fake.email(domain="valbou.fr")
        self.first_name = self.fake.first_name()
        self.hash = self.fake.word()

    def test_email_object(self):
        with self.app.app_context():
            recorder = FlaskTemplateCapture(self.app)
            with recorder:
                email = ChangeEmailToNewEmail(
                    to=[self.to],
                    first_name=self.first_name,
                    hash=self.hash,
                )
                self.assertTemplateUsed(
                    "emails/simple_text.html", recorder.get_recorded_templates()
                )
                self.assertIn(self.first_name, email.html)
                self.assertIn(self.hash, email.html)
                self.assertIn("data:image/svg+xml;base64,", email.html)
                self.assertIn(self.first_name, email.text)
                self.assertIn(self.hash, email.text)
                self.assertIn(self.to, email.to_emails)
                self.assertIn(LINK_TO_CHANGE_EMAIL, email.text)
                self.assertIn(LINK_TO_CHANGE_EMAIL, email.html)


class TestChangePasswordEmail(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.to = self.fake.email(domain="valbou.fr")
        self.first_name = self.fake.first_name()
        self.hash = self.fake.word()

    def test_email_object(self):
        with self.app.app_context():
            recorder = FlaskTemplateCapture(self.app)
            with recorder:
                email = ChangePasswordEmail(
                    to=[self.to],
                    first_name=self.first_name,
                    hash=self.hash,
                )
                self.assertTemplateUsed(
                    "emails/simple_text.html", recorder.get_recorded_templates()
                )
                self.assertIn(self.first_name, email.html)
                self.assertIn(self.hash, email.html)
                self.assertIn("data:image/svg+xml;base64,", email.html)
                self.assertIn(self.first_name, email.text)
                self.assertIn(self.hash, email.text)
                self.assertIn(self.to, email.to_emails)
                self.assertIn(LINK_TO_CHANGE_PASSWORD, email.text)
                self.assertIn(LINK_TO_CHANGE_PASSWORD, email.html)
