from sqlalchemy.orm import Session

from src.libs.sqlalchemy.default_adapter import DefaultDB
from src.users.models import RequestChange, RequestType
from src.users.persistence.ports import RequestChangeDBPort
from src.users.persistence.sqlalchemy.querysets import RequestChangeQueryset


class RequestChangeDB(RequestChangeDBPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = RequestChangeQueryset()

    def update(self, session, request_change: RequestChange) -> None:
        self.qs.update().id(request_change.id).values(
            code=request_change.code,
        )
        session.execute(self.qs.statement)

    def find_request(
        self, session: Session, email: str, request_type: RequestType
    ) -> RequestChange | None:
        self.qs.select().valid_for(email, request_type).last()
        result = session.scalars(self.qs.statement).one_or_none()
        return result

    def clean_history(self, session: Session):
        self.qs.delete().expired()
        session.execute(self.qs.statement)
