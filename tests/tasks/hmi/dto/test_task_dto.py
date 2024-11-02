from datetime import datetime, timedelta
from unittest import TestCase

from src.tasks.hmi.dto import Task, TaskDTO, TaskMapperDTO


class TaskMapperTest(TestCase):
    def test_mapper_model_to_dto(self):
        task = Task(
            title="My new task",
            tenant_id="abc123",
            description="My task description",
            emergency=False,
            important=True,
            scheduled_at=datetime.now(),
            duration=timedelta(seconds=12_345),
            assigned_to="user_123",
        )

        task_dto = TaskMapperDTO.model_to_dto(task=task)

        self.assertIsInstance(task_dto, TaskDTO)

    def test_mapper_dto_to_model(self):
        task_dto = TaskDTO(
            tenant_id="abc123",
            title="My new task",
            description="My task description",
            emergency=True,
            important=False,
            scheduled_at="2024-10-22T11:02:42Z",
            duration="2:00",
            assigned_to="user_123",
        )

        task = TaskMapperDTO.dto_to_model(task_dto=task_dto)

        self.assertIsInstance(task, Task)
