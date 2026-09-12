from datetime import datetime, timedelta


def analyze_event(
    source: str,
    title: str,
    content: str
) -> dict:

    text = f"{title} {content}".lower()

    # ---------------------------------------
    # HIGH RISK / FINANCIAL
    # ---------------------------------------

    financial_keywords = [
        "bill",
        "payment",
        "pay",
        "purchase",
        "buy",
        "transfer",
        "money",
        "₹",
        "rs ",
        "rupee",
    ]

    if any(keyword in text for keyword in financial_keywords):

        deadline = None

        if "tomorrow" in text:
            deadline = (
                datetime.now() + timedelta(days=1)
            ).replace(
                hour=23,
                minute=59,
                second=0,
                microsecond=0
            )

        return {
            "has_task": True,
            "title": title,
            "description": content,
            "deadline": (
                deadline.isoformat()
                if deadline
                else None
            ),
            "risk_level": "HIGH",
            "suggested_action": "ASK_USER",
        }

    # ---------------------------------------
    # MEDIUM RISK
    # ---------------------------------------

    appointment_keywords = [
        "appointment",
        "doctor",
        "meeting",
        "interview",
    ]

    if any(
        keyword in text
        for keyword in appointment_keywords
    ):

        deadline = None

        if "tomorrow" in text:
            deadline = (
                datetime.now() + timedelta(days=1)
            )

        return {
            "has_task": True,
            "title": title,
            "description": content,
            "deadline": (
                deadline.isoformat()
                if deadline
                else None
            ),
            "risk_level": "MEDIUM",
            "suggested_action": "ASK_USER",
        }

    # ---------------------------------------
    # LOW RISK
    # ---------------------------------------

    reminder_keywords = [
        "deadline",
        "due",
        "submit",
        "presentation",
        "assignment",
        "reminder",
    ]

    if any(
        keyword in text
        for keyword in reminder_keywords
    ):

        deadline = None

        if "tomorrow" in text:
            deadline = (
                datetime.now() + timedelta(days=1)
            )

        return {
            "has_task": True,
            "title": title,
            "description": content,
            "deadline": (
                deadline.isoformat()
                if deadline
                else None
            ),
            "risk_level": "LOW",
            "suggested_action": "AUTO",
        }

    # ---------------------------------------
    # NOTHING ACTIONABLE
    # ---------------------------------------

    return {
        "has_task": False,
        "title": None,
        "description": None,
        "deadline": None,
        "risk_level": "LOW",
        "suggested_action": "IGNORE",
    }