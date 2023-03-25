from typing import List

from sqlalchemy.orm import Session

from vtasks.tasks.hmi.ports import AbstractTaskPort
from vtasks.tasks.persistence import TaskDB


class TaskService(AbstractTaskPort):
    def __init__(self, session: Session, testing: bool = False) -> None:
        self.session: Session = session
        self.task_db = TaskDB()

    def get_user_tasks(self, user_id: str) -> List[dict]:
        tasks = self.task_db.user_tasks(self.session, user_id)
        return [t.to_external_data() for t in tasks]
