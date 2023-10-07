from vtaskr.libs.sqlalchemy.queryset import Queryset
from vtaskr.users.models import RoleType


class RoleTypeQueryset(Queryset):
    def __init__(self):
        super().__init__(RoleType)
