from babel import Locale
from sqlalchemy import Dialect, String, types


class LocaleField(types.TypeDecorator):
    impl = String(5)
    cache_ok = True

    def process_bind_param(self, value: Locale, dialect: Dialect) -> str:
        return str(value)

    def process_result_value(self, value: str, dialect: Dialect) -> Locale:
        return Locale.parse(value)
