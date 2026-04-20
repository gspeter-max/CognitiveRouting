# Phase 2 Execution Board

## Purpose

This board tracks the implementation of the Phase 2 autonomous content engine from
`docs/superpowers/plans/2026-04-20-phase2-autonomous-content-engine.md`.

It is written for new contributors who need two things quickly:

1. What Phase 2 adds to the existing Phase 1 router.
2. Which implementation and verification steps are complete.

## Phase 2 In One Page

Phase 1 remains the persona router. Phase 2 is a separate content-generation slice
that creates an original bot post in three graph steps:

1. `decide_search`
   The Mistral client chooses a topic and a deterministic search query for a bot persona.
2. `web_search`
   A mocked `@tool` search function returns a hardcoded headline based on query keywords.
3. `draft_post`
   The Mistral client converts persona + topic + mock headline into a strict JSON post.

The public output shape is always:

```json
{
  "bot_id": "bot_a",
  "topic": "AI jobs",
  "post_content": "Opinionated post under 280 characters"
}
```

## Architecture Map

| Module | Responsibility | Notes |
| --- | --- | --- |
| `content_engine/models.py` | Shared Pydantic models and graph state typing | Schema boundary for LLM and graph outputs |
| `content_engine/tools.py` | Mock search tool and lookup table | Deterministic, no network access |
| `content_engine/llm.py` | Only Mistral SDK wrapper in the repo | Structured parsing lives here |
| `content_engine/graph.py` | LangGraph workflow assembly and public orchestration | Keeps node flow readable |
| `demos/phase2.py` | Manual demo entry point | Produces example console output |

## Progress Tracker

| Task | Status | Verification | Notes |
| --- | --- | --- | --- |
| 1. Dependencies and config | Complete | Implemented | Config defaults and environment template added |
| 2. Typed content models | Complete | Implemented | Strict schema models and graph state added |
| 3. Mock search tool | Complete | Implemented | Deterministic keyword headlines added |
| 4. Mistral wrapper | Complete | Implemented | Centralized structured-output wrapper added |
| 5. LangGraph orchestration | Complete | Implemented | Three-node workflow added |
| 6. Demo and execution logs | Complete | Implemented | Demo entry point and log scaffold added |
| 7. Deep Phase 2 coverage | Complete | Authored, not re-run here | You asked to run verification elsewhere |
| 8. README reviewability docs | Complete | Implemented | README now documents the structured package layout |

## Verification Log

| Checkpoint | Result |
| --- | --- |
| Baseline `pytest -q` before edits | Passed: `18 passed` |
| Further local verification | Intentionally skipped after your instruction to test elsewhere |

## Repository Structure After Refactor

```text
src/cognitive_routing/
├── config.py
├── routing/
│   ├── __init__.py
│   ├── embeddings.py
│   ├── personas.py
│   ├── router.py
│   └── store.py
├── content_engine/
│   ├── __init__.py
│   ├── graph.py
│   ├── llm.py
│   ├── models.py
│   └── tools.py
├── demos/
│   ├── __init__.py
│   ├── phase1.py
│   └── phase2.py
```

## Working Rules

- Keep Phase 1 behavior intact.
- Keep all Mistral usage inside `content_engine/llm.py`.
- Keep search mocked and deterministic.
- Prefer short, direct docstrings and comments only where control flow benefits.
- Do not claim completion without running the matching verification command.
