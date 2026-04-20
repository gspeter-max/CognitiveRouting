from cognitive_routing.content_engine.graph import generate_original_post
from cognitive_routing.content_engine.models import GeneratedPost, SearchDecision


class StubClient:
    pass


def test_generate_original_post_runs_full_pipeline(monkeypatch):
    monkeypatch.setattr(
        "cognitive_routing.content_engine.graph.decide_search_for_persona",
        lambda client, bot_id, persona: SearchDecision(
            topic="AI jobs",
            search_query="latest ai jobs news",
        ),
    )
    monkeypatch.setattr(
        "cognitive_routing.content_engine.graph.mock_searxng_search",
        type("Tool", (), {"invoke": staticmethod(lambda payload: "OpenAI releases a coding model")}),
    )
    monkeypatch.setattr(
        "cognitive_routing.content_engine.graph.draft_post_from_context",
        lambda client, bot_id, persona, topic, search_results: GeneratedPost(
            bot_id=bot_id,
            topic=topic,
            post_content="AI is changing software work faster than most teams admit.",
        ),
    )

    result = generate_original_post("bot_a", "Optimistic AI persona", client=StubClient())

    assert result == {
        "bot_id": "bot_a",
        "topic": "AI jobs",
        "post_content": "AI is changing software work faster than most teams admit.",
    }


def test_generate_original_post_preserves_json_shape(monkeypatch):
    monkeypatch.setattr(
        "cognitive_routing.content_engine.graph.build_content_graph",
        lambda client=None: type(
            "Graph",
            (),
            {
                "invoke": staticmethod(
                    lambda state: {
                        "bot_id": "bot_b",
                        "topic": "Privacy rules",
                        "post_content": "Unchecked surveillance is exactly how monopolies tighten control.",
                        "ignored": "not returned",
                    }
                )
            },
        )(),
    )

    result = generate_original_post("bot_b", "skeptic persona")

    assert set(result.keys()) == {"bot_id", "topic", "post_content"}
