from typing import Literal

from pydantic import BaseModel, Field


class LifeOpsPlan(BaseModel):
    task_id: int | None = Field(
        default=None,
        description="Existing task ID if this plan relates to an existing task."
    )

    goal: str = Field(
        description="The user's actual objective."
    )

    priority: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = Field(
        description="Priority of the objective."
    )

    reason: str = Field(
        description="Why LifeOps believes this needs attention now."
    )

    next_action: str = Field(
        description="The most useful next action LifeOps should take."
    )

    action: Literal["AUTO", "ASK_USER", "WAIT", "NONE"] = Field(
        description="How LifeOps should handle the next action."
    )


class LifeOpsPlanResponse(BaseModel):
    plans: list[LifeOpsPlan] = Field(
        description="Prioritized plans for the user's current workload."
    )