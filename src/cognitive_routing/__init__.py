"""Public package exports for the routing and content-engine phases."""

from cognitive_routing.config import (
    CHROMA_COLLECTION_NAME,
    CONTENT_POST_CHAR_LIMIT,
    DEFAULT_MISTRAL_MODEL,
    DEFAULT_THRESHOLD,
    MODEL_NAME,
)
from cognitive_routing.content_engine.graph import generate_original_post
from cognitive_routing.content_engine.models import GeneratedPost, SearchDecision
from cognitive_routing.pipeline.full_pipeline import run_full_pipeline
from cognitive_routing.routing.embeddings import embed_text, embed_texts, get_embedding_model
from cognitive_routing.routing.personas import Persona, load_personas
from cognitive_routing.routing.router import route_post_to_bots
from cognitive_routing.routing.store import get_chroma_client, get_persona_collection, query_personas, seed_personas

__all__ = [
    "CHROMA_COLLECTION_NAME",
    "CONTENT_POST_CHAR_LIMIT",
    "DEFAULT_MISTRAL_MODEL",
    "DEFAULT_THRESHOLD",
    "MODEL_NAME",
    "GeneratedPost",
    "SearchDecision",
    "generate_original_post",
    "run_full_pipeline",
    "Persona",
    "embed_text",
    "embed_texts",
    "get_embedding_model",
    "load_personas",
    "route_post_to_bots",
    "get_chroma_client",
    "get_persona_collection",
    "query_personas",
    "seed_personas",
]
