from datetime import date, datetime, timedelta
from unittest import TestCase
from zoneinfo import ZoneInfo

from src.libs.utils import Period, Periodicity


class TestPeriodicity(TestCase):
    def setUp(self):
        super().setUp()

        self.cet = ZoneInfo("Europe/Paris")

    def test_str(self):
        self.assertEqual(str(Periodicity.MINUTE_1), "1 minute")
        self.assertEqual(str(Periodicity.DAY_1), "1 day")
        self.assertEqual(str(Periodicity.YEAR_1), "1 year")

    def test_str_plural(self):
        self.assertEqual(str(Periodicity.MINUTE_15), "15 minutes")
        self.assertEqual(str(Periodicity.HOUR_12), "12 hours")
        self.assertEqual(str(Periodicity.WEEK_2), "2 weeks")
        self.assertEqual(str(Periodicity.MONTH_3), "3 months")

    def test_timedelta_to_granularity(self):
        self.assertIs(
            Periodicity.WEEK_1,
            Periodicity.timedelta_to_granularity(delta=timedelta(days=7)),
        )
        self.assertIs(
            Periodicity.MINUTE_30,
            Periodicity.timedelta_to_granularity(delta=timedelta(minutes=30)),
        )
        self.assertIs(
            Periodicity.WEEK_4,
            Periodicity.timedelta_to_granularity(delta=timedelta(days=28)),
        )

    def test_timedelta_to_granularity_roughly(self):
        self.assertIs(
            Periodicity.DAY_1,
            Periodicity.timedelta_to_granularity(delta=timedelta(minutes=60 * 25)),
        )
        self.assertIs(
            Periodicity.MONTH_1,
            Periodicity.timedelta_to_granularity(delta=timedelta(days=30)),
        )
        self.assertIs(
            Periodicity.MONTH_1,
            Periodicity.timedelta_to_granularity(delta=timedelta(days=31)),
        )
        self.assertIs(
            Periodicity.MONTH_3,
            Periodicity.timedelta_to_granularity(delta=timedelta(days=89)),
        )
        self.assertIs(
            Periodicity.MONTH_3,
            Periodicity.timedelta_to_granularity(delta=timedelta(days=92)),
        )
        self.assertIs(
            Periodicity.MONTH_6,
            Periodicity.timedelta_to_granularity(delta=timedelta(days=180)),
        )
        self.assertIs(
            Periodicity.YEAR_1,
            Periodicity.timedelta_to_granularity(delta=timedelta(days=360)),
        )
        self.assertIs(
            Periodicity.YEAR_1,
            Periodicity.timedelta_to_granularity(delta=timedelta(days=366)),
        )

    def test_timedelta_to_granularity_over_max(self):
        self.assertIs(
            Periodicity.YEAR_1,
            Periodicity.timedelta_to_granularity(delta=timedelta(days=1_000)),
        )

    def test_max_for_period(self):
        period = Period(
            start=datetime(year=2025, month=1, day=1),
            end=datetime(year=2026, month=1, day=1),
        )

        optimized = Periodicity.max_for_period(period=period)
        self.assertIsInstance(optimized, Periodicity)
        self.assertIs(optimized, Periodicity.HOUR_12)

    def test_max_for_period_default(self):
        period = Period(
            start=datetime(year=333, month=1, day=1),
            end=datetime(year=2026, month=1, day=1),
        )

        optimized = Periodicity.max_for_period(period=period)
        self.assertIsInstance(optimized, Periodicity)
        self.assertIs(optimized, Periodicity.YEAR_1)

    def test_compute_opposite_minutes_end(self):
        base_date = datetime(
            year=2025,
            month=2,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=self.cet,
        )

        result = Periodicity.MINUTE_15._compute_opposite(base=base_date, opposite="end")

        self.assertIsInstance(result, datetime)
        self.assertEqual(result.minute, 15)
        self.assertEqual(result.isoformat(), "2025-02-01T00:15:00+01:00")

    def test_compute_opposite_minutes_start(self):
        base_date = datetime(
            year=2025,
            month=2,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=self.cet,
        )

        result = Periodicity.MINUTE_15._compute_opposite(
            base=base_date, opposite="start"
        )

        self.assertIsInstance(result, datetime)
        self.assertEqual(result.minute, 45)
        self.assertEqual(result.isoformat(), "2025-01-31T23:45:00+01:00")

    def test_compute_opposite_standard_end(self):
        base_date = datetime(
            year=2025,
            month=2,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=self.cet,
        )

        result = Periodicity.MONTH_3._compute_opposite(base=base_date, opposite="end")

        self.assertIsInstance(result, datetime)
        self.assertEqual(result.month, base_date.month + 3)
        self.assertEqual(result.isoformat(), "2025-05-01T00:00:00+02:00")

    def test_compute_opposite_straddling_years_end(self):
        base_date = datetime(
            year=2025,
            month=10,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=self.cet,
        )

        result = Periodicity.MONTH_6._compute_opposite(base=base_date, opposite="end")

        self.assertIsInstance(result, datetime)
        self.assertEqual(result.month, base_date.month - 6)
        self.assertEqual(result.year, base_date.year + 1)
        self.assertEqual(result.isoformat(), "2026-04-01T00:00:00+02:00")

    def test_compute_opposite_standard_start(self):
        base_date = datetime(
            year=2025,
            month=5,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=self.cet,
        )

        result = Periodicity.MONTH_3._compute_opposite(base=base_date, opposite="start")

        self.assertIsInstance(result, datetime)
        self.assertEqual(result.month, base_date.month - 3)
        self.assertEqual(result.isoformat(), "2025-02-01T00:00:00+01:00")

    def test_compute_opposite_straddling_years_start(self):
        base_date = datetime(
            year=2025,
            month=4,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=self.cet,
        )

        result = Periodicity.MONTH_6._compute_opposite(base=base_date, opposite="start")

        self.assertIsInstance(result, datetime)
        self.assertEqual(result.month, base_date.month + 6)
        self.assertEqual(result.year, base_date.year - 1)
        self.assertEqual(result.isoformat(), "2024-10-01T00:00:00+02:00")

    def test_compute_opposite_year_start(self):
        base_date = datetime(
            year=2025,
            month=4,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=self.cet,
        )

        result = Periodicity.YEAR_1._compute_opposite(base=base_date, opposite="start")

        self.assertIsInstance(result, datetime)
        self.assertEqual(result.year, base_date.year - 1)
        self.assertEqual(result.isoformat(), "2024-04-01T00:00:00+02:00")

    def test_to_magnitude_coef(self):
        m, c = Periodicity.HOUR_12._to_magnitude_coef()
        self.assertIsInstance(m, str)
        self.assertEqual(m, "HOUR")
        self.assertIsInstance(c, int)
        self.assertEqual(c, 12)

        m, c = Periodicity.YEAR_1._to_magnitude_coef()
        self.assertEqual(m, "YEAR")
        self.assertEqual(c, 1)

    def test_special_rounding_to_ten(self):
        result = Periodicity.MINUTE_10._special_rounding(value=0, round_at=10, offset=0)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

        result = Periodicity.MINUTE_10._special_rounding(value=1, round_at=10, offset=0)
        self.assertEqual(result, 0)

        result = Periodicity.MINUTE_10._special_rounding(value=13, round_at=10, offset=0)
        self.assertEqual(result, 10)

        result = Periodicity.MINUTE_10._special_rounding(value=20, round_at=10, offset=0)
        self.assertEqual(result, 20)

        result = Periodicity.MINUTE_10._special_rounding(value=37, round_at=10, offset=0)
        self.assertEqual(result, 30)

        result = Periodicity.MINUTE_10._special_rounding(value=59, round_at=10, offset=0)
        self.assertEqual(result, 50)

    def test_special_rounding_to_thirty(self):
        result = Periodicity.MINUTE_30._special_rounding(value=0, round_at=30, offset=0)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

        result = Periodicity.MINUTE_30._special_rounding(value=19, round_at=30, offset=0)
        self.assertEqual(result, 0)

        result = Periodicity.MINUTE_30._special_rounding(value=31, round_at=30, offset=0)
        self.assertEqual(result, 30)

        result = Periodicity.MINUTE_30._special_rounding(value=59, round_at=30, offset=0)
        self.assertEqual(result, 30)

    def test_special_rounding_to_fifteen(self):
        result = Periodicity.MINUTE_15._special_rounding(value=7, round_at=15, offset=0)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

        result = Periodicity.MINUTE_15._special_rounding(value=14, round_at=15, offset=0)
        self.assertEqual(result, 0)

        result = Periodicity.MINUTE_15._special_rounding(value=16, round_at=15, offset=0)
        self.assertEqual(result, 15)

        result = Periodicity.MINUTE_15._special_rounding(value=31, round_at=15, offset=0)
        self.assertEqual(result, 30)

        result = Periodicity.MINUTE_15._special_rounding(value=59, round_at=15, offset=0)
        self.assertEqual(result, 45)

    def test_special_rounding_to_six_with_offset(self):
        result = Periodicity.MONTH_6._special_rounding(value=1, round_at=6, offset=1)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1)

        result = Periodicity.MONTH_6._special_rounding(value=5, round_at=6, offset=1)
        self.assertEqual(result, 1)

        result = Periodicity.MONTH_6._special_rounding(value=7, round_at=6, offset=1)
        self.assertEqual(result, 7)

        result = Periodicity.MONTH_6._special_rounding(value=12, round_at=6, offset=1)
        self.assertEqual(result, 7)

    def test_round_week_straddling_month(self):
        base_date = datetime(year=2025, month=11, day=1, tzinfo=self.cet)
        day, month, year = Periodicity.WEEK_4._round_week(value=base_date, round_at=4)

        self.assertIsInstance(day, int)
        self.assertEqual(day, 6)
        self.assertIsInstance(month, int)
        self.assertEqual(month, 10)
        self.assertIsInstance(year, int)
        self.assertEqual(year, 2025)

    def test_round_week_straddling_year(self):
        base_date = datetime(year=2025, month=1, day=16, tzinfo=self.cet)
        day, month, year = Periodicity.WEEK_4._round_week(value=base_date, round_at=4)

        self.assertIsInstance(day, int)
        self.assertEqual(day, 30)
        self.assertIsInstance(month, int)
        self.assertEqual(month, 12)
        self.assertIsInstance(year, int)
        self.assertEqual(year, 2024)

    def test_round_month(self):
        base_date = datetime(year=2025, month=11, day=16, tzinfo=self.cet)
        day, month, year = Periodicity.MONTH_3._round_month(value=base_date, round_at=3)

        self.assertIsInstance(day, int)
        self.assertEqual(day, 1)
        self.assertIsInstance(month, int)
        self.assertEqual(month, 10)
        self.assertIsInstance(year, int)
        self.assertEqual(year, 2025)

        base_date = datetime(year=2025, month=4, day=1, tzinfo=self.cet)
        day, month, year = Periodicity.MONTH_3._round_month(value=base_date, round_at=3)

        self.assertEqual(day, 1)
        self.assertEqual(month, 4)
        self.assertEqual(year, 2025)

    def test_round_year(self):
        base_date = datetime(year=2025, month=11, day=16, tzinfo=self.cet)
        day, month, year = Periodicity.YEAR_1._round_year(year=base_date.year)

        self.assertIsInstance(day, int)
        self.assertEqual(day, 1)
        self.assertIsInstance(month, int)
        self.assertEqual(month, 1)
        self.assertIsInstance(year, int)
        self.assertEqual(year, 2025)

    def test_limit_periodicity_count(self):
        period = Period(
            start=datetime(year=2025, month=1, day=1),
            end=datetime(year=2026, month=1, day=1),
        )

        optimized = Periodicity.WEEK_1.limit_periodicity_count(period=period)
        self.assertIs(optimized, Periodicity.WEEK_1)

        # Because of 1 month Periodicity has a duration of 30 days
        # But the average duration over 1 year is 30.4375 days
        optimized = Periodicity.WEEK_1.limit_periodicity_count(
            period=period, max_point=13
        )
        self.assertIs(optimized, Periodicity.MONTH_1)

        # Same problem as before, there is 52.1786 weeks per year
        optimized = Periodicity.WEEK_1.limit_periodicity_count(
            period=period, max_point=14
        )
        self.assertIs(optimized, Periodicity.WEEK_4)

    def test_round_date_date(self):
        base_date = date(year=2025, month=11, day=1)
        result = Periodicity.WEEK_4.round_date(value=base_date)
        self.assertIsInstance(result, date)
        self.assertNotIsInstance(result, datetime)
        self.assertEqual(result, date(year=2025, month=10, day=6))

        result = Periodicity.MONTH_6.round_date(value=base_date)
        self.assertEqual(result, date(year=2025, month=7, day=1))
        result = Periodicity.YEAR_1.round_date(value=base_date)
        self.assertEqual(result, date(year=2025, month=1, day=1))

    def test_round_date_error(self):
        base_date = date(year=2025, month=11, day=1)
        with self.assertRaises(ValueError):
            Periodicity.HOUR_12.round_date(value=base_date)

    def test_round_date_datetime(self):
        base_date = datetime(year=2025, month=11, day=1)
        result = Periodicity.DAY_1.round_date(value=base_date)
        self.assertIsInstance(result, date)
        self.assertIsInstance(result, datetime)
        self.assertEqual(result, datetime(year=2025, month=11, day=1))

        result = Periodicity.MINUTE_15.round_date(value=base_date)
        self.assertEqual(result, datetime(year=2025, month=11, day=1))
        result = Periodicity.HOUR_1.round_date(value=base_date)
        self.assertEqual(result, datetime(year=2025, month=11, day=1))
        result = Periodicity.WEEK_1.round_date(value=base_date)
        self.assertEqual(result, datetime(year=2025, month=10, day=27))
        result = Periodicity.MONTH_3.round_date(value=base_date)
        self.assertEqual(result, datetime(year=2025, month=10, day=1))
        result = Periodicity.YEAR_1.round_date(value=base_date)
        self.assertEqual(result, datetime(year=2025, month=1, day=1))

    def test_count_in_period(self):
        period = Period(
            start=datetime(year=2025, month=1, day=1),
            end=datetime(year=2026, month=1, day=1),
        )
        self.assertEqual(Periodicity.MONTH_6.count_in_period(period=period), 2)
        self.assertEqual(Periodicity.MONTH_3.count_in_period(period=period), 4)
        self.assertEqual(Periodicity.WEEK_4.count_in_period(period=period), 13)
        self.assertEqual(Periodicity.DAY_1.count_in_period(period=period), 365)
        self.assertEqual(Periodicity.HOUR_1.count_in_period(period=period), 8_760)

    def test_to_period_from_start(self):
        start = datetime(year=2025, month=11, day=1)
        period = Periodicity.WEEK_1.to_period_from_start(start=start)

        self.assertIsInstance(period, Period)
        self.assertEqual(period.start, start)
        self.assertEqual(period.end, datetime(year=2025, month=11, day=8))

    def test_to_period_from_end(self):
        end = datetime(year=2025, month=11, day=8)
        period = Periodicity.WEEK_1.to_period_from_end(end=end)

        self.assertIsInstance(period, Period)
        self.assertEqual(period.end, end)
        self.assertEqual(period.start, datetime(year=2025, month=11, day=1))

    def test_get_next_date(self):
        base = datetime(year=2025, month=6, day=25)
        result = Periodicity.MONTH_6.get_next_date(value=base)

        self.assertIsInstance(result, date)
        self.assertIsInstance(result, datetime)
        self.assertEqual(result, datetime(year=2025, month=12, day=25))

    def test_get_prev_date(self):
        base = datetime(year=2025, month=6, day=25)
        result = Periodicity.MONTH_6.get_prev_date(value=base)

        self.assertIsInstance(result, date)
        self.assertIsInstance(result, datetime)
        self.assertEqual(result, datetime(year=2024, month=12, day=25))

    def test_split_in_sub_periods(self):
        period = Period(
            start=datetime(year=2025, month=1, day=1),
            end=datetime(year=2026, month=1, day=1),
        )

        periods = [w for w in Periodicity.WEEK_1.split_in_sub_periods(period=period)]
        base_date = None
        for sub_period in periods:
            if base_date == None:
                base_date = sub_period.start

            with self.subTest(str(sub_period)):
                self.assertIsInstance(sub_period, Period)
                self.assertEqual(sub_period.to_timedelta().total_seconds(), 604_800)
                self.assertEqual(sub_period.start, base_date)

                base_date = sub_period.end
