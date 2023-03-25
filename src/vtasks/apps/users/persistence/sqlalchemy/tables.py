from datetime import datetime

from sqlalchemy.orm import registry
from sqlalchemy import Table, Column, String, DateTime

from src.vtasks.apps.users.models import User


mapper_registry = registry()

user_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("first_name", String(25)),
    Column("last_name", String(25)),
    Column("email", String(250), unique=True),
    Column("hash_password", String(256)),
    Column("created_at", DateTime, default=datetime.now()),
    Column("last_login_at", DateTime, nullable=True, default=None),
)

mapper_registry.map_imperatively(
    User,
    user_table,
)
