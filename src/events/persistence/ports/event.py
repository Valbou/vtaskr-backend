from abc import ABC

from src.libs.sqlalchemy.default_port import AbstractPort


class AbstractEventPort(AbstractPort, ABC):
    pass
