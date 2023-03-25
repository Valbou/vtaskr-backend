from unittest import TestCase
from typing import List

from faker import Faker
from flask import Flask, template_rendered

from tests.utils.db_utils import (
    text_query_table_exists,
    text_query_column_exists,
)

from vtasks.flask.main import create_flask_app
from vtasks.sqlalchemy.database import SQLService
from vtasks.users import User
from vtasks.users.persistence import UserDB
from vtasks.users.hmi.flask.user_service import UserService


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

    def assertTableExists(self, table_name: str):
        params = {"table": table_name}
        stmt = text_query_table_exists()
        with self.app.sql_service.get_session() as session:
            result = session.execute(stmt, params=params).scalar_one_or_none()
            self.assertTrue(result, f"Table {table_name} doesn't exists")

    def assertColumnsExists(self, table_name: str, columns_name: List[str]):
        with self.app.sql_service.get_session() as session:
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
        self.password = self.fake.password()
        self.user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.fake.email(domain="valbou.fr"),
        )
        self.user.set_password(self.password)

        self.user_db = UserDB()
        with self.app.sql_service.get_session() as session:
            session.expire_on_commit = False
            self.user_db.save(session, self.user)

    def get_json_headers(self):
        return {"Content-Type": "application/json"}

    def get_token_headers(self) -> dict:
        self.create_user()
        with self.app.sql_service.get_session() as session:
            auth_service = UserService(session, testing=True)
            token = auth_service.authenticate(
                email=self.user.email, password=self.password
            )
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        return headers
