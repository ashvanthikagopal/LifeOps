from dataclasses import dataclass
from typing import Callable


@dataclass
class ActionDefinition:
    name: str
    description: str
    risk_level: str
    handler: Callable


def prepare_references(task):
    """
    Simulate preparing references for an assignment.
    """

    return {
        "success": True,
        "message": (
            f"LifeOps prepared the remaining references "
            f"for '{task.title}'."
        ),
        "output": [
            "Reference list prepared",
            "Sources organized",
            "References ready for review",
        ],
    }


def create_birthday_draft(task):
    """
    Prepare a birthday message draft.
    """

    return {
        "success": True,
        "message": (
            f"LifeOps prepared a birthday message "
            f"for '{task.title}'."
        ),
        "draft": (
            "Happy Birthday! 🎉 "
            "Wishing you an amazing year ahead!"
        ),
    }


def create_reminder(task):
    """
    Create a reminder for the user.
    """

    return {
        "success": True,
        "message": (
            f"LifeOps created a reminder for '{task.title}'."
        ),
    }


def pay_electricity_bill(task):
    """
    Simulated payment action.

    IMPORTANT:
    This does NOT perform a real payment.
    A real payment integration will be added later
    and must pass through the safety engine.
    """

    return {
        "success": True,
        "message": (
            "Simulated electricity bill payment "
            "prepared successfully."
        ),
        "requires_real_integration": True,
    }


ACTION_REGISTRY = {

    "PREPARE_REFERENCES": ActionDefinition(
        name="PREPARE_REFERENCES",
        description="Prepare references for an assignment.",
        risk_level="LOW",
        handler=prepare_references,
    ),

    "DRAFT_BIRTHDAY_MESSAGE": ActionDefinition(
        name="DRAFT_BIRTHDAY_MESSAGE",
        description="Prepare a birthday message draft.",
        risk_level="LOW",
        handler=create_birthday_draft,
    ),

    "CREATE_REMINDER": ActionDefinition(
        name="CREATE_REMINDER",
        description="Create a reminder.",
        risk_level="LOW",
        handler=create_reminder,
    ),

    "PAY_ELECTRICITY_BILL": ActionDefinition(
        name="PAY_ELECTRICITY_BILL",
        description="Pay an electricity bill.",
        risk_level="HIGH",
        handler=pay_electricity_bill,
    ),
}


def get_action(action_name: str) -> ActionDefinition | None:

    return ACTION_REGISTRY.get(
        action_name.upper()
    )