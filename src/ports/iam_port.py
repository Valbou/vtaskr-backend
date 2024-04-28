from abc import ABC, abstractmethod

from .base_port import InjectablePort


class IdentityAccessManagementPort(InjectablePort, ABC):
    @abstractmethod
    def can(self, permission, tenant_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def all_tenants_with_access(self, permission, tenant_id: str) -> bool:
        raise NotImplementedError
