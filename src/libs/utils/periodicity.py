from datetime import date, datetime, timedelta
from enum import Enum
from typing import Any, Generator, Self

from .enum_mixin import EnumMixin
from .period import Period

MAX_POINTS = 1250  # Arbitrary fixed


class Periodicity(EnumMixin, Enum):
    """Periodicity with rounded time duration"""

    MINUTE_1 = 60
    MINUTE_5 = 60 * 5
    MINUTE_10 = 60 * 10
    MINUTE_15 = 60 * 15
    MINUTE_30 = 60 * 30
    HOUR_1 = 60 * 60
    HOUR_4 = 60 * 60 * 4
    HOUR_6 = 60 * 60 * 6
    HOUR_12 = 60 * 60 * 12
    DAY_1 = 60 * 60 * 24
    WEEK_1 = 60 * 60 * 24 * 7
    WEEK_2 = 60 * 60 * 24 * 14
    WEEK_4 = 60 * 60 * 24 * 28
    MONTH_1 = 60 * 60 * 24 * 30
    MONTH_3 = 60 * 60 * 24 * 90
    MONTH_6 = 60 * 60 * 24 * 180
    YEAR_1 = 60 * 60 * 24 * 365

    def __str__(self):
        magnitude, value = self._to_magnitude_coef()
        plural = "s" if int(value) > 1 else ""
        return f"{value} {magnitude.lower()}{plural}"

    @classmethod
    def timedelta_to_granularity(cls, delta: timedelta) -> Self:
        """Convert roughly a timedelta to a Periodicity"""

        seconds = delta.total_seconds()
        for p in sorted(Periodicity, key=lambda p: p.value):
            if seconds <= p.value * 1.05:
                return p
        else:
            return sorted(Periodicity, key=lambda p: p.value, reverse=True)[0]

    @classmethod
    def max_for_period(cls, period: Period, max_point: int = MAX_POINTS) -> Self:
        """
        Define the max Periodicity occurring in the period
        according to max_point value
        """

        seconds = period.to_timedelta().total_seconds()
        for p in sorted(Periodicity, key=lambda p: p.value):
            if seconds // max_point <= p.value:
                return p

        else:
            return sorted(Periodicity, key=lambda p: p.value, reverse=True)[0]

    def _operation_opposite(self, lhs: Any, rhs: Any, opposite: str) -> Any:
        """Helper to limit code redundancy"""

        return (lhs + rhs) if opposite == "end" else (lhs - rhs)

    def _compute_opposite(self, base: date | datetime, opposite: str) -> date | datetime:
        """Compute the missing part of a period to build one"""

        magnitude, coef = self._to_magnitude_coef()

        if magnitude in ["DAY", "WEEK"]:
            if magnitude == "WEEK":
                coef = coef * 7

            # TODO: Inaccuracy for WEEK_X if X > 1
            # Handle the 53th week every 5-6 years (roughly 71 times per 400 years)
            # If 1st day of the year is a Thursday
            # And if the 1st day of the year is a Wednesday and it's a leap year

            computed = self._operation_opposite(
                lhs=base, rhs=timedelta(days=coef), opposite=opposite
            )

        elif magnitude == "MONTH":
            month = (
                self._operation_opposite(lhs=base.month, rhs=coef, opposite=opposite)
                % 12
            )

            if month == 0:
                month = 12

            incr_year = 0
            if month < base.month and opposite == "end":
                incr_year = 1
            elif month > base.month and opposite == "start":
                incr_year = -1

            computed = base.replace(year=base.year + incr_year, month=month)

        elif magnitude == "YEAR":
            computed = base.replace(
                year=self._operation_opposite(lhs=base.year, rhs=coef, opposite=opposite)
            )

        else:
            computed = self._operation_opposite(
                lhs=base, rhs=timedelta(seconds=self.value), opposite=opposite
            )

        return computed

    def _to_magnitude_coef(self) -> tuple[str, int]:
        """Use enum name to get a more precise behavior"""

        m, c = self.name.split("_")
        return m, int(c)

    def _special_rounding(self, value: int, round_at: int, offset: int = 0) -> int:
        """Round a date part to get a consistent Periodicity start"""

        return (((value - offset) // round_at) * round_at) + offset

    def _round_week(self, value: date | datetime, round_at: int) -> tuple[int, int, int]:
        """Round to a week, looking for a Monday"""

        value = value - timedelta(days=value.weekday())
        week_x = value.isocalendar()[1] - 1

        delta_days = (week_x % round_at) * 7
        new_date = value - timedelta(days=delta_days)

        return new_date.day, new_date.month, new_date.year

    def _round_month(
        self, value: date | datetime, round_at: int
    ) -> tuple[int, int, int]:
        """Round to the first day of the month"""

        value = value.replace(day=1)

        # 28 because of febuary and ok for 6 months
        delta_days = ((value.month - 1) % round_at) * 28

        if delta_days:
            new_date = value - timedelta(days=delta_days)
        else:
            new_date = value

        return 1, new_date.month, new_date.year

    def _round_year(self, year: int) -> tuple[int, int, int]:
        """Round to the first day, and the first month of a year"""
        return 1, 1, year

    def _round_datetime(self, value: datetime) -> datetime:
        """Select the right rounding method according to Periodicity name"""

        microsecond = 0
        second = 0
        minute = 0
        hour = value.hour
        day = value.day
        month = value.month
        year = value.year

        magnitude, coef_value = self._to_magnitude_coef()

        if magnitude == "MINUTE":
            minute = self._special_rounding(value=value.minute, round_at=coef_value)

        elif magnitude == "HOUR":
            hour = self._special_rounding(value=value.hour, round_at=coef_value)

        elif magnitude == "DAY":
            hour = 0

        elif magnitude == "WEEK":
            day, month, year = self._round_week(value=value, round_at=coef_value)

        elif magnitude == "MONTH":
            day, month, year = self._round_month(value=value, round_at=coef_value)

        elif magnitude == "YEAR":
            day, month, year = self._round_year(year=value.year)

        return datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond,
        )

    def _round_date(self, value: date) -> date:
        """Select the right rounding method according to Periodicity name"""

        day = value.day
        month = value.month
        year = value.year

        magnitude, coef_value = self._to_magnitude_coef()

        if magnitude == "WEEK":
            day, month, year = self._round_week(value=value, round_at=coef_value)

        elif magnitude == "MONTH":
            day, month, year = self._round_month(value=value, round_at=coef_value)

        elif magnitude == "YEAR":
            day, month, year = self._round_year(year=value.year)

        return date(year=year, month=month, day=day)

    def limit_periodicity_count(
        self, period: Period, max_point: int = MAX_POINTS
    ) -> Self:
        """Limit periodicity to restrict the number occurring in a period"""

        seconds = period.to_timedelta().total_seconds()

        if seconds // max_point > self.value:
            return Periodicity.max_for_period(period=period, max_point=max_point)

        return self

    def round_date(self, value: date | datetime) -> date | datetime:
        """Round a date according to periodicity"""

        if isinstance(value, datetime):
            return self._round_datetime(value=value)

        elif isinstance(value, date) and self.value >= Periodicity.DAY_1.value:
            return self._round_date(value=value)

        else:
            raise ValueError("A date object cannot be rounded under a daily basis")

    def count_in_period(self, period: Period) -> int:
        """Return the number of periodicity in a period"""

        return period.to_timedelta().total_seconds() // self.value

    def get_next_date(self, value: date | datetime) -> date | datetime:
        """
        Get the next date according to periodicity
        Not accurate for month or year periodicity
        """

        return self._compute_opposite(base=value, opposite="end")

    def get_prev_date(self, value: date | datetime) -> date | datetime:
        """
        Get the next date according to periodicity
        Not accurate for month or year periodicity
        """

        return self._compute_opposite(base=value, opposite="start")

    def to_period_from_start(self, start: date | datetime) -> Period:
        """Create a period computing the end date from Periodicity"""

        end = self.get_next_date(value=start)

        return Period(start=start, end=end)

    def to_period_from_end(self, end: date | datetime) -> Period:
        """Create a period computing the start date from Periodicity"""

        start = self.get_prev_date(value=end)

        return Period(start=start, end=end)

    def split_in_sub_periods(self, period: Period) -> Generator[Period, None, None]:
        """Create some sub periods according to Periodicity needed"""

        current = period.start
        while current < period.end:
            end = self.get_next_date(current)
            yield Period(start=current, end=end)
            current = end
