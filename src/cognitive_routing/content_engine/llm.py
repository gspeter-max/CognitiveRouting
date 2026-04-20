"""Mistral SDK integration for the Phase 2 content engine."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

from cognitive_routing.config import (
    CONTENT_POST_CHAR_LIMIT,
    DEFAULT_MISTRAL_MODEL,
    DEFAULT_POST_TEMPERATURE,
    DEFAULT_TOPIC_TEMPERATURE,
    MISTRAL_API_KEY,
)
from cognitive_routing.content_engine.models import GeneratedPost, SearchDecision

if TYPE_CHECKING:
    from mistralai.client import Mistral
else:
    Mistral = Any


def build_mistral_client(api_key: str | None = None) -> Mistral:
    """Build the official Mistral client from an explicit or environment API key."""

    resolved_key = api_key or MISTRAL_API_KEY
    if not resolved_key:
        raise ValueError("MISTRAL_API_KEY is required for Phase 2 content generation.")

    from mistralai.client import Mistral as MistralClient

    return MistralClient(api_key=resolved_key)


def decide_search_for_persona(client: Mistral, bot_id: str, persona: str) -> SearchDecision:
    """Select one topical angle and one search query for the persona."""

    from cognitive_routing.prompts.engine_prompts import get_search_decision_prompt

    messages = get_search_decision_prompt(bot_id, persona)

    response = client.chat.parse(
        model=DEFAULT_MISTRAL_MODEL,
        response_format=SearchDecision,
        temperature=DEFAULT_TOPIC_TEMPERATURE,
        messages=messages, # type: ignore
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

    from cognitive_routing.prompts.engine_prompts import get_draft_post_prompt

    messages = get_draft_post_prompt(
        bot_id=bot_id,
        persona=persona,
        topic=topic,
        search_results=search_results,
        char_limit=CONTENT_POST_CHAR_LIMIT,
    )

    response = client.chat.parse(
        model=DEFAULT_MISTRAL_MODEL,
        response_format=GeneratedPost,
        temperature=DEFAULT_POST_TEMPERATURE,
        messages=messages, # type: ignore
    )
    return response.choices[0].message.parsed
