from abc import ABC, abstractmethod

from src.libs.sqlalchemy.default_port import AbstractPort
from src.notifications.models import Template


class AbstractTemplatePort(AbstractPort, ABC):
    @abstractmethod
    def update(self, template: Template) -> bool:
        raise NotImplementedError()
