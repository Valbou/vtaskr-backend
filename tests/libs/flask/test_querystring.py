from dataclasses import dataclass
from datetime import date, datetime
from unittest import TestCase

from src.libs.flask.querystring import Filter, Operations, QueryStringFilter


class QSTestMixin(TestCase):
    def assertFilter(self, filter, field, operation, value):
        self.assertIsInstance(filter, Filter)
        self.assertEqual(filter.field, field)
        self.assertEqual(filter.operation, operation)
        self.assertEqual(filter.value, value)


class TestQueryStringFilter(QSTestMixin):
    def test_order_by_asc_filter(self):
        qs = "orderby=name"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "name", Operations.ASC, "name")

    def test_order_by_desc_filter(self):
        qs = "orderby=-name"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "name", Operations.DESC, "-name")

    def test_order_by_multi_filter(self):
        qs = "orderby=-name,id"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 2)
        self.assertFilter(filters[0], "name", Operations.DESC, "-name")
        self.assertFilter(filters[1], "id", Operations.ASC, "id")

    def test_order_by_multi_filter_2(self):
        qs = "orderby=-name&orderby=id"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 2)
        self.assertFilter(filters[0], "name", Operations.DESC, "-name")
        self.assertFilter(filters[1], "id", Operations.ASC, "id")

    def test_offset(self):
        qs = "offset=42"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "offset", Operations.OFFSET, "42")

    def test_limit(self):
        qs = "limit=42"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "limit", Operations.LIMIT, "42")

    def test_page(self):
        qs = "page=5"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "page", Operations.PAGE, "5")

    def test_offset_and_limit(self):
        qs = "offset=42&limit=100"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 2)
        self.assertFilter(filters[0], "offset", Operations.OFFSET, "42")
        self.assertFilter(filters[1], "limit", Operations.LIMIT, "100")

    def test_offset_and_page(self):
        qs = "offset=42&page=5"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 2)
        self.assertFilter(filters[0], "offset", Operations.OFFSET, "42")
        self.assertFilter(filters[1], "page", Operations.PAGE, "5")

    def test_equal(self):
        qs = "name_eq=val"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "name", Operations.EQ, "val")

    def test_not_equal(self):
        qs = "name_neq=val"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "name", Operations.NEQ, "val")

    def test_lower_than(self):
        qs = "age_lt=42"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "age", Operations.LT, "42")

    def test_lower_than_equal(self):
        qs = "age_lte=42"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "age", Operations.LTE, "42")

    def test_greater_than(self):
        qs = "age_gt=18"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "age", Operations.GT, "18")

    def test_greater_than_equal(self):
        qs = "age_gte=18"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "age", Operations.GTE, "18")

    def test_in(self):
        qs = "age_in=18,19,20,21,22"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 5)
        self.assertFilter(filters[0], "age", Operations.IN, "18")
        self.assertFilter(filters[1], "age", Operations.IN, "19")
        self.assertFilter(filters[2], "age", Operations.IN, "20")
        self.assertFilter(filters[3], "age", Operations.IN, "21")
        self.assertFilter(filters[4], "age", Operations.IN, "22")

    def test_not_in(self):
        qs = "age_nin=18,19,20,21,22"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 5)
        self.assertFilter(filters[0], "age", Operations.NIN, "18")
        self.assertFilter(filters[1], "age", Operations.NIN, "19")
        self.assertFilter(filters[2], "age", Operations.NIN, "20")
        self.assertFilter(filters[3], "age", Operations.NIN, "21")
        self.assertFilter(filters[4], "age", Operations.NIN, "22")

    def test_contains(self):
        qs = "name_contains=val"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "name", Operations.CONTAINS, "val")

    def test_not_contains(self):
        qs = "name_ncontains=val"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "name", Operations.NCONTAINS, "val")

    def test_starts_with(self):
        qs = "name_startswith=val"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "name", Operations.STARTSWITH, "val")

    def test_not_starts_with(self):
        qs = "name_nstartswith=val"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "name", Operations.NSTARTSWITH, "val")

    def test_ends_with(self):
        qs = "name_endswith=val"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "name", Operations.ENDSWITH, "val")

    def test_not_ends_with(self):
        qs = "name_nendswith=val"
        qs_filter = QueryStringFilter(query_string=qs)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "name", Operations.NENDSWITH, "val")


@dataclass
class TestDTO:
    string: str = "foo"
    integer: int = 42
    floating: float = 0.0
    boolean: bool = False
    opt_str: str | None = None
    opt_int: int | None = None
    datation: datetime = datetime.now()
    opt_datation: date | None = date.today()


class TestQueryStringFilterLimited(QSTestMixin):
    def setUp(self) -> None:
        super().setUp()
        self.dto = TestDTO()

    def test_filter_on_dto_field(self):
        qs = "opt_int_eq=42"
        qs_filter = QueryStringFilter(query_string=qs, dto=self.dto)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(filters[0], "opt_int", Operations.EQ, 42)
        self.assertIsInstance(filters[0].value, int)

    def test_filter_out_of_dto_fields(self):
        qs = "name_eq=val"
        qs_filter = QueryStringFilter(query_string=qs, dto=self.dto)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 0)

    def test_cast_datetime_from_dto(self):
        qs = "datation_eq=2023-04-02T18:56:55.763324%2B00:00"
        qs_filter = QueryStringFilter(query_string=qs, dto=self.dto)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(
            filters[0],
            "datation",
            Operations.EQ,
            datetime.fromisoformat("2023-04-02T18:56:55.763324+00:00"),
        )
        self.assertIsInstance(filters[0].value, datetime)

    def test_cast_optional_date_from_dto(self):
        qs = "opt_datation_lt=2023-04-02"
        qs_filter = QueryStringFilter(query_string=qs, dto=self.dto)
        filters = qs_filter.get_filters()
        self.assertEqual(len(filters), 1)
        self.assertFilter(
            filters[0], "opt_datation", Operations.LT, date.fromisoformat("2023-04-02")
        )
        self.assertIsInstance(filters[0].value, date)
