from typing import TypeVar

from src.libs.sqlalchemy.queryset import Queryset
from src.notifications.models import Contact

TContactQueryset = TypeVar("TContactQueryset", bound="ContactQueryset")


class ContactQueryset(Queryset):
    def __init__(self):
        super().__init__(Contact)
