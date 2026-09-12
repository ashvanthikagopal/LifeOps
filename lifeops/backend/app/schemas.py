from datetime import datetime

from pydantic import BaseModel


class EventCreate(BaseModel):
    user_id: int
    source: str
    title: str
    content: str
    event_time: datetime | None = None


class EventResponse(BaseModel):
    id: int
    user_id: int
    source: str
    title: str
    content: str
    processed: bool

    class Config:
        from_attributes = True


class TaskResponse(BaseModel):
    id: int
    user_id: int
    event_id: int | None

    title: str
    description: str | None

    # User objective
    status: str

    # Risk
    risk_level: str

    # LifeOps decision
    action_type: str | None

    # Approval
    approval_status: str

    # LifeOps action
    action_status: str

    # Verification
    completion_source: str | None

    deadline: datetime | None
    progress: int
    category: str
    priority: str
    next_action: str | None
    remaining_work: str | None
    last_reasoning: str | None
    action_name: str | None

    class Config:
        from_attributes = True



class VerifyTaskRequest(BaseModel):
    evidence: str
    source: str