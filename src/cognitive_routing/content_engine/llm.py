"""Mistral SDK integration for the Phase 2 content engine."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

from cognitive_routing.config import (
    CONTENT_POST_CHAR_LIMIT,
    DEFAULT_MISTRAL_MODEL,
    DEFAULT_POST_TEMPERATURE,
    DEFAULT_TOPIC_TEMPERATURE,
    MISTRAL_API_KEY_ENV,
)
from cognitive_routing.content_engine.models import GeneratedPost, SearchDecision

if TYPE_CHECKING:
    from mistralai import Mistral
else:
    Mistral = Any


def build_mistral_client(api_key: str | None = None) -> Mistral:
    """Build the official Mistral client from an explicit or environment API key."""

    resolved_key = api_key or os.getenv(MISTRAL_API_KEY_ENV)
    if not resolved_key:
        raise ValueError(f"{MISTRAL_API_KEY_ENV} is required for Phase 2 content generation.")

    from mistralai import Mistral as MistralClient

    return MistralClient(api_key=resolved_key)


def decide_search_for_persona(client: Mistral, bot_id: str, persona: str) -> SearchDecision:
    """Select one topical angle and one search query for the persona."""

    response = client.chat.parse(
        model=DEFAULT_MISTRAL_MODEL,
        response_format=SearchDecision,
        temperature=DEFAULT_TOPIC_TEMPERATURE,
        messages=[
            {
                "role": "system",
                "content": (
                    "Select one current topic for a social bot persona. "
                    "Return only structured fields for topic and search_query."
                ),
            },
            {
                "role": "user",
                "content": f"bot_id={bot_id}\npersona={persona}",
            },
        ],
    )
    return response.choices[0].message.parsed


def draft_post_from_context(
    client: Mistral,
    bot_id: str,
    persona: str,
    topic: str,
    search_results: str,
) -> GeneratedPost:
    """Draft the final structured social post from persona and mock-search context."""

    response = client.chat.parse(
        model=DEFAULT_MISTRAL_MODEL,
        response_format=GeneratedPost,
        temperature=DEFAULT_POST_TEMPERATURE,
        messages=[
            {
                "role": "system",
                "content": (
                    "Write one opinionated social post in the provided persona. "
                    f"Keep post_content under {CONTENT_POST_CHAR_LIMIT} characters."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"bot_id={bot_id}\n"
                    f"persona={persona}\n"
                    f"topic={topic}\n"
                    f"search_results={search_results}"
                ),
            },
        ],
    )
    return response.choices[0].message.parsed
