from src.libs.dependencies import DependencyInjector
from src.logtrail.models import LogTrail
from src.logtrail.persistence.sqlalchemy.adapters import LogTrailDB


class LogTrailService:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.logtrail_db = LogTrailDB()

    def get_all(self) -> list[LogTrail]:
        with self.services.persistence.get_session() as session:
            return self.logtrail_db.get_all(session=session)

    def get_all_from_tenant_id(self, tenant_id: str) -> list[LogTrail]:
        with self.services.persistence.get_session() as session:
            return self.logtrail_db.get_all_from_tenant(
                session=session, tenant_id=tenant_id
            )

    def add(
        self,
        tenant_id: str,
        log_type: str,
        event: dict,
    ) -> LogTrail:
        logtrail = LogTrail(
            tenant_id=tenant_id,
            log_type=log_type,
            event=event,
        )

        with self.services.persistence.get_session() as session:
            self.logtrail_db.save(session=session, obj=logtrail)

        return logtrail
