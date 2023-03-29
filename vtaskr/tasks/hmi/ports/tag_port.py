from abc import ABC, abstractmethod
from typing import List, Optional

from vtaskr.tasks.models import Tag


class AbstractTagPort(ABC):
    @abstractmethod
    def get_user_tags(self, user_id: str) -> List[dict]:
        raise NotImplementedError()

    @abstractmethod
    def get_user_tag(self, user_id: str, tag_id: str) -> Optional[Tag]:
        raise NotImplementedError()

    @abstractmethod
    def get_user_task_tags(self, user_id: str, task_id: str) -> List[Tag]:
        raise NotImplementedError()

    @abstractmethod
    def update_user_tag(self, user_id: str, tag: Tag):
        raise NotImplementedError()

    @abstractmethod
    def delete_user_tag(self, user_id: str, tag: Tag):
        raise NotImplementedError()
