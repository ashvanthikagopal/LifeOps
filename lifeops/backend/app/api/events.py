from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Event
from app.schemas import EventCreate
from app.services.task_service import process_event


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.post("/")
def create_event(
    payload: EventCreate,
    db: Session = Depends(get_db)
):

    event = Event(
        user_id=payload.user_id,
        source=payload.source,
        title=payload.title,
        content=payload.content,
        event_time=payload.event_time,
    )

    db.add(event)

    db.commit()

    db.refresh(event)

    task = process_event(
        db=db,
        event=event
    )

    return {
        "event_id": event.id,
        "task_id": task.id if task else None,
        "message": "Event processed successfully",
    }