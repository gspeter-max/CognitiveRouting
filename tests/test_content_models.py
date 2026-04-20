import pytest
from pydantic import ValidationError

from cognitive_routing.config import CONTENT_POST_CHAR_LIMIT, DEFAULT_MISTRAL_MODEL
from cognitive_routing.content_engine.models import GeneratedPost, SearchDecision


def test_phase2_config_defaults_are_exposed():
    assert DEFAULT_MISTRAL_MODEL == "mistral-small-latest"
    assert CONTENT_POST_CHAR_LIMIT == 280


def test_search_decision_requires_topic_and_query():
    decision = SearchDecision(topic="AI jobs", search_query="latest ai jobs news")
    assert decision.topic == "AI jobs"
    assert decision.search_query == "latest ai jobs news"


def test_generated_post_rejects_extra_fields():
    with pytest.raises(ValidationError):
        GeneratedPost(
            bot_id="bot_a",
            topic="AI jobs",
            post_content="A short post",
            extra_field="not allowed",
        )
