from sqlalchemy.orm import Session

from vtaskr.libs.sqlalchemy.default_adapter import DefaultDB
from vtaskr.users.models import RequestChange
from vtaskr.users.persistence.ports import AbstractRequestChangePort
from vtaskr.users.persistence.sqlalchemy.querysets import RequestChangeQueryset


class RequestChangeDB(AbstractRequestChangePort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = RequestChangeQueryset()

    def find_request(self, session: Session, email: str) -> RequestChange | None:
        self.qs.valid_for(email).last()
        result = session.scalars(self.qs.statement).one_or_none()
        return result

    def clean_history(self, session: Session, autocommit: bool = True):
        self.qs.delete().expired()
        session.execute(self.qs.statement)
        if autocommit:
            session.commit()
