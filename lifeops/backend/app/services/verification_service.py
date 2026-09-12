from sqlalchemy.orm import Session

from app.models import Task


VALID_SOURCES = [
    "USER_CONFIRMATION",
    "EXTERNAL_CONFIRMATION",
]


def verify_task(
    db: Session,
    task: Task,
    evidence: str,
    source: str
) -> Task:

    # ---------------------------------------
    # Safety checks
    # ---------------------------------------

    if task.status == "REJECTED":
        raise ValueError(
            "Rejected tasks cannot be completed."
        )

    if task.status == "COMPLETED":
        raise ValueError(
            "Task is already completed."
        )

    if not evidence.strip():
        raise ValueError(
            "Completion evidence is required."
        )

    source = source.upper()

    if source not in VALID_SOURCES:
        raise ValueError(
            "Invalid completion source."
        )

    # ---------------------------------------
    # COMPLETE USER OBJECTIVE
    # ---------------------------------------

    task.status = "COMPLETED"

    task.completion_source = source

    db.commit()
    db.refresh(task)

    return task