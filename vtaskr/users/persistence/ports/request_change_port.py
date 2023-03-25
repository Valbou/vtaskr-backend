from abc import ABC, abstractmethod

from vtaskr.base.persistence import AbstractPort


class AbstractRequestChangePort(AbstractPort, ABC):
    @abstractmethod
    def clean_history(self):
        raise NotImplementedError

    @abstractmethod
    def find_request(self):
        raise NotImplementedError
