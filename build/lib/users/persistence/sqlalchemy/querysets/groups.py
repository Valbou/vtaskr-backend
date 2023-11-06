from src.libs.sqlalchemy.queryset import Queryset
from src.users.models import Group


class GroupQueryset(Queryset):
    def __init__(self):
        super().__init__(Group)
