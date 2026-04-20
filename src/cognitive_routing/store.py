"""ChromaDB persistence and query helpers for persona routing."""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlparse
from typing import Any

import chromadb

from cognitive_routing.config import CHROMA_COLLECTION_NAME, CHROMA_PERSIST_DIR
from cognitive_routing.embeddings import embed_text
from cognitive_routing.personas import Persona


def get_chroma_client(path: str = CHROMA_PERSIST_DIR) -> Any:
    """Return a Chroma client backed by HTTP or local persistence.

    If ``CHROMA_HOST`` is set, the app connects to a remote Chroma server.
    Otherwise it falls back to a local on-disk PersistentClient.
    """

    chroma_host = os.getenv("CHROMA_HOST")
    if chroma_host:
        parsed = urlparse(chroma_host)
        host = parsed.hostname or "localhost"
        port = parsed.port or 8000
        ssl = parsed.scheme == "https"
        return chromadb.HttpClient(host=host, port=port, ssl=ssl)

    persist_path = Path(path)
    persist_path.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(persist_path))


def get_persona_collection(client: Any) -> Any:
    """Create or open the router's collection using cosine distance."""

    return client.get_or_create_collection(
        name=CHROMA_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def seed_personas(collection: Any, personas: list[Persona]) -> None:
    """Upsert all personas into Chroma using persona descriptions as documents."""

    if not personas:
        return

    ids = [persona.bot_id for persona in personas]
    documents = [persona.description for persona in personas]
    embeddings = [embed_text(persona.description) for persona in personas]
    metadatas = [
        {"bot_name": persona.bot_name, "tags": ",".join(persona.tags)}
        for persona in personas
    ]
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def query_personas(collection: Any, query_embedding: list[float], top_k: int = 3) -> dict[str, Any]:
    """Query the persona collection for the closest matches to one embedding."""

    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
