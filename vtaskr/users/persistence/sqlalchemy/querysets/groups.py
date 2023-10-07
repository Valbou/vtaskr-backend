from vtaskr.libs.sqlalchemy.queryset import Queryset
from vtaskr.users.models import Group


class GroupQueryset(Queryset):
    def __init__(self):
        super().__init__(Group)
