from uuid import uuid4
from hashlib import sha256
from base64 import b64encode

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


def hash_from_password(password: str) -> str:
    ph = PasswordHasher()
    return ph.hash(password)


def check_password(hash: str, password: str) -> bool:
    ph = PasswordHasher()
    try:
        return ph.verify(hash, password)
    except VerifyMismatchError:
        return False


def hash_str(string: str) -> str:
    return sha256(string.encode()).hexdigest()


def get_id() -> str:
    """
    Generate an unique id with a very low level of collision risk
    """
    return uuid4().hex


def get_token() -> str:
    """
    Generate a hash from an unique Token
    """
    return sha256(get_id().encode()).hexdigest()


def get_2FA(length: int = 6) -> str:
    """
    Generate an alphanumeric case sensitive code.
    Hard to brute-force in few minutes with API response time
    """
    return b64encode(get_id().encode()).decode()[:length]


def file_to_base64(file_path_name: str) -> str:
    with open(file_path_name, "rb") as file:
        return b64encode(file.read()).decode()
