from dataclasses import dataclass
from unittest import TestCase

from sqlalchemy import Column, Integer, String, Table

from src.libs.flask.querystring import QueryStringFilter
from src.libs.sqlalchemy.base import mapper_registry
from src.libs.sqlalchemy.queryset import Queryset


@dataclass
class TestUser:
    id: int
    name: str
    age: int
    fullname: str | None


test_table = Table(
    "test_user",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("name", String()),
    Column("age", Integer()),
    Column("fullname", String(), nullable=True, default=None),
)

mapper_registry.map_imperatively(
    TestUser,
    test_table,
)


class TestQueryset(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.queryset = Queryset(TestUser)

    def assertInStatment(self, stmt: str, *args: str):
        for arg in args:
            with self.subTest(arg):
                self.assertIn(arg, stmt)

    def assertNotInStatment(self, stmt: str, *args: str):
        for arg in args:
            with self.subTest(arg):
                self.assertNotIn(arg, stmt)

    def test_page(self):
        self.queryset.page(2)
        self.assertInStatment(
            str(self.queryset.statement), "SELECT", "FROM", "OFFSET", "LIMIT"
        )
        self.assertNotIn(str(self.queryset.statement), "WHERE")

    def test_from_filters(self):
        qsf = QueryStringFilter("name_in=val,bou&orderby=-name&age_gte=18&page=2")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(
            str(self.queryset.statement),
            "SELECT",
            "FROM",
            "WHERE",
            "IN",
            "ORDER BY",
            "OFFSET",
            "LIMIT",
        )
