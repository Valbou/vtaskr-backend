from unittest import TestCase

from babel import Locale
from faker import Faker

from flask import Flask, template_rendered
from src.settings import LOCALE, TIMEZONE
from src.users.hmi.dto import UserDTO
from src.users.services import UserService
from tests.utils.db_utils import text_query_column_exists, text_query_table_exists

from . import APP, DUMMY_APP


class FlaskTemplateCapture:
    def __init__(self, app: Flask) -> None:
        self.recorded_templates: list[str] = []
        self.app = app

    def __enter__(self):
        template_rendered.connect(self.add, self.app)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        template_rendered.disconnect(self.add, self.app)

    def add(self, sender, template, context, **extra):
        self.recorded_templates.append(template.name or "string template")

    def get_recorded_templates(self):
        return self.recorded_templates


class MixinTestCase:
    def generate_email(self):
        return self.fake.bothify("???###?#-").lower() + self.fake.email(
            domain="valbou.fr"
        )

    def generate_password(self):
        return self.fake.password(
            length=10, special_chars=True, digits=True, upper_case=True, lower_case=True
        )


class DummyBaseTestCase(MixinTestCase, TestCase):
    app: Flask = DUMMY_APP

    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()


class BaseTestCase(MixinTestCase, TestCase):
    app: Flask = APP

    def setUp(self) -> None:
        super().setUp()

        self.fake = Faker()
        self.client = self.app.test_client()
        self.cli = self.app.test_cli_runner()

    def assertTemplateUsed(self, template_name: str, recorded_templates: list[str]):
        self.assertIn(template_name, recorded_templates)

    def assertTableExists(self, table_name: str):
        params = {"table": table_name}
        stmt = text_query_table_exists()
        with self.app.dependencies.persistence.get_session() as session:
            result = session.execute(stmt, params=params).scalar_one_or_none()
            self.assertTrue(result, f"Table {table_name} doesn't exists")

    def assertColumnsExists(self, table_name: str, columns_name: list[str]):
        with self.app.dependencies.persistence.get_session() as session:
            for column_name in columns_name:
                params = {
                    "table": table_name,
                    "column": column_name,
                }
                stmt = text_query_column_exists()
                result = session.execute(stmt, params=params).scalar_one_or_none()
                self.assertTrue(
                    result, f"Column {column_name} doesn't exists in {table_name} Table"
                )

    def create_user(self):
        """Create a default test user and his group, role etc..."""
        self.password = self.generate_password()

        self.user_dto = UserDTO(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            locale=Locale.parse(LOCALE),
            timezone=TIMEZONE,
        )

        user_service = UserService(services=self.app.dependencies)
        self.user, self.group = user_service.register(
            self.user_dto, password=self.password
        )

    def get_json_headers(self):
        return {"Content-Type": "application/json"}

    def get_token_headers(self, valid: bool = True) -> dict:
        self.create_user()

        auth_service = UserService(services=self.app.dependencies)
        self.token, _ = auth_service.authenticate(
            email=self.user.email, password=self.password
        )

        if valid:
            auth_service.get_temp_token(
                sha_token=self.token.sha_token, code=self.token.temp_code
            )

        sha_token = self.token.sha_token
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {sha_token}",
        }
        return headers
