from abc import ABC, abstractmethod

from src.notifications.models import Template
from src.ports import AbstractDBPort


class TemplateDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def update(self, template: Template) -> bool:
        raise NotImplementedError()
