from fastapi import APIRouter

from app.services.autonomous_worker import run_planning_cycle


router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


@router.post("/run")
def run_agent():

    run_planning_cycle()

    return {
        "message": "LifeOps planning cycle completed."
    }