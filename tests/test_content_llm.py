import pytest

from cognitive_routing.content_engine.llm import build_mistral_client, decide_search_for_persona, draft_post_from_context
from cognitive_routing.content_engine.models import GeneratedPost, SearchDecision


class FakeParsedMessage:
    def __init__(self, parsed):
        self.parsed = parsed


class FakeChoice:
    def __init__(self, parsed):
        self.message = FakeParsedMessage(parsed)


class FakeResponse:
    def __init__(self, parsed):
        self.choices = [FakeChoice(parsed)]


class FakeChat:
    def __init__(self, responses):
        self._responses = responses
        self.calls = []

    def parse(self, **kwargs):
        self.calls.append(kwargs)
        return FakeResponse(self._responses.pop(0))


class FakeClient:
    def __init__(self, responses):
        self.chat = FakeChat(responses)


def test_decide_search_for_persona_returns_search_decision():
    client = FakeClient([SearchDecision(topic="AI jobs", search_query="latest ai jobs news")])
    result = decide_search_for_persona(client, "bot_a", "optimistic AI persona")
    assert result.search_query == "latest ai jobs news"


def test_draft_post_from_context_returns_generated_post():
    client = FakeClient([GeneratedPost(bot_id="bot_a", topic="AI jobs", post_content="Short opinionated post")])
    result = draft_post_from_context(client, "bot_a", "optimistic AI persona", "AI jobs", "headline")
    assert result.bot_id == "bot_a"


def test_build_mistral_client_requires_api_key(monkeypatch):
    monkeypatch.delenv("MISTRAL_API_KEY", raising=False)
    with pytest.raises(ValueError):
        build_mistral_client()
