from dataclasses import dataclass
from datetime import datetime, time, timedelta

from src.libs.openapi.base import openapi
from src.libs.utils import time_to_seconds, timedelta_to_time
from src.tasks.models import Task

task_component = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "tenant_id": {"type": "string"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "emergency": {"type": "boolean"},
        "important": {"type": "boolean"},
        "scheduled_at": {"type": "string", "format": "date-time"},
        "duration": {"type": "integer", "format": "int32"},
        "created_at": {"type": "string", "format": "date-time"},
    },
    "required": ["tenant_id", "title"],
}
openapi.register_schemas_components("Task", task_component)


@dataclass
class TaskDTO:
    id: str | None = ""
    created_at: str = ""
    tenant_id: str = ""
    title: str = ""
    description: str = ""
    emergency: bool = False
    important: bool = False
    scheduled_at: str | None = None
    duration: time | None = None
    done: datetime | None = None


class TaskMapperDTO:
    @classmethod
    def model_to_dto(cls, task: Task) -> TaskDTO:
        duration = task.duration if task.duration else None
        if duration:
            duration = timedelta_to_time(to_convert=duration)

        return TaskDTO(
            id=task.id,
            created_at=task.created_at.isoformat(),
            title=task.title,
            description=task.description,
            emergency=task.emergency,
            important=task.important,
            scheduled_at=task.scheduled_at.isoformat() if task.scheduled_at else None,
            duration=duration,
            done=task.done.isoformat() if task.done else None,
        )

    @classmethod
    def dto_to_model(cls, task_dto: TaskDTO, task: Task | None = None) -> Task:
        if not task:
            task = Task(tenant_id=task_dto.tenant_id, title=task_dto.title)

        task.title = task_dto.title
        task.description = task_dto.description
        task.emergency = task_dto.emergency
        task.important = task_dto.important

        if task_dto.scheduled_at:
            task.scheduled_at = datetime.fromisoformat(task_dto.scheduled_at)
        else:
            task.scheduled_at = None

        if task_dto.duration:
            task.duration = timedelta(
                seconds=time_to_seconds(to_convert=task_dto.duration)
            )
        else:
            task.duration = None

        if task_dto.done:
            task.done = datetime.fromisoformat(task_dto.done)
        else:
            task.done = None

        return task
