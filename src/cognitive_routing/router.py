"""Routing logic that maps posts to matching personas."""

from __future__ import annotations

from typing import Any

from cognitive_routing.config import DEFAULT_THRESHOLD
from cognitive_routing.embeddings import embed_text
from cognitive_routing.store import query_personas


def route_post_to_bots(collection: Any, post_content: str, threshold: float = DEFAULT_THRESHOLD) -> list[dict[str, Any]]:
    """Return the personas whose cosine similarity clears ``threshold``."""

    query_embedding = embed_text(post_content)
    result = query_personas(collection, query_embedding, top_k=3)

    matches: list[dict[str, Any]] = []
    ids = _first_result_row(result.get("ids"))
    distances = _first_result_row(result.get("distances"))
    metadatas = _first_result_row(result.get("metadatas"))

    for index, bot_id in enumerate(ids):
        distance = distances[index]
        # Chroma returns cosine distance; similarity is the inverse score.
        similarity = 1.0 - distance
        print(f"distance: {distance} | bot_id: {bot_id} | metadatas: {metadatas[index]} | similarity: {similarity} | threshold: {threshold}")
        if similarity < threshold:
            continue

        metadata = metadatas[index] or {}
        matches.append(
            {
                "bot_id": bot_id,
                "bot_name": metadata.get("bot_name", bot_id),
                "similarity": round(float(similarity), 4),
            }
        )

    return matches


def _first_result_row(value: Any) -> list[Any]:
    """Safely unwrap the first row from a Chroma query response field."""

    if not value:
        return []
    first_row = value[0]
    if first_row is None:
        return []
    return list(first_row)
