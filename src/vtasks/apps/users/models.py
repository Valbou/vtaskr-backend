from datetime import datetime
from typing import Optional

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.vtasks.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(25))
    last_name: Mapped[str] = mapped_column(String(25))
    email: Mapped[str] = mapped_column(String(250), unique=True)
    password: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    last_login_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def set_password(self, password):
        ph = PasswordHasher()
        self.password = ph.hash(password)

    def check_password(self, password):
        ph = PasswordHasher()
        try:
            return ph.verify(hash, password)
        except VerifyMismatchError:
            return False

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"<User {self.name!r}>"
