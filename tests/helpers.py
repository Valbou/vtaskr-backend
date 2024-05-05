from src.events.services import EventBusService
from src.libs.babel.translations import TranslationService
from src.libs.dependencies import DependencyInjector, DependencyType
from src.libs.iam.config import PermissionControl
from src.libs.redis.database import TestCacheService
from src.libs.sqlalchemy.database import DummyPersistenceService, TestPersistenceService
from src.notifications.services import TestNotificationService


def get_test_di() -> DependencyInjector:
    di = DependencyInjector()
    di.add_dependency(DependencyType.PERSISTENCE, TestPersistenceService, echo=False)
    di.add_dependency(DependencyType.CACHE, TestCacheService)
    di.add_dependency(DependencyType.EVENTBUS, EventBusService)
    di.add_dependency(DependencyType.IDENTITY, PermissionControl)
    di.add_dependency(DependencyType.NOTIFICATION, TestNotificationService)
    di.add_dependency(DependencyType.TRANSLATION, TranslationService)

    di.instantiate_dependencies()
    return di


def get_dummy_di() -> DependencyInjector:
    di = DependencyInjector()
    di.add_dependency(DependencyType.PERSISTENCE, DummyPersistenceService, echo=False)
    di.add_dependency(DependencyType.CACHE, TestCacheService)
    di.add_dependency(DependencyType.EVENTBUS, EventBusService)
    di.add_dependency(DependencyType.IDENTITY, PermissionControl)
    di.add_dependency(DependencyType.NOTIFICATION, TestNotificationService)
    di.add_dependency(DependencyType.TRANSLATION, TranslationService)

    di.instantiate_dependencies()
    return di
