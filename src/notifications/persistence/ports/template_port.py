from abc import ABC, abstractmethod

from src.notifications.models import MessageType, Template
from src.ports import AbstractDBPort


class TemplateDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def update(self, session, template: Template) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_template_for_event(
        self, session, event_name: str, event_type: MessageType
    ) -> Template | None:
        raise NotImplementedError()
