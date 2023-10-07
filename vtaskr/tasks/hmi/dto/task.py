from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Optional

from vtaskr.libs.openapi.base import openapi
from vtaskr.tasks.models import Task

task_component = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "emergency": {"type": "boolean"},
        "important": {"type": "boolean"},
        "scheduled_at": {"type": "string", "format": "date-time"},
        "duration": {"type": "integer", "format": "int32"},
        "created_at": {"type": "string", "format": "date-time"},
    },
}
openapi.register_schemas_components("Task", task_component)


@dataclass
class TaskDTO:
    id: Optional[str] = ""
    created_at: str = ""
    title: str = ""
    description: str = ""
    emergency: bool = False
    important: bool = False
    scheduled_at: Optional[str] = None
    duration: Optional[int] = None
    done: Optional[datetime] = None


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
            done=task.done.isoformat() if task.done else None,
        )

    @classmethod
    def list_models_to_list_dto(cls, tasks: list[Task] | None) -> list[TaskDTO] | None:
        return [TaskMapperDTO.model_to_dto(t) for t in tasks] if tasks else None

    @classmethod
    def dto_to_model(
        cls, tenant_id: str, task_dto: TaskDTO, task: Optional[Task] = None
    ) -> Task:
        if not task:
            task = Task(tenant_id=tenant_id, title=task_dto.title)

        task.title = task_dto.title
        task.description = task_dto.description
        task.emergency = task_dto.emergency
        task.important = task_dto.important

        if task_dto.scheduled_at is not None:
            task.scheduled_at = datetime.fromisoformat(task_dto.scheduled_at)
        else:
            task.scheduled_at = None

        if task_dto.duration is not None:
            task.duration = timedelta(seconds=task_dto.duration)
        else:
            task.duration = None

        if task_dto.done is not None:
            task.done = datetime.fromisoformat(task_dto.done)
        else:
            task.done = None

        return task

    @classmethod
    def dto_to_dict(cls, task_dto: TaskDTO) -> dict:
        return asdict(task_dto)

    @classmethod
    def list_dto_to_dict(cls, tasks_dto: list[TaskDTO]) -> list[dict]:
        return [asdict(task_dto) for task_dto in tasks_dto]
