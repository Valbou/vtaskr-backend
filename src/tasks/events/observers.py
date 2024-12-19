from logging import getLogger

from src.ports import ObserverPort
from src.tasks.services import TasksService

logger = getLogger(__name__)


class UsersDeleteTenantObserver(ObserverPort):
    subscribe_to: list[str] = ["users:delete:tenant"]

    @classmethod
    def run(cls, app_ctx, event_name: str, event_data: dict):
        service = TasksService(services=app_ctx.dependencies)

        tenant_id = event_data.get("tenant_id")
        if tenant_id is not None:
            service.clean_all_items_of_tenant(tenant_id=tenant_id)
