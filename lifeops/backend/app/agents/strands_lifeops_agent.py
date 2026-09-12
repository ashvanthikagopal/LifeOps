from strands import Agent

from app.agents.agent_schema import LifeOpsDecision
from app.agents.context_tools import build_context_tools
from app.config import settings
from app.database import SessionLocal


SYSTEM_PROMPT = """
You are LifeOps, an autonomous personal operations agent.

Your purpose is to manage the user's routine operational workload.

You should not behave like a simple notification system.

Instead:

1. Understand the current event.
2. Look at the user's existing open tasks when useful.
3. Look at recent events when useful.
4. Identify relationships between events and existing tasks.
5. Determine what should happen next.
6. Prefer useful action over unnecessary notification.
7. Only interrupt the user when approval is genuinely required.

SAFETY RULES:

1. Financial actions are HIGH risk.

Examples:
- payments
- purchases
- money transfers
- bills

These should suggest ASK_USER.

2. Destructive or irreversible actions are HIGH risk.

Examples:
- deleting files
- permanently removing data
- cancelling important services

These should suggest ASK_USER.

3. Low-risk organizational work can suggest AUTO.

Examples:
- preparing reminders
- organizing information
- preparing drafts
- preparing references
- summarizing information

4. If an action requires information that is not available,
suggest WAIT instead of guessing.

5. If there is no meaningful task,
return has_task=false and suggested_action=IGNORE.

6. Do not create unnecessary notifications.

7. Do not claim that a user's objective is completed merely
because LifeOps performed an action.

IMPORTANT:

You are a reasoning and planning component.

You DO NOT have authority to:
- approve actions
- reject actions
- complete tasks
- make payments
- send irreversible communications
- modify database state

A deterministic safety engine controls authorization.

The action executor controls actual execution.

Task completion requires verification.

APPROVAL ≠ ACTION COMPLETION ≠ TASK COMPLETION.
"""


def create_strands_agent(db, user_id: int) -> Agent:

    tools = build_context_tools(
        db=db,
        user_id=user_id,
    )

    return Agent(
        system_prompt=SYSTEM_PROMPT,
        tools=tools,
    )


def analyze_with_strands(
    source: str,
    title: str,
    content: str,
    db,
    user_id: int,
) -> dict:

    agent = create_strands_agent(
        db=db,
        user_id=user_id,
    )

    prompt = f"""
Analyze this incoming event as part of the user's
overall operational workload.

CURRENT EVENT

Source:
{source}

Title:
{title}

Content:
{content}

Before making your decision, use your available
read-only context tools when additional context
would improve the decision.

Think about:

- existing open tasks
- deadlines
- recent events
- whether this event is related to an existing task
- whether there is useful work LifeOps can perform
- whether user approval is actually necessary

Return a structured LifeOps decision.
"""

    result = agent(
        prompt,
        structured_output_model=LifeOpsDecision,
    )

    decision = result.structured_output

    return decision.model_dump()