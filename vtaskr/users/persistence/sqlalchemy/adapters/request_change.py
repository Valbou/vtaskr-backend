from typing import Optional

from sqlalchemy.orm import Session

from vtaskr.users.models import RequestChange
from vtaskr.users.persistence.ports import AbstractRequestChangePort
from vtaskr.users.persistence.sqlalchemy.querysets import RequestChangeQueryset


class RequestChangeDB(AbstractRequestChangePort):
    def __init__(self) -> None:
        super().__init__()
        self.req_change_qs = RequestChangeQueryset()

    def load(self, session: Session, id: str) -> Optional[RequestChange]:
        self.req_change_qs.id(id)
        result = session.scalars(self.req_change_qs.statement).one_or_none()
        return result

    def find_request(self, session: Session, email: str) -> Optional[RequestChange]:
        self.req_change_qs.valid_for(email).last()
        result = session.scalars(self.req_change_qs.statement).one_or_none()
        return result

    def save(
        self, session: Session, request_change: RequestChange, autocommit: bool = True
    ):
        session.add(request_change)
        if autocommit:
            session.commit()

    def clean_history(self, session: Session, autocommit: bool = True):
        self.req_change_qs.delete().expired()
        session.execute(self.req_change_qs.statement)
        if autocommit:
            session.commit()

    def delete(
        self, session: Session, request_change: RequestChange, autocommit: bool = True
    ):
        session.delete(request_change)
        if autocommit:
            session.commit()

    def exists(self, session: Session, id: str) -> bool:
        self.req_change_qs.id(id)
        return session.query(self.req_change_qs.statement.exists()).scalar()
