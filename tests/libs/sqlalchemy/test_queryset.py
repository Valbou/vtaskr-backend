from dataclasses import dataclass
from unittest import TestCase
from unittest.mock import MagicMock

from sqlalchemy import Column, Integer, String, Table

from src.libs.hmi.querystring import QueryStringFilter
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
        self.queryset.select()

    def assertInStatment(self, stmt: str, *args: str):
        for arg in args:
            with self.subTest(arg):
                self.assertIn(arg, stmt)

    def assertNotInStatment(self, stmt: str, *args: str):
        for arg in args:
            with self.subTest(arg):
                self.assertNotIn(arg, stmt)

    def test_options(self):
        self.queryset._query.options = MagicMock()
        tested = self.queryset._query.options
        result = self.queryset.options(test_name="test_value")

        tested.assert_called_once_with(test_name="test_value")
        self.assertIsInstance(result, Queryset)
        self.assertIs(result, self.queryset)

    def test_page(self):
        self.queryset.page(2)
        self.assertInStatment(
            str(self.queryset.statement), "SELECT", "FROM", "OFFSET", "LIMIT"
        )
        self.assertNotIn(str(self.queryset.statement), "WHERE")

    def test_order_by_asc(self):
        self.queryset.order_by(name="ASC")
        self.assertInStatment(
            str(self.queryset.statement), "ORDER BY test_user.name ASC"
        )

    def test_order_by_desc(self):
        self.queryset.order_by(age="DESC")
        self.assertInStatment(
            str(self.queryset.statement), "ORDER BY test_user.age DESC"
        )

    def test_limit(self):
        self.queryset.limit(42)
        self.assertInStatment(str(self.queryset.statement), "LIMIT")

    def test_filter_EQ(self):
        qsf = QueryStringFilter("name_eq=val")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(str(self.queryset.statement), "test_user.name = :name_1")

    def test_filter_NEQ(self):
        qsf = QueryStringFilter("name_neq=val")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(str(self.queryset.statement), "test_user.name != :name_1")

    def test_filter_LT(self):
        qsf = QueryStringFilter("age_lt=42")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(str(self.queryset.statement), "test_user.age < :age_1")

    def test_filter_LTE(self):
        qsf = QueryStringFilter("age_lte=42")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(str(self.queryset.statement), "test_user.age <= :age_1")

    def test_filter_GT(self):
        qsf = QueryStringFilter("age_gt=42")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(str(self.queryset.statement), "test_user.age > :age_1")

    def test_filter_GTE(self):
        qsf = QueryStringFilter("age_gte=42")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(str(self.queryset.statement), "test_user.age >= :age_1")

    def test_filter_CONTAINS(self):
        qsf = QueryStringFilter("name_contains=val")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(
            str(self.queryset.statement), "test_user.name LIKE '%' || :name_1 || '%'"
        )

    def test_filter_NCONTAINS(self):
        qsf = QueryStringFilter("name_ncontains=val")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(
            str(self.queryset.statement), "test_user.name NOT LIKE '%' || :name_1 || '%'"
        )

    def test_filter_STARTSWITH(self):
        qsf = QueryStringFilter("name_startswith=val")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(
            str(self.queryset.statement), "test_user.name LIKE :name_1 || '%'"
        )

    def test_filter_NSTARTSWITH(self):
        qsf = QueryStringFilter("name_nstartswith=val")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(
            str(self.queryset.statement), "test_user.name NOT LIKE :name_1 || '%'"
        )

    def test_filter_ENDSWITH(self):
        qsf = QueryStringFilter("name_endswith=val")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(
            str(self.queryset.statement), "test_user.name LIKE '%' || :name_1"
        )

    def test_filter_NENDSWITH(self):
        qsf = QueryStringFilter("name_nendswith=val")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(
            str(self.queryset.statement), "test_user.name NOT LIKE '%' || :name_1"
        )

    def test_filter_IN(self):
        qsf = QueryStringFilter("name_in=val")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(str(self.queryset.statement), "test_user.name IN")

    def test_filter_NIN(self):
        qsf = QueryStringFilter("name_nin=val")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(str(self.queryset.statement), "test_user.name NOT IN")

    def test_filter_ISNULL(self):
        qsf = QueryStringFilter("name_isnull=t")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(str(self.queryset.statement), "test_user.name IS NULL")

    def test_filter_not_ISNULL(self):
        qsf = QueryStringFilter("name_isnull=0")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(str(self.queryset.statement), "test_user.name IS NOT NULL")

    def test_filter_order_by_asc(self):
        qsf = QueryStringFilter("orderby=name")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(
            str(self.queryset.statement), "ORDER BY test_user.name ASC"
        )

    def test_filter_order_by_desc(self):
        qsf = QueryStringFilter("orderby=-name")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(
            str(self.queryset.statement), "ORDER BY test_user.name DESC"
        )

    def test_filter_limit(self):
        qsf = QueryStringFilter("limit=42")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(str(self.queryset.statement), "LIMIT :param_1")

    def test_filter_offset(self):
        qsf = QueryStringFilter("offset=42")
        self.queryset.from_filters(qsf.get_filters())
        self.assertInStatment(
            str(self.queryset.statement), "LIMIT :param_1 OFFSET :param_2"
        )

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
