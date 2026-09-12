import asyncio
import logging

from app.config import settings
from app.database import SessionLocal
from app.models import Task
from app.services.action_executor import execute_task
from app.services.planner_service import generate_workload_plan


logger = logging.getLogger("lifeops.worker")


def run_planning_cycle():
    """
    Run one autonomous LifeOps planning cycle.

    The worker:
    1. Finds users with pending tasks.
    2. Runs the planner for each user.
    3. Updates task reasoning and next action.
    4. Automatically executes safe AUTO actions.
    5. Leaves ASK_USER actions waiting for approval.
    """

    db = SessionLocal()

    try:

        user_ids = (
            db.query(Task.user_id)
            .filter(Task.status == "PENDING")
            .distinct()
            .all()
        )

        if not user_ids:
            logger.info(
                "LifeOps worker: no pending tasks."
            )
            return

        for (user_id,) in user_ids:

            logger.info(
                "LifeOps worker: planning for user %s",
                user_id,
            )

            try:

                plan = generate_workload_plan(
                    db=db,
                    user_id=user_id,
                )

                plans = plan.get("plans", [])

                for item in plans:

                    task_id = item.get("task_id")

                    if task_id is None:
                        continue

                    task = (
                        db.query(Task)
                        .filter(
                            Task.id == task_id,
                            Task.user_id == user_id,
                        )
                        .first()
                    )

                    if not task:
                        continue

                    if task.status != "PENDING":
                        continue

                    # Save the planner's current reasoning.
                    task.priority = item.get(
                        "priority",
                        task.priority or "MEDIUM",
                    )

                    task.next_action = item.get(
                        "next_action"
                    )
                    task.action_name = item.get(
                        "action_name",
                    task.action_name,
                    )

                    task.last_reasoning = item.get(
                        "reason"
                    )

                    db.commit()
                    db.refresh(task)

                    action = item.get("action")

                    logger.info(
                        "Task %s: priority=%s action=%s",
                        task.id,
                        task.priority,
                        action,
                    )

                    # -------------------------------------------------
                    # AUTO
                    # -------------------------------------------------

                    if action == "AUTO":

                        # Never execute the same completed action again.
                        if task.action_status == "COMPLETED":
                            logger.info(
                                "Task %s already has a completed action. "
                                "Skipping.",
                                task.id,
                            )
                            continue

                        try:

                            execute_task(
                                db=db,
                                task=task,
                            )

                            logger.info(
                                "Task %s AUTO action completed.",
                                task.id,
                            )

                        except Exception as error:

                            logger.exception(
                                "Task %s AUTO action failed: %s",
                                task.id,
                                error,
                            )

                    # -------------------------------------------------
                    # ASK USER
                    # -------------------------------------------------

                    elif action == "ASK_USER":

                        logger.info(
                            "Task %s requires user approval.",
                            task.id,
                        )

                    # -------------------------------------------------
                    # WAIT
                    # -------------------------------------------------

                    elif action == "WAIT":

                        logger.info(
                            "Task %s is waiting.",
                            task.id,
                        )

            except Exception as error:

                logger.exception(
                    "Planning failed for user %s: %s",
                    user_id,
                    error,
                )

    finally:

        db.close()


async def autonomous_worker():

    interval = settings.LIFEOPS_WORKER_INTERVAL_SECONDS

    logger.info(
        "LifeOps autonomous worker started. "
        "Interval: %s seconds",
        interval,
    )

    while True:

        try:

            await asyncio.to_thread(
                run_planning_cycle
            )

        except Exception as error:

            logger.exception(
                "Autonomous worker error: %s",
                error,
            )

        await asyncio.sleep(interval)