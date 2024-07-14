from abc import ABC, abstractmethod

from src.ports import AbstractDBPort
from src.users.models import Invitation


class InvitationDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def clean_expired(self, session):
        raise NotImplementedError()

    @abstractmethod
    def get_from_hash(self, session, hash: str) -> Invitation | None:
        raise NotImplementedError()

    @abstractmethod
    def get_from_group(self, session, group_id: str) -> list[Invitation]:
        raise NotImplementedError()
