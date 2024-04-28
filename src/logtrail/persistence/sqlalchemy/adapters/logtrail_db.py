from sqlalchemy.orm import Session

from src.libs.sqlalchemy.default_adapter import DefaultDB
from src.logtrail.models import LogTrail
from src.logtrail.persistence.ports import AbstractLogTrailPort
from src.logtrail.persistence.sqlalchemy.querysets import LogTrailQueryset


class LogTrailDB(AbstractLogTrailPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = LogTrailQueryset()

    def get_all(self, session: Session) -> list[LogTrail]:
        self.qs.select().order_by(created_at="DESC").limit(100)
        return session.scalars(self.qs.statement).all()

    def get_all_from_tenant(self, session: Session, tenant_id: str) -> list[LogTrail]:
        self.qs.select().where(LogTrail.tenant_id == tenant_id).order_by(
            created_at="DESC"
        ).limit(100)
        return session.scalars(self.qs.statement).all()
