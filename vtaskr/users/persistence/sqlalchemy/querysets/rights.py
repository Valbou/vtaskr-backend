from vtaskr.libs.sqlalchemy.queryset import Queryset
from vtaskr.users.models import Right


class RightQueryset(Queryset):
    def __init__(self):
        super().__init__(Right)
