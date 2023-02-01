from datetime import datetime
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import Column, Integer, String, DateTime

from vtasks.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    pseudo = Column(String(120), unique=False)
    email = Column(String(250), unique=True)
    password = Column(String(100))
    created_at = Column(DateTime, default=datetime.now())
    last_login_at = Column(DateTime, nullable=True, default=None)

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
