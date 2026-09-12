import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.events import router as events_router
from app.api.tasks import router as tasks_router
from app.database import Base, engine
from app.services.autonomous_worker import autonomous_worker
from app.api.agent import router as agent_router


Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):

    worker_task = asyncio.create_task(
        autonomous_worker()
    )

    print("LifeOps autonomous worker started.")

    yield

    worker_task.cancel()

    try:
        await worker_task
    except asyncio.CancelledError:
        print("LifeOps autonomous worker stopped.")


app = FastAPI(
    title="LifeOps API",
    description="Autonomous Personal Operations Agent",
    version="0.4.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(events_router)
app.include_router(tasks_router)
app.include_router(agent_router)

@app.get("/")
def root():
    return {
        "application": "LifeOps",
        "status": "running",
        "version": "0.4.0",
        "autonomous_worker": True,
    }