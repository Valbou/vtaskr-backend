from abc import ABC, abstractmethod
from typing import List


class AbstractTaskPort(ABC):
    @abstractmethod
    def get_user_tasks(self, user_id: str) -> List[dict]:
        raise NotImplementedError()
