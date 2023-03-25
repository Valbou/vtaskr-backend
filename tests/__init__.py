from dotenv import load_dotenv

from vtasks.sqlalchemy.database import SQLService
from vtasks.redis.database import NoSQLService

from .base_test import BaseTestCase, FlaskTemplateCapture


load_dotenv()

# Clean cache
nosql_test = NoSQLService(testing=True)
redis = nosql_test.get_engine()
redis.flushdb()

# Clean database
print("Install Tables...")
sql_test = SQLService(testing=True, echo=False)
sql_test.drop_tables()
sql_test.create_tables()

# Set fixtures
