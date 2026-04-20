"""Typed models shared by the Phase 2 content engine."""

from __future__ import annotations

from typing import TypedDict

from pydantic import BaseModel, ConfigDict, Field

from cognitive_routing.config import CONTENT_POST_CHAR_LIMIT


class SearchDecision(BaseModel):
    """Structured topic and search query selected for a persona-driven post."""

    model_config = ConfigDict(extra="forbid")

    topic: str = Field(min_length=3)
    search_query: str = Field(min_length=3)


class GeneratedPost(BaseModel):
    """Strict final post payload returned by the Phase 2 graph."""

    model_config = ConfigDict(extra="forbid")

    bot_id: str
    topic: str = Field(min_length=3)
    post_content: str = Field(min_length=1, max_length=CONTENT_POST_CHAR_LIMIT)


class ContentGraphState(TypedDict, total=False):
    """Mutable state shared between the linear LangGraph nodes."""

    bot_id: str
    persona: str
    topic: str
    search_query: str
    search_results: str
    post_content: str


class ThreadMessage(TypedDict):
    """Represents a single message in a back-and-forth thread."""

    author: str
    content: str
