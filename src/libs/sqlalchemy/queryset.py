from typing import TypeVar

from sqlalchemy import delete, not_, select, update

from ..flask.querystring import Filter, Operations

TQueryset = TypeVar("TQueryset", bound="Queryset")


class Queryset:
    """
    Queryset is used to avoid duplication in SQL queries.
    It's particulary usefull to chain complex queries.
    """

    def __init__(self, qs_class):
        self.qs_class = qs_class
        self._query = None
        self.select()

    @property
    def statement(self):
        statement = self._query
        self.clean()
        return statement

    def clean(self) -> None:
        self.select()

    def select(self, *args) -> TQueryset:
        self._query = select(*args) if args else select(self.qs_class)
        return self

    def update(self) -> TQueryset:
        self._query = update(self.qs_class)
        return self

    def delete(self) -> TQueryset:
        self._query = delete(self.qs_class)
        return self

    def values(self, **kwargs) -> TQueryset:
        self._query = self._query.values(**kwargs)
        return self

    def join(self, column) -> TQueryset:
        self._query = self._query.join(column)
        return self

    def where(self, *args) -> TQueryset:
        self._query = self._query.where(*args)
        return self

    def id(self, id: str) -> TQueryset:
        self._query = self._query.where(self.qs_class.id == id)
        return self

    def ids(self, ids: list[str]) -> TQueryset:
        self._query = self._query.where(self.qs_class.id.in_(ids))
        return self

    def page(self, page_number: int, per_page: int = 100) -> TQueryset:
        """A simple paginator"""
        offset = (page_number - 1) * per_page
        self._query = self._query.offset(offset).limit(per_page)
        return self

    def from_filters(self, filters: list[Filter]) -> TQueryset:
        """
        Build a query statement from query string filters
        """
        self._add_where(filters)
        self._add_order_by(filters)
        self._add_page(filters)
        return self

    def _add_where(self, filters: list[Filter]) -> None:
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
            self._query = self._query.where(getattr(self.qs_class, f.field) == f.value)
        elif f.operation == Operations.NEQ:
            self._query = self._query.where(getattr(self.qs_class, f.field) != f.value)
        elif f.operation == Operations.LT:
            self._query = self._query.where(getattr(self.qs_class, f.field) < f.value)
        elif f.operation == Operations.LTE:
            self._query = self._query.where(getattr(self.qs_class, f.field) <= f.value)
        elif f.operation == Operations.GT:
            self._query = self._query.where(getattr(self.qs_class, f.field) > f.value)
        elif f.operation == Operations.GTE:
            self._query = self._query.where(getattr(self.qs_class, f.field) >= f.value)
        elif f.operation == Operations.CONTAINS:
            self._query = self._query.where(
                getattr(self.qs_class, f.field).contains(f.value)
            )
        elif f.operation == Operations.NCONTAINS:
            self._query = self._query.where(
                not_(getattr(self.qs_class, f.field).contains(f.value))
            )
        elif f.operation == Operations.STARTSWITH:
            self._query = self._query.where(
                getattr(self.qs_class, f.field).startswith(f.value)
            )
        elif f.operation == Operations.NSTARTSWITH:
            self._query = self._query.where(
                not_(getattr(self.qs_class, f.field).startswith(f.value))
            )
        elif f.operation == Operations.ENDSWITH:
            self._query = self._query.where(
                getattr(self.qs_class, f.field).endswith(f.value)
            )
        elif f.operation == Operations.NENDSWITH:
            self._query = self._query.where(
                not_(getattr(self.qs_class, f.field).endswith(f.value))
            )

    def _add_composed_where_clause(self, fs: list[Filter], operation: Operations):
        fields = {f.field for f in fs}
        for field in fields:
            values = [f.value for f in fs if f.field == field]
            if operation == Operations.IN:
                self._query = self._query.where(
                    getattr(self.qs_class, field).in_(values)
                )
            elif operation == Operations.NIN:
                self._query = self._query.where(
                    getattr(self.qs_class, field).notin_(values)
                )

    def _add_order_by(self, filters: list[Filter]) -> None:
        """Apply order by clauses found in filters"""

        order_by_filters = [
            f for f in filters if f.operation in [Operations.ASC, Operations.DESC]
        ]
        for order in order_by_filters:
            if order.operation == Operations.DESC:
                self._query = self._query.order_by(
                    getattr(self.qs_class, order.field).desc()
                )
            else:
                self._query = self._query.order_by(
                    getattr(self.qs_class, order.field).asc()
                )

    def _add_page(self, filters: list[Filter]) -> None:
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

        self._query = self._query.offset(offset).limit(limit)
