from datetime import datetime

from sqlalchemy.orm import Session

from app.agents.lifeops_agent import analyze_event
from app.models import Event, Task
from app.services.action_executor import execute_task
from app.services.decision_engine import determine_action


def process_event(
    db: Session,
    event: Event
) -> Task | None:

    # ---------------------------------------
    # AGENT ANALYSIS
    # ---------------------------------------

    result = analyze_event(
    source=event.source,
    title=event.title,
    content=event.content,
    db=db,
    user_id=event.user_id,
)

    # ---------------------------------------
    # NOTHING ACTIONABLE
    # ---------------------------------------

    if not result.get("has_task", False):

        event.processed = True

        db.commit()

        return None

    # ---------------------------------------
    # Extract result
    # ---------------------------------------

    title = result.get(
        "title",
        event.title
    )

    description = result.get(
        "description",
        event.content
    )

    risk_level = result.get(
        "risk_level",
        "LOW"
    )

    suggested_action = result.get(
        "suggested_action",
        "ASK_USER"
    )

    # ---------------------------------------
    # Deadline
    # ---------------------------------------

    deadline = None

    deadline_string = result.get(
        "deadline"
    )

    if deadline_string:

        try:

            deadline = datetime.fromisoformat(
                deadline_string
            )

        except ValueError:

            deadline = None

    # ---------------------------------------
    # SAFETY DECISION
    # ---------------------------------------

    action_type = determine_action(
        title=title,
        description=description,
        risk_level=risk_level,
        suggested_action=suggested_action,
    )

    # ---------------------------------------
    # APPROVAL STATE
    # ---------------------------------------

    if action_type == "ASK_USER":

        approval_status = "PENDING"

    else:

        approval_status = "NOT_REQUIRED"

    # ---------------------------------------
    # TASK STATE
    # ---------------------------------------

    if action_type == "WAIT":

        task_status = "PENDING"

    else:

        task_status = "PENDING"

    # ---------------------------------------
    # CREATE TASK
    # ---------------------------------------

    task = Task(
        user_id=event.user_id,
        event_id=event.id,
        title=title,
        description=description,

        status=task_status,

        risk_level=risk_level,

        action_type=action_type,

        approval_status=approval_status,

        action_status="NOT_STARTED",

        completion_source=None,

        deadline=deadline,
    )

    db.add(task)

    event.processed = True

    db.commit()

    db.refresh(task)

    # ---------------------------------------
    # AUTO EXECUTION
    # ---------------------------------------

    if task.action_type == "AUTO":

        try:

            execute_task(
                db=db,
                task=task
            )

        except ValueError:

            db.refresh(task)

    return task