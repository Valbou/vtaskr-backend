from dotenv import load_dotenv

from vtasks.sqlalchemy.database import SQLService, DBType

from .base_db_test import *


load_dotenv()

# Clean database
print("Install Tables...")
sql_test = SQLService(database=DBType.TEST, echo=False)
sql_test.drop_tables()
sql_test.create_tables()

# Set fixtures

# Define flask app context
