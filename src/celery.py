from celery import Celery
from src.events.services import EventBusService
from src.libs.babel.translations import TranslationService
from src.libs.dependencies import DependencyInjector, DependencyType
from src.libs.iam.config import PermissionControl
from src.libs.redis.database import CacheService
from src.libs.sqlalchemy.database import PersistenceService

from .libs.celery import create_celery_app

di = DependencyInjector()
di.add_dependency(DependencyType.PERSISTENCE, PersistenceService)
di.add_dependency(DependencyType.CACHE, CacheService)
di.add_dependency(DependencyType.EVENTBUS, EventBusService)
di.add_dependency(DependencyType.IDENTITY, PermissionControl)
di.add_dependency(DependencyType.TRANSLATION, TranslationService)

app: Celery = create_celery_app(dependencies=di)
