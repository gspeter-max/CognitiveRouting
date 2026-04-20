"""Deterministic tools used by the Phase 2 content engine."""

from langchain_core.tools import tool


SEARCH_HEADLINES = {
    "ai": "OpenAI releases a new coding-focused model as AI automation pressure grows.",
    "crypto": "Bitcoin hits a new high as ETF momentum and regulatory approvals reshape markets.",
    "space": "Private launch providers expand reusable rocket capacity amid renewed lunar competition.",
    "privacy": "Privacy regulators push new restrictions on large-scale consumer data collection.",
    "markets": "Treasury yields and rate-cut expectations dominate market positioning this week.",
}


@tool
def mock_searxng_search(query: str) -> str:
    """Return one deterministic mock headline based on simple keyword matching."""

    normalized_query = query.lower()
    for keyword, headline in SEARCH_HEADLINES.items():
        if keyword in normalized_query:
            return headline
    return "No recent matching headlines found for the provided query."
