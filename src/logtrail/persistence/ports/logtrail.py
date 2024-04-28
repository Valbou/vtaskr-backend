from abc import ABC

from src.libs.sqlalchemy.default_port import AbstractPort


class AbstractLogTrailPort(AbstractPort, ABC):
    pass
