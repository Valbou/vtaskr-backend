from abc import ABC, abstractmethod
from enum import Enum
from typing import ContextManager

from .base_port import InjectablePort


class IdentityAccessManagementPort(InjectablePort, ABC):
    @abstractmethod
    def get_resources(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def can(
        self,
        session: ContextManager,
        permission: Enum,
        user_id: str,
        group_id_resource: str,
        resource: str,
        exception: bool = True,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def all_tenants_with_access(
        session: ContextManager,
        permission: Enum,
        user_id: str,
        resource: str,
    ) -> list[str]:
        raise NotImplementedError
