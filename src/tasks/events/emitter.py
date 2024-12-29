from src.ports import EventBusPort


class TasksEventManager:
    def send_tasks_todo_today_event(
        self,
        session: EventBusPort,
        assigned_to: str,
        today_tasks: list[dict],
        tomorrow_tasks: list[dict],
    ) -> dict:
        session.emit(
            tenant_id=assigned_to,
            event_name="tasks:todo_today:tasks",
            event_data={
                "targets": [assigned_to],
                "user_id": assigned_to,
                "today": today_tasks,
                "nb_today": len(today_tasks),
                "tomorrow": tomorrow_tasks,
                "nb_tomorrow": len(tomorrow_tasks),
            },
        )
