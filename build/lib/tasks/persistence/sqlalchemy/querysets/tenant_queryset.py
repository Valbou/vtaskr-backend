from src.libs.sqlalchemy.queryset import Queryset


class TenantQueryset(Queryset):
    def __init__(self, qs_class):
        super().__init__(qs_class)

    def tenants(self, tenant_ids: list[str]):
        self._query = self._query.where(self.qs_class.tenant_id.in_(tenant_ids))
        return self
