from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from vtasks.users.models import RequestChange
from vtasks.users.persistence.ports import AbstractRequestChangePort


class RequestChangeDB(AbstractRequestChangePort):
    def load(self, session: Session, id: str) -> Optional[RequestChange]:
        stmt = select(RequestChange).where(RequestChange.id == id)
        result = session.scalars(stmt).one_or_none()
        return result

    def find_request(
        self, session: Session, email: str, autocommit: bool = True
    ) -> Optional[RequestChange]:
        stmt = (
            select(RequestChange)
            .where(
                RequestChange.email == email,
                RequestChange.created_at > RequestChange.valid_after(),
            )
            .order_by(RequestChange.created_at.desc())
            .limit(1)
        )
        result = session.scalars(stmt).one_or_none()
        return result

    def save(
        self, session: Session, request_change: RequestChange, autocommit: bool = True
    ):
        session.add(request_change)
        if autocommit:
            session.commit()

    def clean_history(self, session: Session, autocommit: bool = True):
        stmt = delete(RequestChange).where(
            RequestChange.created_at < RequestChange.history_expired_before()
        )
        session.execute(stmt)
        if autocommit:
            session.commit()

    def delete(
        self, session: Session, request_change: RequestChange, autocommit: bool = True
    ):
        session.delete(request_change)
        if autocommit:
            session.commit()

    def exists(self, session: Session, id: str) -> bool:
        return session.query(
            select(RequestChange).where(RequestChange.id == id).exists()
        ).scalar()
