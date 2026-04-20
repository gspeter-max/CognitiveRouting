from cognitive_routing.pipeline.full_pipeline import run_full_pipeline
from cognitive_routing.routing.personas import Persona


def test_run_full_pipeline_routes_then_generates(monkeypatch):
    monkeypatch.setattr(
        "cognitive_routing.pipeline.full_pipeline.load_personas",
        lambda: [
            Persona(
                bot_id="bot_a",
                bot_name="Tech Maximalist",
                description="Optimistic AI persona",
                tags=("ai",),
            ),
            Persona(
                bot_id="bot_b",
                bot_name="Skeptic",
                description="Critical privacy persona",
                tags=("privacy",),
            ),
        ],
    )
    monkeypatch.setattr("cognitive_routing.pipeline.full_pipeline.get_chroma_client", lambda: object())
    monkeypatch.setattr("cognitive_routing.pipeline.full_pipeline.get_persona_collection", lambda client: object())
    monkeypatch.setattr("cognitive_routing.pipeline.full_pipeline.seed_personas", lambda collection, personas: None)
    monkeypatch.setattr(
        "cognitive_routing.pipeline.full_pipeline.route_post_to_bots",
        lambda collection, post_content, threshold: [
            {"bot_id": "bot_b", "bot_name": "Skeptic", "similarity": 0.91},
            {"bot_id": "bot_a", "bot_name": "Tech Maximalist", "similarity": 0.74},
        ],
    )
    monkeypatch.setattr(
        "cognitive_routing.pipeline.full_pipeline.generate_original_post",
        lambda bot_id, persona, client=None: {
            "bot_id": bot_id,
            "topic": "Privacy rules",
            "post_content": f"Generated from {persona}",
        },
    )

    result = run_full_pipeline("User input about surveillance", mistral_client=object())

    assert result["selected_bot"]["bot_id"] == "bot_b"
    assert result["selected_bot"]["bot_name"] == "Skeptic"
    assert result["generated_post"] == {
        "bot_id": "bot_b",
        "topic": "Privacy rules",
        "post_content": "Generated from Critical privacy persona",
    }


def test_run_full_pipeline_raises_when_no_phase1_match(monkeypatch):
    monkeypatch.setattr("cognitive_routing.pipeline.full_pipeline.load_personas", lambda: [])
    monkeypatch.setattr("cognitive_routing.pipeline.full_pipeline.get_chroma_client", lambda: object())
    monkeypatch.setattr("cognitive_routing.pipeline.full_pipeline.get_persona_collection", lambda client: object())
    monkeypatch.setattr("cognitive_routing.pipeline.full_pipeline.seed_personas", lambda collection, personas: None)
    monkeypatch.setattr(
        "cognitive_routing.pipeline.full_pipeline.route_post_to_bots",
        lambda collection, post_content, threshold: [],
    )

    try:
        run_full_pipeline("No matches")
        raised = False
    except ValueError as exc:
        raised = True
        assert "did not find a persona match" in str(exc)

    assert raised is True
