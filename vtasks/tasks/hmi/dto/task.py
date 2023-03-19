from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Optional

from vtasks.tasks.models import Task


@dataclass
class TaskDTO:
    id: str = ""
    created_at: str = ""
    title: str = ""
    description: str = ""
    emergency: bool = False
    important: bool = False
    scheduled_at: Optional[str] = None
    duration: str = ""
    done: bool = False


class TaskMapperDTO:
    @classmethod
    def model_to_dto(cls, task: Task) -> TaskDTO:
        return TaskDTO(
            id=task.id,
            created_at=task.created_at.isoformat(),
            title=task.title,
            description=task.description,
            emergency=task.emergency,
            important=task.important,
            scheduled_at=task.scheduled_at.isoformat() if task.scheduled_at else None,
            duration=task.duration.total_seconds() if task.duration else None,
            done=task.done,
        )

    @classmethod
    def dto_to_model(cls, task_dto: TaskDTO, task: Task) -> Task:
        if task_dto.title:
            task.title = task_dto.title
        if task_dto.description:
            task.description = task_dto.description
        if task_dto.emergency:
            task.emergency = task_dto.emergency
        if task_dto.important:
            task.important = task_dto.important
        if task_dto.scheduled_at:
            task.scheduled_at = (
                datetime.fromisoformat(task_dto.scheduled_at)
                if task_dto.scheduled_at
                else None
            )
        if task_dto.duration:
            task.duration = (
                timedelta(seconds=int(task_dto.duration)) if task_dto.duration else None
            )
        if task_dto.done:
            task.done = task_dto.done
        return task

    @classmethod
    def dto_to_dict(cls, task_dto: TaskDTO) -> dict:
        return asdict(task_dto)
