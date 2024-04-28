from typing import TypeVar

from src.libs.sqlalchemy.queryset import Queryset
from src.logtrail.models import LogTrail

TLogTrailQueryset = TypeVar("TLogTrailQueryset", bound="LogTrailQueryset")


class LogTrailQueryset(Queryset):
    def __init__(self):
        super().__init__(LogTrail)

    def of_type(self, log_type: str) -> TLogTrailQueryset:
        self._query = self._query.where(LogTrail.log_type == log_type)
        return self
