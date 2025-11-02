from enum import Enum
from datetime import date, datetime, timedelta
from typing import Self
from zoneinfo import ZoneInfo

from .enum_mixin import EnumMixin


class PeriodTypes(EnumMixin, Enum):
    AUTO = "auto"
    DATE = "date"
    DATETIME = "datetime"
    NAIVE = "naive_datetime"


class Period:
    """
    Period object represent an interval of time between two dates:
    [start; end[
    """

    type: PeriodTypes
    start: date | datetime
    end: date | datetime

    def __init__(
        self,
        start: date | datetime | str,
        end: date | datetime | str,
        tz: ZoneInfo | None = None,
        type: PeriodTypes = PeriodTypes.AUTO,
    ):
        """Setup Period object from various type and check consistency"""

        self.type = type
        self.start = self._check_type(self._to_date_obj(value=start, tz=tz))
        self.end = self._check_type(self._to_date_obj(value=end, tz=tz))

        self._check_consistency()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(start={repr(self.start)}, end={repr(self.end)})"
        )

    def __str__(self) -> str:
        return f"{self.start.isoformat()} - {self.end.isoformat()}"

    def __bool__(self) -> bool:
        return self.to_timedelta().total_seconds() >= 0

    def _to_date_obj(
        self, value: date | datetime | str, tz: ZoneInfo = None
    ) -> date | datetime:
        """Convert a string to a date or datetime object"""

        period_value = value
        if isinstance(value, str):
            try:
                period_value = date.fromisoformat(value)
            except ValueError as e1:
                try:
                    period_value = datetime.fromisoformat(value)
                    if tz:
                        period_value = value.astimezone(tz=tz)
                except ValueError as e2:
                    raise ValueError(
                        f"{self.__class__.__name__} string format unknown: {e1} -- {e2}"
                    )

        if isinstance(period_value, date):
            return period_value

        raise ValueError(f"Invalid value '{type(value)}' for {self.__class__.__name__}")

    def _check_type(self, value: date | datetime) -> date | datetime:
        """Check period type"""

        if isinstance(value, datetime):
            period_type = PeriodTypes.DATETIME

            if value.tzinfo is None:
                period_type = PeriodTypes.NAIVE

        elif isinstance(value, date):
            period_type = PeriodTypes.DATE

        if self.type is PeriodTypes.AUTO or self.type is period_type:
            self.type = period_type
            return value
        else:
            raise ValueError(
                f"Invalid type '{period_type}' for {self.__class__.__name__}"
                f", type required: {self.type}"
            )

    def _check_consistency(self) -> None:
        """Check for period consistency"""

        utc = ZoneInfo("UTC")
        if (
            self.type in [PeriodTypes.DATE, PeriodTypes.NAIVE] and self.start > self.end
        ) or (
            self.type is PeriodTypes.DATETIME
            and self.start.astimezone(tz=utc) > self.end.astimezone(tz=utc)
        ):
            raise ValueError(
                f"Start date greater than end date: {self.start} > {self.end}"
            )

    def contain(self, value: date | datetime | str) -> bool:
        """Check if period include a date or datetime"""

        comp_date = self._check_type(self._to_date_obj(value))
        if self.type == PeriodTypes.DATETIME:
            utc = ZoneInfo("UTC")
            return (
                self.start.astimezone(tz=utc) <= comp_date < self.end.astimezone(tz=utc)
            )

        else:
            return self.start <= comp_date < self.end

    def split_at(self, value: date | datetime | str) -> tuple[Self, Self]:
        """Split a period in two periods from a date in between start and end"""

        comp_date = self._check_type(self._to_date_obj(value))
        if self.contain(value=value):
            return (
                Period(start=self.start, end=comp_date),
                Period(start=comp_date, end=self.end),
            )
        else:
            ValueError(
                f"The value given '{comp_date}' is not included in period: "
                f"[{self.start}; {self.end}["
            )

    def to_timedelta(self) -> timedelta:
        """Convert a period to a duration"""

        return self.end - self.start

    def prev_period(self) -> Self:
        """Return the same duration period before this one"""

        delta = self.to_timedelta()
        return Period(start=self.start - delta, end=self.start)

    def next_period(self) -> Self:
        """Return the same duration period after this one"""

        delta = self.to_timedelta()
        return Period(start=self.end, end=self.end + delta)

    def is_instant(self) -> bool:
        """Check if period is an instant"""

        return self.to_timedelta().total_seconds() == 0

    def is_covered(self, period: Self) -> bool:
        """Check if period is covered by another"""

        return period.start <= self.start and self.end <= period.end

    def is_intersected(self, period: Self) -> bool:
        """Check if partially covered"""

        before = period.start < self.start < period.end
        after = period.start < self.end < period.end

        return before or after

    def is_joined(self, period: Self) -> bool:
        """Check if period is joined"""

        return self.start == period.end or self.end == period.start
