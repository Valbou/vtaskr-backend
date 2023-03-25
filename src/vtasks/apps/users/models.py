from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import Column, Integer, String

from src.database import Base


ph = PasswordHasher()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    pseudo = Column(String(120), unique=False)
    email = Column(String(250), unique=True)
    password = Column(String(100))

    def set_password(self, password):
        self.password = ph.hash(password)

    def check_password(self, password):
        try:
            return ph.verify(hash, password)
        except VerifyMismatchError:
            return False

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.name!r}>'

