from app.config import settings


def generate_workload_plan(
    db,
    user_id: int,
    current_event: dict | None = None,
) -> dict:

    if settings.AGENT_PROVIDER.lower() == "strands":

        from app.agents.planner_agent import create_workload_plan

        return create_workload_plan(
            db=db,
            user_id=user_id,
            current_event=current_event,
        )

    if settings.AGENT_PROVIDER.lower() == "mock":

        return generate_mock_plan(
            db=db,
            user_id=user_id,
            current_event=current_event,
        )

    raise ValueError(
        f"Unsupported AGENT_PROVIDER: {settings.AGENT_PROVIDER}"
    )


def generate_mock_plan(
    db,
    user_id: int,
    current_event: dict | None = None,
) -> dict:

    from datetime import datetime

    from app.models import Task

    tasks = (
        db.query(Task)
        .filter(
            Task.user_id == user_id,
            Task.status == "PENDING",
        )
        .order_by(Task.deadline.asc())
        .all()
    )

    plans = []

    now = datetime.now()

    for task in tasks:

        # Ignore tasks whose action has already been completed,
        # unless the task is still waiting for user approval.
        if (
            task.action_status == "COMPLETED"
            and task.approval_status != "PENDING"
        ):
            continue

        # -----------------------------------------------------
        # PRIORITY
        # -----------------------------------------------------

        priority = task.priority or "MEDIUM"

        if task.deadline:

            time_remaining = task.deadline - now

            if time_remaining.total_seconds() <= 86400:
                priority = "CRITICAL"

            elif time_remaining.total_seconds() <= 172800:
                priority = "HIGH"

        # -----------------------------------------------------
        # NEXT ACTION
        # -----------------------------------------------------

        next_action = task.next_action

        if not next_action:

            if task.remaining_work:
                next_action = task.remaining_work

            else:
                next_action = task.title

        # -----------------------------------------------------
        # ACTION MODE
        # -----------------------------------------------------

        if task.action_type == "ASK_USER":

            action = "ASK_USER"

        elif task.action_type == "AUTO":

            action = "AUTO"

        elif task.action_type == "WAIT":

            action = "WAIT"

        else:

            action = "NONE"

        # -----------------------------------------------------
        # REASONING
        # -----------------------------------------------------

        reasons = []

        if task.progress > 0:

            reasons.append(
                f"Progress is {task.progress}%"
            )

        if task.remaining_work:

            reasons.append(
                f"Remaining work: {task.remaining_work}"
            )

        if task.deadline:

            reasons.append(
                "The deadline is approaching"
            )

        if not reasons:

            reasons.append(
                "Task is still pending"
            )

        reason = ". ".join(reasons) + "."

        # -----------------------------------------------------
        # CREATE PLAN
        # -----------------------------------------------------

        plans.append(
            {
                "task_id": task.id,
                "goal": task.title,
                "priority": priority,
                "reason": reason,
                "next_action": next_action,

                # Step 9:
                # Tell the planner/executor exactly what
                # registered capability should be used.
                "action": action,
                "action_name": task.action_name,
            }
        )

    # ---------------------------------------------------------
    # SORT BY PRIORITY
    # ---------------------------------------------------------

    priority_order = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3,
    }

    plans.sort(
        key=lambda plan: priority_order.get(
            plan["priority"],
            99,
        )
    )

    return {
        "plans": plans,
    }