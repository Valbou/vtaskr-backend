from src.ports import EventBusPort


class NotificationsEventService:
    def __init__(self, eventbus: EventBusPort):
        self.eventbus = eventbus
