"""End-to-end pipeline that connects Phase 1 routing to Phase 2 content generation."""

from __future__ import annotations

from typing import Any

from cognitive_routing.config import DEFAULT_THRESHOLD
from cognitive_routing.content_engine.graph import generate_original_post
from cognitive_routing.routing.personas import Persona, load_personas
from cognitive_routing.routing.router import route_post_to_bots
from cognitive_routing.routing.store import get_chroma_client, get_persona_collection, seed_personas


def run_full_pipeline(
    post_content: str,
    *,
    routing_threshold: float = DEFAULT_THRESHOLD,
    chroma_client: Any | None = None,
    mistral_client: Any | None = None,
) -> dict[str, Any]:
    """Run the full Phase 1 -> Phase 2 pipeline for one incoming post.

    The pipeline keeps each phase independent:

    1. Phase 1 selects the best matching persona for ``post_content``.
    2. Phase 2 generates the final structured post for that selected persona.

    The highest-ranked Phase 1 match is used as the single handoff into Phase 2.
    """

    personas = load_personas()
    resolved_chroma_client = chroma_client or get_chroma_client()
    collection = get_persona_collection(resolved_chroma_client)
    seed_personas(collection, personas)

    matches = route_post_to_bots(collection, post_content, threshold=routing_threshold)
    if not matches:
        raise ValueError("Phase 1 did not find a persona match for the provided post.")

    selected_match = matches[0]
    selected_persona = _get_persona_by_id(personas, selected_match["bot_id"])
    generated_post = generate_original_post(
        selected_persona.bot_id,
        selected_persona.description,
        client=mistral_client,
    )

    return {
        "input_post": post_content,
        "selected_bot": {
            "bot_id": selected_persona.bot_id,
            "bot_name": selected_persona.bot_name,
            "persona": selected_persona.description,
            "similarity": selected_match["similarity"],
        },
        "routing_matches": matches,
        "generated_post": generated_post,
    }


def _get_persona_by_id(personas: list[Persona], bot_id: str) -> Persona:
    """Return the canonical persona record for one routed bot id."""

    for persona in personas:
        if persona.bot_id == bot_id:
            return persona
    raise ValueError(f"Phase 1 selected unknown bot_id: {bot_id}")
