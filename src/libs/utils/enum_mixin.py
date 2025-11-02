from enum import Enum


class EnumMixin:
    @classmethod
    def get_enum_from_value(cls, value) -> Enum:
        try:
            return [e for e in cls if e.value == value][0]
        except IndexError:
            raise ValueError(f"{value} not a valid value for enum {cls.__name__}")

    @classmethod
    def get_enum_from_name(cls, name: str) -> Enum:
        try:
            return [e for e in cls if e.name == name.upper()][0]
        except IndexError:
            raise ValueError(f"{name} not a valid name for enum {cls.__name__}")
