from uuid import uuid4
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


@dataclass
class User:
    id: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    hash_password: str = ""
    created_at: datetime = datetime.now()
    last_login_at: Optional[datetime] = None

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        hash_password: str,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        last_login_at: Optional[datetime] = None,
    ) -> None:
        self.id = id or uuid4().hex
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        if hash_password:
            self.hash_password = hash_password
        self.created_at = created_at or datetime.now()
        self.last_login_at = last_login_at

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def set_password(self, password):
        ph = PasswordHasher()
        self.hash_password = ph.hash(password)

    def check_password(self, password):
        ph = PasswordHasher()
        try:
            return ph.verify(self.hash_password, password)
        except VerifyMismatchError:
            return False

    def __str__(self) -> str:
        return self.full_name

    def __repr__(self):
        return f"<User {self.full_name!r}>"
