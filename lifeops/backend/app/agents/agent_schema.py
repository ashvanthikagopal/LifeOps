from typing import Literal

from pydantic import BaseModel, Field


class LifeOpsDecision(BaseModel):
    """
    Structured decision returned by the LifeOps agent.
    """

    has_task: bool = Field(
        description="Whether the event contains an actionable task."
    )

    title: str | None = Field(
        default=None,
        description="Short title of the task."
    )

    description: str | None = Field(
        default=None,
        description="Description of what needs to be done."
    )

    risk_level: Literal[
        "LOW",
        "MEDIUM",
        "HIGH"
    ] = Field(
        description="Estimated risk level."
    )

    suggested_action: Literal[
        "AUTO",
        "ASK_USER",
        "WAIT",
        "IGNORE"
    ] = Field(
        description="Suggested LifeOps action."
    )

    reason: str = Field(
        description="Short explanation for the decision."
    )