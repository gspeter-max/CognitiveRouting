"""LangGraph orchestration for persona-based content generation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cognitive_routing.content_engine.llm import build_mistral_client, decide_search_for_persona, draft_post_from_context
from cognitive_routing.content_engine.models import ContentGraphState
from cognitive_routing.content_engine.tools import mock_searxng_search

if TYPE_CHECKING:
    from mistralai import Mistral
else:
    Mistral = Any


def _decide_search(state: ContentGraphState, *, client: Mistral) -> ContentGraphState:
    """Resolve the topic and search query that fit the current persona."""

    decision = decide_search_for_persona(client, state["bot_id"], state["persona"])
    return {
        "topic": decision.topic,
        "search_query": decision.search_query,
    }


def _web_search(state: ContentGraphState) -> ContentGraphState:
    """Call the deterministic mock-search tool for one headline."""

    headline = mock_searxng_search.invoke({"query": state["search_query"]})
    return {"search_results": headline}


def _draft_post(state: ContentGraphState, *, client: Mistral) -> ContentGraphState:
    """Generate the final post payload from persona, topic, and headline context."""

    result = draft_post_from_context(
        client,
        state["bot_id"],
        state["persona"],
        state["topic"],
        state["search_results"],
    )
    return {
        "bot_id": result.bot_id,
        "topic": result.topic,
        "post_content": result.post_content,
    }


def build_content_graph(client: Mistral | None = None):
    """Build and compile the linear three-node LangGraph workflow."""

    from langgraph.graph import END, START, StateGraph

    resolved_client = client or build_mistral_client()
    graph = StateGraph(ContentGraphState)
    graph.add_node("decide_search", lambda state: _decide_search(state, client=resolved_client))
    graph.add_node("web_search", _web_search)
    graph.add_node("draft_post", lambda state: _draft_post(state, client=resolved_client))
    graph.add_edge(START, "decide_search")
    graph.add_edge("decide_search", "web_search")
    graph.add_edge("web_search", "draft_post")
    graph.add_edge("draft_post", END)
    return graph.compile()


def generate_original_post(bot_id: str, persona: str, client: Mistral | None = None) -> dict[str, str]:
    """Run the Phase 2 workflow and return the public JSON payload."""

    graph = build_content_graph(client=client)
    result = graph.invoke({"bot_id": bot_id, "persona": persona})
    return {
        "bot_id": result["bot_id"],
        "topic": result["topic"],
        "post_content": result["post_content"],
    }
