from enum import Enum
from unittest import TestCase

from src.libs.utils import EnumMixin


class EnumTest(EnumMixin, Enum):
    CASE_A = "case a"
    CASE_B = "case b"
    CASE_C = "case c"


class TestEnumMixin(TestCase):
    def test_get_enum_from_value(self):
        ea = EnumTest.get_enum_from_value("case a")
        self.assertIs(ea, EnumTest.CASE_A)

        ec = EnumTest.get_enum_from_value("case c")
        self.assertIs(ec, EnumTest.CASE_C)

    def test_get_enum_from_name(self):
        ea = EnumTest.get_enum_from_name("CASE_A")
        self.assertIs(ea, EnumTest.CASE_A)

        eb = EnumTest.get_enum_from_name("CASE_B")
        self.assertIs(eb, EnumTest.CASE_B)
