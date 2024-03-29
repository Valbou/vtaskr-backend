from src.settings import LINK_TO_CHANGE_EMAIL, LINK_TO_CHANGE_PASSWORD
from src.users.hmi.flask.emails import (
    ChangeEmailToNewEmail,
    ChangeEmailToOldEmail,
    ChangePasswordEmail,
    LoginEmail,
    RegisterEmail,
)
from tests.base_test import BaseTestCase, FlaskTemplateCapture


class TestRegisterEmail(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.to_emails = self.fake.email(domain="valbou.fr")
        self.first_name = self.fake.first_name()

    def test_email_object(self):
        with self.app.app_context():
            with FlaskTemplateCapture(self.app) as recorder:
                with self.app.trans.get_translation_session("users", "en") as trans:
                    email = RegisterEmail(
                        trans=trans,
                        to_emails=[self.to_emails],
                        first_name=self.first_name,
                    )
                self.assertTemplateUsed(
                    "emails/simple_text.html", recorder.get_recorded_templates()
                )
                self.assertIn(self.first_name, email.html)
                self.assertIn("data:image/svg+xml;base64,", email.html)
                self.assertIn(self.first_name, email.text)
                self.assertIn(self.to_emails, email.to_emails)


class TestLoginEmail(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.to_emails = self.fake.email(domain="valbou.fr")
        self.first_name = self.fake.first_name()
        self.code = self.fake.bothify("???###???###")

    def test_email_object(self):
        with self.app.app_context():
            with FlaskTemplateCapture(self.app) as recorder:
                with self.app.trans.get_translation_session("users", "en") as trans:
                    email = LoginEmail(
                        trans=trans,
                        to_emails=[self.to_emails],
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
                self.assertIn(self.to_emails, email.to_emails)


class TestChangeEmailOldEmail(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.to_emails = self.fake.email(domain="valbou.fr")
        self.first_name = self.fake.first_name()
        self.code = self.fake.bothify("???###???###")

    def test_email_object(self):
        with self.app.app_context():
            with FlaskTemplateCapture(self.app) as recorder:
                with self.app.trans.get_translation_session("users", "en") as trans:
                    email = ChangeEmailToOldEmail(
                        trans=trans,
                        to_emails=[self.to_emails],
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
                self.assertIn(self.to_emails, email.to_emails)


class TestChangeEmailNewEmail(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.to_emails = self.fake.email(domain="valbou.fr")
        self.first_name = self.fake.first_name()
        self.hash = self.fake.word()

    def test_email_object(self):
        with self.app.app_context():
            with FlaskTemplateCapture(self.app) as recorder:
                with self.app.trans.get_translation_session("users", "en") as trans:
                    email = ChangeEmailToNewEmail(
                        trans=trans,
                        to_emails=[self.to_emails],
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
                self.assertIn(self.to_emails, email.to_emails)
                self.assertIn(LINK_TO_CHANGE_EMAIL, email.text)
                self.assertIn(LINK_TO_CHANGE_EMAIL, email.html)


class TestChangePasswordEmail(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.to_emails = self.fake.email(domain="valbou.fr")
        self.first_name = self.fake.first_name()
        self.hash = self.fake.word()

    def test_email_object(self):
        with self.app.app_context():
            with FlaskTemplateCapture(self.app) as recorder:
                with self.app.trans.get_translation_session("users", "en") as trans:
                    email = ChangePasswordEmail(
                        trans=trans,
                        to_emails=[self.to_emails],
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
                self.assertIn(self.to_emails, email.to_emails)
                self.assertIn(LINK_TO_CHANGE_PASSWORD, email.text)
                self.assertIn(LINK_TO_CHANGE_PASSWORD, email.html)
