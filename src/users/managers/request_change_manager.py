from src.libs.dependencies import DependencyInjector
from src.users.models import RequestChange, RequestType
from src.users.persistence import RequestChangeDBPort
from src.users.settings import APP_NAME


class RequestChangeManager:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.request_change_db: RequestChangeDBPort = (
            self.services.persistence.get_repository(APP_NAME, "RequestChange")
        )

    def create_request_change(
        self, email: str, request_type: RequestType
    ) -> RequestChange:
        with self.services.persistence.get_session() as session:
            self.request_change_db.clean_history(session)

            request_change = RequestChange(request_type, email=email)
            self.request_change_db.save(session, request_change)

            session.commit()

        return request_change

    def get_request(self, session, email: str) -> RequestChange | None:
        return self.request_change_db.find_request(session=session, email=email)
