FINANCIAL_KEYWORDS = [
    "payment",
    "pay",
    "bill",
    "purchase",
    "buy",
    "transfer",
    "money",
    "₹",
    "rupee",
    "rs ",
]

DESTRUCTIVE_KEYWORDS = [
    "delete",
    "remove permanently",
    "erase",
]


def determine_action(
    title: str,
    description: str,
    risk_level: str,
    suggested_action: str
) -> str:

    text = f"{title} {description}".lower()

    # ---------------------------------------
    # Financial actions always require approval
    # ---------------------------------------

    for keyword in FINANCIAL_KEYWORDS:

        if keyword in text:
            return "ASK_USER"

    # ---------------------------------------
    # Destructive actions always require approval
    # ---------------------------------------

    for keyword in DESTRUCTIVE_KEYWORDS:

        if keyword in text:
            return "ASK_USER"

    # ---------------------------------------
    # High risk always requires approval
    # ---------------------------------------

    if risk_level.upper() == "HIGH":
        return "ASK_USER"

    # ---------------------------------------
    # Agent suggestion
    # ---------------------------------------

    if suggested_action == "AUTO":
        return "AUTO"

    if suggested_action == "WAIT":
        return "WAIT"

    return "ASK_USER"