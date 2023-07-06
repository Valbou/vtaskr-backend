from flask import Flask

from vtaskr.libs.flask.main import create_flask_app
from vtaskr.libs.notifications import TestNotificationService
from vtaskr.libs.redis.database import TestNoSQLService
from vtaskr.libs.sqlalchemy.database import TestSQLService

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
)
