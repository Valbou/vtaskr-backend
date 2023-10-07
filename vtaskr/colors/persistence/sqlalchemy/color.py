from typing import Optional

from sqlalchemy import Dialect, String, types

from vtaskr.colors.models.color import Color


class ColorType(types.TypeDecorator):
    impl = String(20)
    cache_ok = True

    def process_bind_param(self, value: Color, dialect: Dialect) -> str:
        return str(value)

    def process_result_value(self, value: str, dialect: Dialect) -> Optional[Color]:
        return Color.from_string(value) if value else None
