from sqlalchemy.orm import Session

from app.models import Action, Task
from app.services.action_registry import get_action


def execute_task(db: Session, task: Task) -> Action:

    # ---------------------------------------------------------
    # STATE VALIDATION
    # ---------------------------------------------------------

    if task.status == "REJECTED":
        raise ValueError(
            "Rejected tasks cannot be executed."
        )

    if task.status == "COMPLETED":
        raise ValueError(
            "Task has already been completed."
        )

    if task.action_type == "WAIT":
        raise ValueError(
            "This task is currently waiting."
        )

    if task.action_type == "ASK_USER":

        if task.approval_status != "APPROVED":
            raise ValueError(
                "User approval is required."
            )

    if task.action_type == "AUTO":

        if task.approval_status not in [
            "NOT_REQUIRED",
            "APPROVED",
        ]:
            raise ValueError(
                "AUTO task cannot be executed with "
                "the current approval status."
            )

    # ---------------------------------------------------------
    # ACTION VALIDATION
    # ---------------------------------------------------------

    if not task.action_name:
        raise ValueError(
            "No action has been assigned to this task."
        )

    action_definition = get_action(
        task.action_name
    )

    if not action_definition:
        raise ValueError(
            f"Unknown action: {task.action_name}"
        )

    # ---------------------------------------------------------
    # SAFETY CHECK
    # ---------------------------------------------------------

    if (
        action_definition.risk_level == "HIGH"
        and task.approval_status != "APPROVED"
    ):
        raise ValueError(
            "High-risk action requires user approval."
        )

    # ---------------------------------------------------------
    # START EXECUTION
    # ---------------------------------------------------------

    task.action_status = "EXECUTING"

    action = Action(
        task_id=task.id,
        action_type=task.action_name,
        status="EXECUTING",
        result=None,
    )

    db.add(action)
    db.commit()
    db.refresh(action)

    try:

        # -----------------------------------------------------
        # ACTUAL REGISTERED ACTION
        # -----------------------------------------------------

        result = action_definition.handler(task)

        action.status = "COMPLETED"
        action.result = str(result)

        # IMPORTANT:
        #
        # Do NOT mark the user objective completed.
        #
        task.action_status = "COMPLETED"

        db.commit()
        db.refresh(action)

        return action

    except Exception as error:

        action.status = "FAILED"
        action.result = str(error)

        task.action_status = "FAILED"

        db.commit()
        db.refresh(action)

        raise