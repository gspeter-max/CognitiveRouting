"""Phase 1 routing package."""

from cognitive_routing.routing.embeddings import embed_text, embed_texts, get_embedding_model
from cognitive_routing.routing.personas import Persona, load_personas
from cognitive_routing.routing.router import route_post_to_bots
from cognitive_routing.routing.store import get_chroma_client, get_persona_collection, query_personas, seed_personas

__all__ = [
    "Persona",
    "embed_text",
    "embed_texts",
    "get_embedding_model",
    "get_chroma_client",
    "get_persona_collection",
    "load_personas",
    "query_personas",
    "route_post_to_bots",
    "seed_personas",
]
