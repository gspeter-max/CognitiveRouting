from cognitive_routing.routing.personas import load_personas
from cognitive_routing.routing.router import route_post_to_bots
from cognitive_routing.routing.store import get_chroma_client, get_persona_collection, seed_personas


def test_route_post_to_bots_returns_matching_bots(tmp_path, monkeypatch):
    monkeypatch.setattr("cognitive_routing.routing.store.embed_text", lambda text: [0.1, 0.2, 0.3])
    monkeypatch.setattr("cognitive_routing.routing.router.embed_text", lambda text: [0.1, 0.2, 0.3])

    client = get_chroma_client(str(tmp_path / "chroma"))
    collection = get_persona_collection(client)
    seed_personas(collection, load_personas())

    matches = route_post_to_bots(
        collection,
        "OpenAI just released a new model that might replace junior developers.",
        threshold=0.0,
    )

    assert isinstance(matches, list)
    assert len(matches) >= 1
    assert {"bot_id", "bot_name", "similarity"} <= set(matches[0].keys())


def test_route_post_to_bots_filters_below_threshold(tmp_path, monkeypatch):
    monkeypatch.setattr("cognitive_routing.routing.store.embed_text", lambda text: [0.1, 0.2, 0.3])
    monkeypatch.setattr("cognitive_routing.routing.router.embed_text", lambda text: [0.1, 0.2, 0.3])

    client = get_chroma_client(str(tmp_path / "chroma"))
    collection = get_persona_collection(client)
    seed_personas(collection, load_personas())

    matches = route_post_to_bots(
        collection,
        "A quiet afternoon with no technology news at all.",
        threshold=0.99,
    )

    assert isinstance(matches, list)


def test_route_post_to_bots_includes_score_at_threshold(monkeypatch):
    monkeypatch.setattr("cognitive_routing.routing.router.embed_text", lambda text: [0.1, 0.2, 0.3])
    monkeypatch.setattr(
        "cognitive_routing.routing.router.query_personas",
        lambda collection, query_embedding, top_k=3: {
            "ids": [["bot_a"]],
            "distances": [[0.15]],
            "metadatas": [[{"bot_name": "Tech Maximalist"}]],
        },
    )

    matches = route_post_to_bots(object(), "A post", threshold=0.85)

    assert matches == [
        {
            "bot_id": "bot_a",
            "bot_name": "Tech Maximalist",
            "similarity": 0.85,
        }
    ]


def test_route_post_to_bots_returns_empty_list_for_empty_query_result(monkeypatch):
    monkeypatch.setattr("cognitive_routing.routing.router.embed_text", lambda text: [0.1, 0.2, 0.3])
    monkeypatch.setattr(
        "cognitive_routing.routing.router.query_personas",
        lambda collection, query_embedding, top_k=3: {"ids": [[]], "distances": [[]], "metadatas": [[]]},
    )

    matches = route_post_to_bots(object(), "A post", threshold=0.0)

    assert matches == []


def test_route_post_to_bots_defaults_missing_metadata_to_bot_id(monkeypatch):
    monkeypatch.setattr("cognitive_routing.routing.router.embed_text", lambda text: [0.1, 0.2, 0.3])
    monkeypatch.setattr(
        "cognitive_routing.routing.router.query_personas",
        lambda collection, query_embedding, top_k=3: {
            "ids": [["bot_x"]],
            "distances": [[0.0]],
            "metadatas": [[None]],
        },
    )

    matches = route_post_to_bots(object(), "A post", threshold=0.0)

    assert matches == [
        {
            "bot_id": "bot_x",
            "bot_name": "bot_x",
            "similarity": 1.0,
        }
    ]
