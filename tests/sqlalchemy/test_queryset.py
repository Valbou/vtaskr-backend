from typing import Optional
from unittest import TestCase

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from vtaskr.sqlalchemy.queryset import Queryset
from vtaskr.sqlalchemy.querystring import QueryStringFilter


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    fullname: Mapped[Optional[str]]


class TestQueryset(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.queryset = Queryset(User)

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
            str(self.queryset.query), "SELECT", "FROM", "OFFSET", "LIMIT"
        )
        self.assertNotIn(str(self.queryset.query), "WHERE")

    def test_from_filters(self):
        qsf = QueryStringFilter("name_in=val,bou&orderby=-name&age_gte=18&page=2")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(
            str(self.queryset.query),
            "SELECT",
            "FROM",
            "WHERE",
            "IN",
            "ORDER BY",
            "OFFSET",
            "LIMIT",
        )
