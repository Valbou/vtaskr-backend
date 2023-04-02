from dataclasses import dataclass
from enum import Enum
from typing import List
from urllib.parse import parse_qs


class Operations(Enum):
    ASC = "order ASC"
    DESC = "order DESC"
    OFFSET = "offset"
    LIMIT = "limit"
    PAGE = "page"
    EQ = "equal"
    NEQ = "not equal"
    LT = "lower than"
    LTE = "lower than equal"
    GT = "greater than"
    GTE = "greater than equal"
    IN = "in"
    NIN = "not in"
    CONTAINS = "contains"
    NCONTAINS = "not contains"
    STARTSWITH = "starts with"
    NSTARTSWITH = "not starts with"
    ENDSWITH = "ends with"
    NENDSWITH = "not ends with"


@dataclass
class Filter:
    field: str
    operation: Operations
    value: str


class QueryStringFilter:
    _filters: list = []

    def __init__(self, query_string: str):
        self._filters = []
        raw_data = parse_qs(query_string)
        for k, v in raw_data.items():
            list_values = self._separate_values(v)
            [self._create_filter(k, val) for val in list_values if val]

    def _separate_values(self, values: List[str]) -> List[str]:
        new_values = []
        for value in values:
            new_values.extend(value.split(","))
        return new_values

    def _create_filter(self, key: str, value: str):
        field, op = self._parse_key(key, value)
        if field and op:
            self._filters.append(Filter(field=field, operation=op, value=value))

    def _parse_key(self, key: str, value: str):
        if "_" in key:
            for op in Operations:
                op_name = f"_{op.name.lower()}"
                if key.endswith(op_name):
                    size = len(op_name)
                    return key[:-size], op

        elif key == "orderby":
            if value.startswith("-"):
                return value[1:], Operations.DESC
            else:
                return value, Operations.ASC

        elif key == "offset":
            return key, Operations.OFFSET
        elif key == "limit":
            return key, Operations.LIMIT
        elif key == "page":
            return key, Operations.PAGE

        return None, None

    def get_filters(self) -> List[Filter]:
        return self._filters
