from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task
from app.schemas import VerifyTaskRequest
from app.services.action_executor import execute_task
from app.services.verification_service import verify_task


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# =====================================================
# GET ALL TASKS
# =====================================================

@router.get("/")
def get_tasks(
    db: Session = Depends(get_db)
):

    tasks = (
        db.query(Task)
        .order_by(Task.created_at.desc())
        .all()
    )

    return tasks


# =====================================================
# GET SINGLE TASK
# =====================================================

@router.get("/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# =====================================================
# APPROVE
# =====================================================

@router.post("/{task_id}/approve")
def approve_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.status == "COMPLETED":

        raise HTTPException(
            status_code=400,
            detail="Completed task cannot be approved."
        )

    if task.status == "REJECTED":

        raise HTTPException(
            status_code=400,
            detail="Rejected task cannot be approved."
        )

    if task.action_type != "ASK_USER":

        raise HTTPException(
            status_code=400,
            detail="This task does not require approval."
        )

    task.approval_status = "APPROVED"

    db.commit()

    db.refresh(task)

    return {
        "task_id": task.id,
        "task_status": task.status,
        "approval_status": task.approval_status,
        "message": "Task approved. It is NOT completed yet."
    }


# =====================================================
# REJECT
# =====================================================

@router.post("/{task_id}/reject")
def reject_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.status == "COMPLETED":

        raise HTTPException(
            status_code=400,
            detail="Completed task cannot be rejected."
        )

    task.approval_status = "REJECTED"

    task.status = "REJECTED"

    db.commit()

    db.refresh(task)

    return {
        "task_id": task.id,
        "task_status": task.status,
        "approval_status": task.approval_status,
        "message": "Task rejected."
    }


# =====================================================
# EXECUTE
# =====================================================

@router.post("/{task_id}/execute")
def execute_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # ---------------------------------------
    # NEVER execute rejected task
    # ---------------------------------------

    if task.status == "REJECTED":

        raise HTTPException(
            status_code=403,
            detail="Rejected tasks cannot be executed."
        )

    # ---------------------------------------
    # Already completed
    # ---------------------------------------

    if task.status == "COMPLETED":

        raise HTTPException(
            status_code=400,
            detail="Task has already been completed."
        )

    # ---------------------------------------
    # WAIT
    # ---------------------------------------

    if task.action_type == "WAIT":

        raise HTTPException(
            status_code=400,
            detail="This task is currently waiting."
        )

    # ---------------------------------------
    # ASK USER
    # ---------------------------------------

    if task.action_type == "ASK_USER":

        if task.approval_status != "APPROVED":

            raise HTTPException(
                status_code=403,
                detail=(
                    "User approval is required. "
                    f"Current approval status: "
                    f"{task.approval_status}"
                )
            )

    # ---------------------------------------
    # Execute
    # ---------------------------------------

    try:

        action = execute_task(
            db=db,
            task=task
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return {
        "task_id": task.id,

        "task_status": task.status,

        "approval_status": task.approval_status,

        "action_status": task.action_status,

        "action_id": action.id,

        "result": action.result,

        "message": (
            "LifeOps action completed. "
            "The user task is still pending "
            "until completion is verified."
        )
    }


# =====================================================
# VERIFY COMPLETION
# =====================================================

@router.post("/{task_id}/verify")
def verify_task_endpoint(
    task_id: int,
    payload: VerifyTaskRequest,
    db: Session = Depends(get_db)
):

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    try:

        task = verify_task(
            db=db,
            task=task,
            evidence=payload.evidence,
            source=payload.source
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return {
        "task_id": task.id,

        "task_status": task.status,

        "approval_status": task.approval_status,

        "action_status": task.action_status,

        "completion_source": (
            task.completion_source
        ),

        "message": (
            "User task has been verified "
            "and marked as completed."
        )
    }