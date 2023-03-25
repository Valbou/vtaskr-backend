from abc import ABC, abstractmethod
from typing import Optional, Tuple

from vtasks.users import User


class AbstractUserPort(ABC):
    @abstractmethod
    def register(self, data: dict) -> User:
        raise NotImplementedError()

    @abstractmethod
    def authenticate(
        self, email: str, password: str
    ) -> Tuple[Optional[str], Optional[User]]:
        raise NotImplementedError()

    @abstractmethod
    def logout(self, email: str, sha_token: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def user_from_token(self, sha_token: str) -> Optional[User]:
        raise NotImplementedError()
