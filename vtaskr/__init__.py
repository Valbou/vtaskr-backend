from dotenv import load_dotenv

from vtaskr.libs.notifications import NotificationService
from vtaskr.libs.redis.database import NoSQLService
from vtaskr.libs.sqlalchemy.database import SQLService

from .libs.flask.main import create_flask_app

load_dotenv()

app = create_flask_app(
    sql_class=SQLService,
    nosql_class=NoSQLService,
    notification_class=NotificationService,
)
