from app.database import SessionLocal
from app.services.planner_service import generate_workload_plan


db = SessionLocal()

try:

    plan = generate_workload_plan(
        db=db,
        user_id=1,
    )

    print("\nLIFEOPS WORKLOAD PLAN")
    print("=====================")

    for item in plan["plans"]:

        print(f"\nTask: {item['goal']}")
        print(f"Priority: {item['priority']}")
        print(f"Reason: {item['reason']}")
        print(f"Next action: {item['next_action']}")
        print(f"Action: {item['action']}")

finally:

    db.close()