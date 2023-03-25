from dotenv import load_dotenv

from src.vtasks.database import SQLService, DBType

from .apps import *
from .base_test import *


load_dotenv()

# Clean database
print("Install Tables...")
sql_test = SQLService(database=DBType.TEST, echo=False)
sql_test.drop_tables()
sql_test.create_tables()

# Set fixtures

# Define flask app context
