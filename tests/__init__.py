from dotenv import load_dotenv

from vtasks.sqlalchemy.database import SQLService

from .base_test import BaseTestCase, FlaskTemplateCapture


load_dotenv()

# Clean database
print("Install Tables...")
sql_test = SQLService(testing=True, echo=False)
sql_test.drop_tables()
sql_test.create_tables()

# Set fixtures
