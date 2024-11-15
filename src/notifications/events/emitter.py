from src.ports import EventBusPort


class NotificationsEventManger:
    def send_(self, session: EventBusPort, tenant_id: str, **kwargs) -> None:

        session.emit(
            tenant_id=tenant_id, event_name="notification:", event_data={**kwargs}
        )
