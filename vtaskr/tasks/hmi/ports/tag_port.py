from abc import ABC, abstractmethod
from typing import List


class AbstractTagPort(ABC):
    @abstractmethod
    def get_user_tags(self, user_id: str) -> List[dict]:
        raise NotImplementedError()
