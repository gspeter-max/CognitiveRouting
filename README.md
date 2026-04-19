# CognitiveRouting

Phase 1 of the Cognitive Routing assignment: a local persona router that embeds three fixed bot personas, stores them in ChromaDB, and routes incoming posts to matching bots by cosine similarity.

## What is included

- Persona definitions for the three Phase 1 bots
- SentenceTransformer-based embeddings with `BAAI/bge-small-en-v1.5`
- ChromaDB collection setup and persistence
- Deterministic routing with a configurable similarity threshold
- A small console demo
- Tests for embeddings, storage, and routing

## Project layout

- `src/cognitive_routing/personas.py`
- `src/cognitive_routing/embeddings.py`
- `src/cognitive_routing/store.py`
- `src/cognitive_routing/router.py`
- `src/cognitive_routing/demo_phase1.py`

## Run locally

1. Create an environment and install dependencies.
2. Run the demo:

```bash
python -m cognitive_routing.demo_phase1
```

## Run tests

```bash
pytest -q
```

## Docker

The repository includes a `Dockerfile` for the Python app and a `docker-compose.yml` that runs ChromaDB only.
