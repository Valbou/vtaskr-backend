from flask import Flask
from src.libs.babel.translations import TranslationService
from src.libs.dependencies import DependencyInjector, DependencyType
from src.libs.iam.config import PermissionControl
from src.libs.redis.database import CacheService
from src.libs.sqlalchemy.database import SQLService
from src.events.services import EventBusService
from src.notifications.services import NotificationService

from .libs.flask import create_flask_app

di = DependencyInjector()
di.add_dependency(DependencyType.PERSISTENCE, SQLService)
di.add_dependency(DependencyType.CACHE, CacheService)
di.add_dependency(DependencyType.EVENTBUS, EventBusService)
di.add_dependency(DependencyType.IDENTITY, PermissionControl)
di.add_dependency(DependencyType.NOTIFICATION, NotificationService)
di.add_dependency(DependencyType.TRANSLATION, TranslationService)

app: Flask = create_flask_app(dependencies=di)
