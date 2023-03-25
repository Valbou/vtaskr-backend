from abc import ABC, abstractmethod
from typing import Optional, Tuple

from vtaskr.users import User


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

    @abstractmethod
    def request_password_change(self, user: User) -> str:
        raise NotImplementedError()

    @abstractmethod
    def request_email_change(self, user: User, new_email: str) -> Tuple[str, str]:
        raise NotImplementedError()

    @abstractmethod
    def set_new_password(self, email: str, hash: str, password: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def set_new_email(
        self, old_email: str, new_email: str, hash: str, code: str
    ) -> bool:
        raise NotImplementedError()
