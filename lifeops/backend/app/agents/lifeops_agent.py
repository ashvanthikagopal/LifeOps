from app.agents.mock_lifeops_agent import analyze_event as analyze_mock
from app.config import settings


def analyze_event(
    source: str,
    title: str,
    content: str,
    db=None,
    user_id: int | None = None,
) -> dict:

    if settings.AGENT_PROVIDER.lower() == "mock":

        return analyze_mock(
            source=source,
            title=title,
            content=content,
        )

    if settings.AGENT_PROVIDER.lower() == "strands":

        if db is None:
            raise ValueError(
                "Database session is required for the Strands agent."
            )

        if user_id is None:
            raise ValueError(
                "user_id is required for the Strands agent."
            )

        from app.agents.strands_lifeops_agent import analyze_with_strands

        return analyze_with_strands(
            source=source,
            title=title,
            content=content,
            db=db,
            user_id=user_id,
        )

    raise ValueError(
        f"Unsupported AGENT_PROVIDER: {settings.AGENT_PROVIDER}"
    )