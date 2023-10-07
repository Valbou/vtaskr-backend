from vtaskr.libs.sqlalchemy.default_adapter import DefaultDB
from vtaskr.users.persistence.ports import AbstractRightPort
from vtaskr.users.persistence.sqlalchemy.querysets import RightQueryset


class RightDB(AbstractRightPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = RightQueryset()
