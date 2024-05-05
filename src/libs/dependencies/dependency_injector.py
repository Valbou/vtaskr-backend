from enum import Enum

from src.ports import (
    CachePort,
    EventBusPort,
    IdentityAccessManagementPort,
    InjectablePort,
    NotificationPort,
    PersistencePort,
    TranslationPort,
)


class DependencyType(Enum):
    CACHE = "cache"
    EVENTBUS = "eventbus"
    IDENTITY = "identity"
    NOTIFICATION = "notification"
    PERSISTENCE = "persistence"
    TRANSLATION = "translation"


class DependencyInjector:
    cache: CachePort
    eventbus: EventBusPort
    identity: IdentityAccessManagementPort
    notification: NotificationPort
    persistence: PersistencePort
    translation: TranslationPort

    def add_dependency(
        self, dep: DependencyType, dep_class: type[InjectablePort], **dep_kwargs
    ):
        setattr(self, f"{dep.value}_class", dep_class)
        setattr(self, f"{dep.value}_kwargs", dep_kwargs)

    def instantiate_dependencies(self) -> None:
        for dep in DependencyType:
            dep_class = getattr(self, f"{dep.value}_class", False)
            dep_kwargs = getattr(self, f"{dep.value}_kwargs", {})
            if dep_class:
                setattr(self, dep.value, dep_class(**dep_kwargs))

    def set_context(self, **ctx):
        for dep in DependencyType:
            dep_instance: InjectablePort = getattr(self, dep.value, False)
            if dep_instance:
                dep_instance.set_context(**ctx)
