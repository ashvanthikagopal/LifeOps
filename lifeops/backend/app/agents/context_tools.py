from datetime import datetime
from sqlalchemy.orm import Session

from strands import tool

from app.models import Event, Task


def build_context_tools(db: Session, user_id: int):

    @tool
    def get_open_tasks() -> list[dict]:
        """
        Get the user's currently open tasks.

        Returns tasks that are still pending and have not been rejected.
        This is a read-only tool.
        """

        tasks = (
            db.query(Task)
            .filter(
                Task.user_id == user_id,
                Task.status == "PENDING",
            )
            .order_by(Task.deadline.asc())
            .all()
        )

        return [
    {
        "id": task.id,
        "title": task.title,
        "description": task.description,

        "status": task.status,

        "progress": task.progress,
        "category": task.category,
        "priority": task.priority,

        "remaining_work": task.remaining_work,
        "next_action": task.next_action,

        "risk_level": task.risk_level,
        "action_type": task.action_type,
        "action_name": task.action_name,

        "approval_status": task.approval_status,
        "action_status": task.action_status,

        "deadline": (
            task.deadline.isoformat()
            if task.deadline
            else None
        ),
    }
    for task in tasks
]

    @tool
    def get_recent_events() -> list[dict]:
        """
        Get the user's recent events.

        This is a read-only tool used to understand the user's
        recent activity and context.
        """

        events = (
            db.query(Event)
            .filter(Event.user_id == user_id)
            .order_by(Event.created_at.desc())
            .limit(20)
            .all()
        )

        return [
            {
                "id": event.id,
                "source": event.source,
                "title": event.title,
                "content": event.content,
                "event_time": (
                    event.event_time.isoformat()
                    if event.event_time
                    else None
                ),
                "processed": event.processed,
                "created_at": (
                    event.created_at.isoformat()
                    if event.created_at
                    else None
                ),
            }
            for event in events
        ]

    @tool
    def get_task_details(task_id: int) -> dict:
        """
        Get detailed information about one task.

        This is a read-only tool.
        """

        task = (
            db.query(Task)
            .filter(
                Task.id == task_id,
                Task.user_id == user_id,
            )
            .first()
        )

        if not task:
            return {
                "found": False,
                "message": "Task not found."
            }

        return {
            "found": True,
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "risk_level": task.risk_level,
            "action_type": task.action_type,
            "approval_status": task.approval_status,
            "action_status": task.action_status,
            "completion_source": task.completion_source,
            "deadline": (
                task.deadline.isoformat()
                if task.deadline
                else None
            ),
            "created_at": (
                task.created_at.isoformat()
                if task.created_at
                else None
            ),
        }

    return [
        get_open_tasks,
        get_recent_events,
        get_task_details,
    ]