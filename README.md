# CognitiveRouting

CognitiveRouting now contains two clearly separated slices:

- Phase 1 routing: match incoming posts to fixed personas by embedding similarity.
- Phase 2 content engine: generate an original bot post through a small LangGraph workflow with strict JSON output.

## Repository Structure

The source tree is organized by responsibility so a new developer can find the
correct entry point without scanning every file.

```text
src/cognitive_routing/
├── config.py
├── routing/
│   ├── personas.py
│   ├── embeddings.py
│   ├── store.py
│   └── router.py
├── content_engine/
│   ├── models.py
│   ├── tools.py
│   ├── llm.py
│   └── graph.py
├── demos/
│   ├── phase1.py
│   └── phase2.py
├── demo_phase1.py
├── demo_phase2.py
```

## Phase 1: Persona Routing

Phase 1 embeds three canonical personas with `BAAI/bge-small-en-v1.5`, stores
them in ChromaDB, and routes a new post to the best matching bots using cosine
similarity.

Main modules:

- `cognitive_routing.routing.personas`
- `cognitive_routing.routing.embeddings`
- `cognitive_routing.routing.store`
- `cognitive_routing.routing.router`

Demo:

```bash
python -m cognitive_routing.demos.phase1
```

## Phase 2: Autonomous Content Engine

Phase 2 adds a readable three-step LangGraph workflow that creates an original
bot post:

1. `decide_search`
   The Mistral client selects a topic and a search query for the persona.
2. `web_search`
   The mocked `mock_searxng_search` tool returns one deterministic headline.
3. `draft_post`
   The Mistral client generates the final post as strict structured output.

Public JSON shape:

```json
{
  "bot_id": "bot_a",
  "topic": "AI jobs",
  "post_content": "Opinionated post under 280 characters"
}
```

Main modules:

- `cognitive_routing.content_engine.models`
- `cognitive_routing.content_engine.tools`
- `cognitive_routing.content_engine.llm`
- `cognitive_routing.content_engine.graph`

Demo:

```bash
python -m cognitive_routing.demos.phase2
```

## Environment

Required for Phase 2:

- `MISTRAL_API_KEY`
- `MISTRAL_MODEL` optional, defaults to `mistral-small-latest`

Reference template:

- `.env.example`

## Review Notes

- Public functions and packages use short docstrings for high readability.
- The only Mistral integration lives in `content_engine/llm.py`.
- The graph state and schema boundaries are centralized in `content_engine/models.py`.
- The mock-search behavior is deterministic and isolated in `content_engine/tools.py`.
- The repository now uses only the package paths under `routing/`,
  `content_engine/`, and `demos/`.

## Verification

You said you will run verification in your own environment, so no further local
test execution is claimed in this repository state.

Suggested commands in your environment:

```bash
pytest -q
python -m cognitive_routing.demos.phase1
python -m cognitive_routing.demos.phase2
```
