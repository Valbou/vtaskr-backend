from logging import getLogger

from src.notifications.services import NotificationService
from src.ports import ObserverPort

logger = getLogger(__name__)


class TasksNotificationsObserver(ObserverPort):
    subscribe_to: list[str] = ["tasks:todo_today:tasks"]

    @classmethod
    def run(cls, app_ctx, event_name: str, event_data: dict):
        service = NotificationService(services=app_ctx.dependencies)

        try:
            messages = service.build_messages(name=event_name, context=event_data)
            service.add_messages(messages=messages)
            service.notify_all()
        except Exception as e:
            logger.error(f"{e}")
