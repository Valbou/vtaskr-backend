from typing import List, TypeVar

from sqlalchemy import select

from .querystring import Filter, Operations

TQueryset = TypeVar("TQueryset", bound="Queryset")


class Queryset:
    """
    Queryset is used to avoid duplication in SQL queries.
    It's particulary usefull on complex queries.
    """

    def __init__(self, qs_class):
        self.qs_class = qs_class
        self.query = select(qs_class)

    def page(self, page_number: int, per_page: int = 100) -> TQueryset:
        """A simple paginator"""
        offset = (page_number - 1) * per_page
        self.query = self.query.offset(offset).limit(per_page)
        return self

    def from_filters(self, filters: List[Filter]) -> TQueryset:
        """
        Build a query statement from query string filters
        """
        self._add_where(filters)
        self._add_order_by(filters)
        self._add_page(filters)
        return self

    def _add_where(self, filters: List[Filter]) -> None:
        """Apply a where clause according to filters"""
        [
            self._add_simple_where_clause(f)
            for f in filters
            if f.operation not in [Operations.IN, Operations.NIN]
        ]
        self._add_composed_where_clause(
            [fs for fs in filters if fs.operation is Operations.IN], Operations.IN
        )
        self._add_composed_where_clause(
            [fs for fs in filters if fs.operation is Operations.NIN], Operations.NIN
        )

    def _add_simple_where_clause(self, f: Filter):
        if f.operation == Operations.EQ:
            self.query = self.query.where(getattr(self.qs_class, f.field) == f.value)
        elif f.operation == Operations.NEQ:
            self.query = self.query.where(getattr(self.qs_class, f.field) != f.value)
        elif f.operation == Operations.LT:
            self.query = self.query.where(getattr(self.qs_class, f.field) < f.value)
        elif f.operation == Operations.LTE:
            self.query = self.query.where(getattr(self.qs_class, f.field) <= f.value)
        elif f.operation == Operations.GT:
            self.query = self.query.where(getattr(self.qs_class, f.field) > f.value)
        elif f.operation == Operations.GTE:
            self.query = self.query.where(getattr(self.qs_class, f.field) >= f.value)
        elif f.operation == Operations.CONTAINS:
            self.query = self.query.where(
                getattr(self.qs_class, f.field).contains(f.value)
            )
        elif f.operation == Operations.STARTSWITH:
            self.query = self.query.where(
                getattr(self.qs_class, f.field).startswith(f.value)
            )
        elif f.operation == Operations.ENDSWITH:
            self.query = self.query.where(
                getattr(self.qs_class, f.field).endswith(f.value)
            )

    def _add_composed_where_clause(self, fs: List[Filter], operation: Operations):
        fields = {f.field for f in fs}
        for field in fields:
            values = [f.value for f in fs if f.field == field]
            if operation == Operations.IN:
                self.query = self.query.where(getattr(self.qs_class, field).in_(values))
            elif operation == Operations.NIN:
                self.query = self.query.where(
                    getattr(self.qs_class, field).notin_(values)
                )

    def _add_order_by(self, filters: List[Filter]) -> None:
        """Apply order by clauses found in filters"""

        order_by_filters = [
            f for f in filters if f.operation in [Operations.ASC, Operations.DESC]
        ]
        for order in order_by_filters:
            if order.operation == Operations.DESC:
                self.query = self.query.order_by(
                    getattr(self.qs_class, order.field).desc()
                )
            else:
                self.query = self.query.order_by(
                    getattr(self.qs_class, order.field).asc()
                )

    def _add_page(self, filters: List[Filter]) -> None:
        """
        Apply pagination constraints
        offset and page cannot be used together
        page has the precedence over offset
        """
        limit = 100
        limit_filter = [f for f in filters if f.operation == Operations.LIMIT]
        if len(limit_filter) > 0:
            limit = int(limit_filter[0].value)

        offset = 0
        offset_filter = [f for f in filters if f.operation == Operations.OFFSET]
        if len(offset_filter) > 0:
            offset = int(offset_filter[0].value)

        page_filter = [f for f in filters if f.operation == Operations.PAGE]
        if len(page_filter) > 0:
            offset = (int(page_filter[0].value) - 1) * limit

        self.query = self.query.offset(offset).limit(limit)
