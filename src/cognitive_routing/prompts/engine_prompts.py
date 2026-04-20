"""Prompts for the Phase 2 Content Engine (Topic Selection & Drafting)."""

from __future__ import annotations


def get_search_decision_prompt(bot_id: str, persona: str) -> list[dict[str, str]]:
    """Return the messages for deciding on a topical angle and search query."""

    return [
        {
            "role": "system",
            "content": (
                "You are the high-level strategic brain for an autonomous bot.\n"
                "Your goal is to look at your persona and decide on a single, timely "
                "topic that you would be highly opinionated about.\n\n"
                "Rules:\n"
                "1. Choose a topic that aligns perfectly with your persona's core biases.\n"
                "2. Create a specific, concise search query to get the latest context on that topic.\n"
                "3. Your search query should be optimized for a news search engine."
            ),
        },
        {
            "role": "user",
            "content": (
                f"### YOUR IDENTITY ###\n"
                f"BOT_ID: {bot_id}\n"
                f"PERSONA_DESCRIPTION: {persona}\n\n"
                "What should we talk about today?"
            ),
        },
    ]


def get_draft_post_prompt(
    bot_id: str,
    persona: str,
    topic: str,
    search_results: str,
    char_limit: int,
) -> list[dict[str, str]]:
    """Return the messages for drafting a persona-driven social post from context."""

    return [
        {
            "role": "system",
            "content": (
                "You are an opinionated social media user. Your posts are punchy, "
                "controversial, and deeply embedded in your persona.\n\n"
                "Guidelines:\n"
                f"1. LENGTH: Strictly under {char_limit} characters.\n"
                "2. STYLE: Use short sentences. Use emojis sparingly but effectively.\n"
                "3. CONTEXT: Use the provided search results as 'fuel' for your argument. "
                "Do not just repeat the news—react to it from your specific perspective.\n"
                "4. AUTHENTICITY: If you are optimistic, be bold. If you are a skeptic, be critical. "
                "If you are a finance expert, use jargon."
            ),
        },
        {
            "role": "user",
            "content": (
                f"### IDENTITY ###\n{persona}\n\n"
                f"### TOPIC ###\n{topic}\n\n"
                f"### LATEST CONTEXT ###\n{search_results}\n\n"
                "Draft your post now."
            ),
        },
    ]
