from dotenv import load_dotenv

from vtasks.sqlalchemy.database import SQLService, DBType
from vtasks.flask.main import create_flask_app

from .base_db_test import *


load_dotenv()

# Clean database
print("Install Tables...")
sql_test = SQLService(database=DBType.TEST, echo=False)
sql_test.drop_tables()
sql_test.create_tables()

# Set fixtures
