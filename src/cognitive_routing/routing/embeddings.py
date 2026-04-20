"""Embedding helpers for Phase 1 persona routing."""

from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

from cognitive_routing.config import MODEL_NAME


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """Load and cache the SentenceTransformer model once per process."""

    return SentenceTransformer(MODEL_NAME)


def _to_list(vector: np.ndarray | list[float]) -> list[float]:
    """Convert NumPy arrays or Python sequences into plain float lists."""

    if isinstance(vector, np.ndarray):
        return vector.tolist()
    return list(vector)


def embed_text(text: str) -> list[float]:
    """Embed one piece of text as a normalized vector."""

    model = get_embedding_model()
    vector = model.encode(
        text,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )
    return _to_list(vector)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed many texts in one batch while preserving input order."""

    if not texts:
        return []

    model = get_embedding_model()
    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )
    if isinstance(vectors, np.ndarray):
        return vectors.tolist()
    return [list(vector) for vector in vectors]
