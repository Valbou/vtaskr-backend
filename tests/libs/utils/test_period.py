from datetime import date, datetime, timedelta
from unittest import TestCase
from zoneinfo import ZoneInfo

from src.libs.utils import Period, Periodicity, PeriodTypes


class TestPeriod(TestCase):
    def setUp(self):
        super().setUp()

        self.cet = ZoneInfo("Europe/Paris")
        self.utc = ZoneInfo("UTC")

    def _get_instance(self, type: PeriodTypes) -> Period:
        if type is PeriodTypes.DATETIME:
            start = datetime.now(tz=self.cet)
            end = start + timedelta(days=365)

        elif type is PeriodTypes.NAIVE:
            start = datetime.now()
            end = start + timedelta(days=365)

        elif type is PeriodTypes.DATE:
            start = date.today()
            end = start + timedelta(days=365)

        else:
            NotImplementedError(f"Not implemented for {type}")

        return Period(start=start, end=end)

    def test_init_date(self):
        today = date.today()
        tomorrow = today + timedelta(days=1)
        period = Period(start=today, end=tomorrow)

        self.assertIsInstance(period, Period)
        self.assertIs(period.type, PeriodTypes.DATE)

    def test_init_str_date(self):
        today = date.today()
        tomorrow = today + timedelta(days=1)
        period = Period(start=today.isoformat(), end=tomorrow.isoformat())

        self.assertIsInstance(period, Period)
        self.assertIs(period.type, PeriodTypes.DATE)

    def test_init_datetime(self):
        now = datetime.now(tz=self.cet)
        next_week = now + timedelta(days=7)
        period = Period(start=now, end=next_week)

        self.assertIsInstance(period, Period)
        self.assertIs(period.type, PeriodTypes.DATETIME)

    def test_init_str_datetime(self):
        now = datetime.now(tz=self.cet)
        next_week = now + timedelta(days=7)
        period = Period(start=now.isoformat(), end=next_week.isoformat())

        self.assertIsInstance(period, Period)
        self.assertIs(period.type, PeriodTypes.DATETIME)

    def test_init_naive_datetime(self):
        now = datetime.now()
        next_week = now + timedelta(days=7)
        period = Period(start=now, end=next_week)

        self.assertIsInstance(period, Period)
        self.assertIs(period.type, PeriodTypes.NAIVE)

    def test_init_str_naive_datetime(self):
        now = datetime.now()
        next_week = now + timedelta(days=7)
        period = Period(start=now.isoformat(), end=next_week.isoformat())

        self.assertIsInstance(period, Period)
        self.assertIs(period.type, PeriodTypes.NAIVE)

    def test_fail_init(self):
        now = datetime.now()
        next_week = now + timedelta(days=7)

        with self.assertRaises(ValueError):
            Period(start=now, end=next_week, type="test")

    def test_fail_init_different_types(self):
        now = datetime.now()
        next_week = date.today() + timedelta(days=7)

        with self.assertRaises(ValueError):
            Period(start=now, end=next_week)

    def test_fail_init_end_before_start(self):
        now = datetime.now()
        prev_week = now - timedelta(days=7)

        with self.assertRaises(ValueError):
            Period(start=now, end=prev_week)

    def test_to_date_obj_from_str(self):
        period = self._get_instance(type=PeriodTypes.DATETIME)

        value = "2025-06-01T01:22:57.123650+02:00"
        result = period._to_date_obj(value=value)

        self.assertIsInstance(result, datetime)
        self.assertIsNotNone(result.tzinfo)
        self.assertEqual(result.isoformat(), value)

    def test_to_date_obj_from_datetime(self):
        period = self._get_instance(type=PeriodTypes.DATETIME)

        result = period._to_date_obj(value=period.start)

        self.assertIsInstance(result, datetime)
        self.assertEqual(result, period.start)
        self.assertNotEqual(result, period.end)

    def test_check_type_datetime(self):
        period = self._get_instance(type=PeriodTypes.DATETIME)
        self.assertIs(period.type, PeriodTypes.DATETIME)

    def test_check_type_date(self):
        period = self._get_instance(type=PeriodTypes.DATE)
        self.assertIs(period.type, PeriodTypes.DATE)

    def test_check_type_naive_datetime(self):
        period = self._get_instance(type=PeriodTypes.NAIVE)
        self.assertIs(period.type, PeriodTypes.NAIVE)

    def test_check_consistency(self):
        period = self._get_instance(type=PeriodTypes.DATE)
        self.assertIsNone(period._check_consistency())

    def test_check_consistency_same_start_end(self):
        period = self._get_instance(type=PeriodTypes.NAIVE)
        new_period = Period(start=period.start, end=period.start)

        self.assertIsInstance(new_period, Period)
        self.assertTrue(new_period.__bool__())

    def test_check_consistency_fail(self):
        period = self._get_instance(type=PeriodTypes.DATE)
        with self.assertRaises(ValueError):
            Period(start=period.end, end=period.start)

    def test_repr(self):
        start = date(year=2025, month=1, day=1)
        end = date(year=2026, month=1, day=1)
        period = Period(start=start, end=end)

        self.assertEqual(
            repr(period),
            (
                "Period(start=datetime.date(2025, 1, 1), "
                "end=datetime.date(2026, 1, 1))"
            ),
        )

    def test_str(self):
        start = date(year=2025, month=1, day=1)
        end = date(year=2026, month=1, day=1)
        period = Period(start=start, end=end)

        self.assertEqual(str(period), "2025-01-01 - 2026-01-01")

    def test_contain(self):
        start = date(year=2025, month=1, day=1)
        end = date(year=2026, month=1, day=1)
        period = Period(start=start, end=end)

        self.assertTrue(period.contain(value=date(year=2025, month=1, day=1)))
        self.assertTrue(period.contain(value=date(year=2025, month=6, day=25)))
        self.assertFalse(period.contain(value=date(year=2026, month=6, day=25)))
        self.assertFalse(period.contain(value=date(year=2026, month=1, day=1)))

    def test_split_at(self):
        period = self._get_instance(PeriodTypes.DATETIME)
        middle = period.start + timedelta(
            seconds=period.to_timedelta().total_seconds() // 2
        )

        before, after = period.split_at(value=middle)

        self.assertIsInstance(before, Period)
        self.assertIsInstance(after, Period)
        self.assertEqual(before.end, after.start)
        self.assertIs(before.type, period.type)
        self.assertIs(after.type, period.type)
        self.assertEqual(before.start, period.start)
        self.assertEqual(after.end, period.end)

        self.assertTrue(before.is_joined(after))
        self.assertTrue(after.is_joined(before))

    def to_timedelta(self):
        period = self._get_instance(type=PeriodTypes.DATETIME)
        delta = period.to_timedelta()

        self.assertIsInstance(delta, timedelta)

    def test_next_period(self):
        period = self._get_instance(PeriodTypes.DATETIME)
        next = period.next_period()

        self.assertIsInstance(next, Period)
        self.assertEqual(
            period.to_timedelta().total_seconds(), next.to_timedelta().total_seconds()
        )
        self.assertTrue(period.is_joined(next))
        self.assertGreater(next.start, period.start)

    def test_prev_period(self):
        period = self._get_instance(PeriodTypes.DATETIME)
        prev = period.prev_period()

        self.assertIsInstance(prev, Period)
        self.assertEqual(
            period.to_timedelta().total_seconds(), prev.to_timedelta().total_seconds()
        )
        self.assertTrue(period.is_joined(prev))
        self.assertLess(prev.start, period.start)

    def test_is_instant_true(self):
        now = datetime.now()
        period = Period(start=now, end=now)
        self.assertTrue(period.is_instant())

    def test_is_instant_false(self):
        period = self._get_instance(PeriodTypes.NAIVE)
        self.assertFalse(period.is_instant())
