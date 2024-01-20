from flask import Flask
from src.libs.eventbus import EventBusService
from src.libs.flask.main import create_flask_app
from src.libs.notifications import TestNotificationService
from src.libs.redis.database import TestNoSQLService
from src.libs.sqlalchemy.database import TestSQLService

# Clean cache
nosql_test = TestNoSQLService()
redis = nosql_test.get_engine()
redis.flushdb()

# Clean database
print("Install Tables...")
sql_test = TestSQLService(echo=False)
sql_test.drop_tables()
sql_test.create_tables()

# Set APP
APP: Flask = create_flask_app(
    sql_class=TestSQLService,
    nosql_class=TestNoSQLService,
    notification_class=TestNotificationService,
    eventbus_class=EventBusService,
)

print("All registered routes:")
for rule in APP.url_map.iter_rules():
    print(f"{rule.endpoint:-<30} {rule.rule}")
print(" ----- ")
