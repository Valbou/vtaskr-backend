from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from src.libs.dependencies import DependencyInjector
from src.libs.hmi.querystring import Filter
from src.libs.utils import split_by
from src.tasks.events import TasksEventManager
from src.tasks.managers import TagManager, TaskManager
from src.tasks.models import Tag, Task


class TasksService:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services

        self._define_managers()

    def _define_managers(self):
        """Define managers from domain (no DI here)"""

        self.event_manager = TasksEventManager()
        self.tag_manager = TagManager(services=self.services)
        self.task_manager = TaskManager(services=self.services)

    def create_new_task(self, user_id: str, task: Task) -> bool:
        """Create a new task for a user"""

        with self.services.persistence.get_session() as session:
            return self.task_manager.create_task(
                session=session, user_id=user_id, task=task
            )

    def get_user_task(self, user_id: str, task_id: str):
        """Return a user's task"""

        with self.services.persistence.get_session() as session:
            return self.task_manager.get_task(
                session=session, user_id=user_id, task_id=task_id
            )

    def get_user_all_tasks(self, user_id: str, qs_filters: list[Filter] | None = None):
        """Return all user's tasks"""

        with self.services.persistence.get_session() as session:
            tasks = self.task_manager.get_tasks(
                session=session, user_id=user_id, qs_filters=qs_filters
            )

        return tasks

    def get_all_tag_tasks(
        self, user_id: str, tag_id: str, qs_filters: list[Filter] | None = None
    ) -> list[Tag]:
        """Return all tasks with this at least this tag"""

        with self.services.persistence.get_session() as session:
            return self.task_manager.get_tag_tasks(
                session=session, user_id=user_id, tag_id=tag_id, qs_filters=qs_filters
            )

    def update_task(self, user_id: str, task: Task) -> bool:
        """Update a task"""

        with self.services.persistence.get_session() as session:
            return self.task_manager.update_task(
                session=session, user_id=user_id, task=task
            )

    def delete_task(self, user_id: str, task: Task) -> bool:
        """Delete a task"""

        with self.services.persistence.get_session() as session:
            return self.task_manager.delete_task(
                session=session, user_id=user_id, task=task
            )

    def create_new_tag(self, user_id: str, tag: Tag) -> bool:
        """Create a new tag for a user"""

        with self.services.persistence.get_session() as session:
            return self.tag_manager.create_tag(session=session, user_id=user_id, tag=tag)

    def get_user_tag(self, user_id: str, tag_id: str) -> Tag | None:
        """Return a user's tag"""

        with self.services.persistence.get_session() as session:
            return self.tag_manager.get_tag(
                session=session, user_id=user_id, tag_id=tag_id
            )

    def check_user_tag_exists(self, user_id: str, tag_id: str) -> bool:
        """Check if user's tag exists"""

        with self.services.persistence.get_session() as session:
            return self.tag_manager.tags_exists(
                session=session, user_id=user_id, tag_ids=[tag_id]
            )

    def get_all_task_tags(self, user_id: str, task_id: str) -> list[Tag]:
        with self.services.persistence.get_session() as session:
            return self.tag_manager.get_task_tags(
                session=session, user_id=user_id, task_id=task_id
            )

    def get_tags_from_id(self, user_id: str, tag_ids: list[str]) -> list[Tag]:
        with self.services.persistence.get_session() as session:
            return self.tag_manager.get_tags_from_ids(
                session=session, user_id=user_id, tag_ids=tag_ids
            )

    def get_user_all_tags(
        self, user_id: str, qs_filters: list[Filter] | None = None
    ) -> list[Tag]:
        """Return all user's tags"""

        with self.services.persistence.get_session() as session:
            tags = self.tag_manager.get_tags(
                session=session, user_id=user_id, qs_filters=qs_filters
            )

        return tags

    def update_tag(self, user_id: str, tag: Tag) -> bool:
        """Update a tag"""

        with self.services.persistence.get_session() as session:
            return self.tag_manager.update_tag(session=session, user_id=user_id, tag=tag)

    def delete_tag(self, user_id: str, tag: Tag) -> bool:
        """Delete a tag"""

        with self.services.persistence.get_session() as session:
            return self.tag_manager.delete_tag(session=session, user_id=user_id, tag=tag)

    def set_tags_to_task(self, user_id: str, task_id: str, tag_ids: list[str]) -> bool:
        """Set tags to a task"""

        with self.services.persistence.get_session() as session:
            task = self.task_manager.get_task(user_id=user_id, task_id=task_id)

            if not task:
                return False

            if tag_ids:
                tags = self.get_tags_from_id(user_id=user_id, tag_ids=tag_ids)

                if tags:
                    tags = self.tag_manager.get_tags(session=session, user_id=user_id)
                    task.tags = tags

            elif len(tag_ids) == 0:
                task.tags = []

            self.task_manager.update_task(session=session, user_id=user_id, task=task)

            return True

    def clean_all_items_of_tenant(self, tenant_id: str) -> None:
        """
        Clean all data associated with the tenant_id.

        This function must stay behind a permission control
        or an event sent after permission check.
        """

        with self.services.persistence.get_session() as session:
            self.task_manager.delete_all_tenant_tasks(
                session=session, tenant_id=tenant_id
            )
            self.tag_manager.delete_all_tenant_tags(session=session, tenant_id=tenant_id)

    def _add_tasks_dict_to_index(self, index: dict, tasks: list[Task]) -> None:
        for task in tasks:
            if index[task.assigned_to] is None:
                index[task.assigned_to] = []

            index[task.assigned_to].append(
                {
                    "title": task.title,
                    "emergency": task.emergency,
                    "important": task.important,
                    "scheduled_at": task.scheduled_at.isoformat(),
                    "duration": task.duration.total_seconds() // 60,
                }
            )

    def notify_tasks_to_assigned(
        self, ids: list[str], now: datetime, end_day_1: datetime, end_day_2: datetime
    ) -> None:
        """Send events with today and tomorrow tasks"""

        with self.services.persistence.get_session() as session:
            # Build today tasks index
            indexed_today_tasks = dict.fromkeys(ids)
            today_tasks = self.task_manager.get_tasks_assigned_to_and_scheduled_between(
                session=session, ids=ids, start=now, end=end_day_1
            )
            self._add_tasks_dict_to_index(index=indexed_today_tasks, tasks=today_tasks)

            # Build tomorrow tasks index
            indexed_tomorrow_tasks = dict.fromkeys(ids)
            tomorrow_tasks = (
                self.task_manager.get_tasks_assigned_to_and_scheduled_between(
                    session=session, ids=ids, start=end_day_1, end=end_day_2
                )
            )
            self._add_tasks_dict_to_index(
                index=indexed_tomorrow_tasks, tasks=tomorrow_tasks
            )

            # Send notifications
            for assigned_to_id in ids:
                with self.services.eventbus as event_session:
                    self.event_manager.send_tasks_todo_today_event(
                        session=event_session,
                        assigned_to=assigned_to_id,
                        today_tasks=indexed_today_tasks[assigned_to_id],
                        tomorrow_tasks=indexed_tomorrow_tasks[assigned_to_id],
                    )

    def send_today_tasks_notifications(
        self, assigned_to: str | None = None, split_size: int = 100
    ) -> None:
        """
        Send tasks scheduled in next 48h to all users by default

        Update with caution to avoid data leak between users !
        """

        DAY = 24

        now = datetime.now(tz=ZoneInfo("UTC"))
        end_day_1 = now + timedelta(hours=DAY)
        end_day_2 = end_day_1 + timedelta(hours=DAY)

        # Look for all unique assigned_to id in tasks scheduled in next 48h
        with self.services.persistence.get_session() as session:
            assigned_ids = self.task_manager.all_assigned_to_for_scheduled_between(
                session=session, start=now, end=end_day_2
            )

        # Split assigned by split_size to limit database access and memory consumption
        for ids in split_by(iterable=assigned_ids, size=split_size):
            self.notify_tasks_to_assigned(
                ids=ids, now=now, end_day_1=end_day_1, end_day_2=end_day_2
            )
