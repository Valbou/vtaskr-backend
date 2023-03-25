from typing import List
from unittest import TestCase

from faker import Faker
from flask import Flask, template_rendered

from tests.utils.db_utils import text_query_column_exists, text_query_table_exists
from vtaskr.flask.main import create_flask_app
from vtaskr.sqlalchemy.database import SQLService
from vtaskr.users import User
from vtaskr.users.hmi.user_service import UserService
from vtaskr.users.persistence import UserDB


class FlaskTemplateCapture:
    def __init__(self, app: Flask) -> None:
        self.recorded_templates: List[str] = []
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


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.fake = Faker()
        self.app: Flask = create_flask_app(testing=True)
        self.client = self.app.test_client()
        self.cli = self.app.test_cli_runner()
        self.app.sql = SQLService(testing=True, echo=False)

    def assertTemplateUsed(self, template_name: str, recorded_templates: List[str]):
        self.assertIn(template_name, recorded_templates)

    def assertTableExists(self, table_name: str):
        params = {"table": table_name}
        stmt = text_query_table_exists()
        with self.app.sql.get_session() as session:
            result = session.execute(stmt, params=params).scalar_one_or_none()
            self.assertTrue(result, f"Table {table_name} doesn't exists")

    def assertColumnsExists(self, table_name: str, columns_name: List[str]):
        with self.app.sql.get_session() as session:
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
        self.password = self.fake.password() + "Aa1#"
        self.user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email="base." + self.fake.email(domain="valbou.fr"),
        )
        self.user.set_password(self.password)

        self.user_db = UserDB()
        with self.app.sql.get_session() as session:
            session.expire_on_commit = False
            self.user_db.save(session, self.user)

    def get_json_headers(self):
        return {"Content-Type": "application/json"}

    def get_token_headers(self, valid: bool = True) -> dict:
        self.create_user()
        with self.app.sql.get_session() as session:
            session.expire_on_commit = False
            auth_service = UserService(session, testing=True)
            self.token, _ = auth_service.authenticate(
                email=self.user.email, password=self.password
            )
            if valid:
                self.token.validate_token(self.token.temp_code)
            session.commit()
            sha_token = self.token.sha_token
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {sha_token}",
        }
        return headers
