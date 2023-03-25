from typing import List, Optional

from sqlalchemy.orm import Session

from vtasks.tasks.hmi.ports import AbstractTaskPort
from vtasks.tasks.persistence import TaskDB
from vtasks.tasks.models import Task


class TaskService(AbstractTaskPort):
    def __init__(self, session: Session, testing: bool = False) -> None:
        self.session: Session = session
        self.task_db = TaskDB()

    def get_user_tasks(self, user_id: str) -> List[dict]:
        return self.task_db.user_tasks(self.session, user_id)

    def get_user_task(self, user_id: str, task_id: str) -> Optional[Task]:
        # TODO: Add a better security
        task = self.task_db.load(self.session, task_id)
        return task if task.user_id == user_id else None
