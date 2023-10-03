from abc import ABC, abstractmethod
from typing import Optional

from vtaskr.tasks.models import Task


class AbstractTaskPort(ABC):
    @abstractmethod
    def get_user_tasks(self, user_id: str) -> list[dict]:
        raise NotImplementedError()

    def get_user_task(self, user_id: str, task_id: str) -> Optional[Task]:
        raise NotImplementedError()

    def get_user_tag_tasks(self, user_id: str, tag_id: str) -> list[Task]:
        raise NotImplementedError()

    def update_user_task(self, user_id: str, task: Task):
        raise NotImplementedError()

    def delete_user_task(self, user_id: str, task: Task):
        raise NotImplementedError()
