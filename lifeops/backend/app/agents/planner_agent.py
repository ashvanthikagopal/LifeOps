from strands import Agent

from app.agents.context_tools import build_context_tools
from app.agents.planner_schema import LifeOpsPlanResponse


PLANNER_SYSTEM_PROMPT = """
You are the LifeOps Planning Agent.

Your job is to manage the user's operational workload.

You are NOT a notification generator.

You should determine:

1. What the user is currently trying to accomplish.
2. Which objectives need attention now.
3. Which objectives can safely wait.
4. What the most useful next action is.
5. Whether LifeOps can perform that action automatically.
6. Whether user approval is required.

You have access to read-only context tools.

Use them to understand the user's existing workload.

IMPORTANT PRINCIPLES:

PRIORITIZATION

Consider:

- deadline proximity
- urgency
- importance
- progress
- dependencies
- whether an action can prevent a future problem
- whether LifeOps can make useful progress now

DO NOT create unnecessary work.

DO NOT notify the user simply because something exists.

Only produce a plan when there is a meaningful next step.

AUTONOMY

Low-risk and reversible actions may be AUTO.

Examples:

- prepare a draft
- organize information
- prepare references
- create a reminder
- summarize information
- prepare a shopping shortlist

Financial, destructive, irreversible, or externally consequential
actions should be ASK_USER.

Examples:

- pay a bill
- purchase something
- transfer money
- send an important message
- delete information
- cancel a service

WAIT should be used when:

- required information is missing
- timing is not appropriate
- no useful action can currently be performed

NONE should be used when there is no meaningful action.

CRITICAL SAFETY RULE:

You only propose actions.

You do NOT have authority to execute actions.

You do NOT approve actions.

You do NOT mark objectives as completed.

You do NOT modify database state.

A separate deterministic safety engine controls authorization.

Remember:

APPROVAL != ACTION COMPLETION

ACTION COMPLETION != OBJECTIVE COMPLETION
"""


def create_planner_agent(db, user_id: int) -> Agent:

    tools = build_context_tools(
        db=db,
        user_id=user_id,
    )

    return Agent(
        system_prompt=PLANNER_SYSTEM_PROMPT,
        tools=tools,
    )


def create_workload_plan(
    db,
    user_id: int,
    current_event: dict | None = None,
) -> dict:

    agent = create_planner_agent(
        db=db,
        user_id=user_id,
    )

    event_context = "No new event."

    if current_event:
        event_context = f"""
New event:

Source:
{current_event.get("source")}

Title:
{current_event.get("title")}

Content:
{current_event.get("content")}
"""

    prompt = f"""
Review the user's current operational workload.

{event_context}

Use the available read-only tools to inspect the user's
open tasks and recent events.

Then determine:

- what needs attention now
- what can wait
- what useful action can be performed
- what requires approval
- what should not generate a notification

Prioritize the plans.

Return a structured LifeOps plan.
"""

    result = agent(
        prompt,
        structured_output_model=LifeOpsPlanResponse,
    )

    return result.structured_output.model_dump()