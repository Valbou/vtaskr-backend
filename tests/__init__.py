from flask import Flask
from src.libs.babel.translations import TranslationService
from src.libs.dependencies import DependencyInjector, DependencyType
from src.libs.flask import create_flask_app
from src.libs.iam.config import PermissionControl
from src.libs.redis.database import TestCacheService
from src.libs.sqlalchemy.database import TestSQLService
from src.events.services import EventBusService
from src.notifications.services import TestNotificationService

di = DependencyInjector()
di.add_dependency(DependencyType.PERSISTENCE, TestSQLService, echo=False)
di.add_dependency(DependencyType.CACHE, TestCacheService)
di.add_dependency(DependencyType.EVENTBUS, EventBusService)
di.add_dependency(DependencyType.IDENTITY, PermissionControl)
di.add_dependency(DependencyType.NOTIFICATION, TestNotificationService)
di.add_dependency(DependencyType.TRANSLATION, TranslationService)

di.instantiate_dependencies()

# Clean cache
cache = di.cache.get_engine()
cache.flushdb()

# Clean database
print("Install Tables...")
di.persistence.drop_tables()
di.persistence.create_tables()

# Set APP
APP: Flask = create_flask_app(dependencies=di)

print("All registered routes:")
for rule in APP.url_map.iter_rules():
    print(f"{rule.endpoint:-<30} {rule.rule}")
print(" ----- ")
