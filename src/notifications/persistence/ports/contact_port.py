from abc import ABC, abstractmethod

from src.notifications.models import Contact
from src.ports import AbstractDBPort


class ContactDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def update(self, session, contact: Contact) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def load_by_email(self, session, email: str) -> Contact | None:
        raise NotImplementedError()
