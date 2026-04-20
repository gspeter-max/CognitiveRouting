from cognitive_routing.routing.personas import load_personas
from cognitive_routing.routing.store import get_chroma_client, get_persona_collection, query_personas, seed_personas


def test_seed_personas_creates_three_records(tmp_path, monkeypatch):
    monkeypatch.setattr("cognitive_routing.routing.store.embed_text", lambda text: [0.1, 0.2, 0.3])

    client = get_chroma_client(str(tmp_path / "chroma"))
    collection = get_persona_collection(client)
    seed_personas(collection, load_personas())

    result = collection.get(include=["documents", "metadatas"])

    assert len(result["ids"]) == 3
    assert len(result["documents"]) == 3
    assert result["documents"][0]


def test_query_personas_returns_distances(tmp_path, monkeypatch):
    monkeypatch.setattr("cognitive_routing.routing.store.embed_text", lambda text: [0.1, 0.2, 0.3])

    client = get_chroma_client(str(tmp_path / "chroma"))
    collection = get_persona_collection(client)
    seed_personas(collection, load_personas())

    result = query_personas(collection, [0.1, 0.2, 0.3], top_k=3)

    assert "distances" in result
    assert len(result["ids"][0]) == 3


def test_seed_personas_noops_on_empty_input(tmp_path, monkeypatch):
    called = {"embed": False}

    def fake_embed(text):
        called["embed"] = True
        return [0.1, 0.2, 0.3]

    monkeypatch.setattr("cognitive_routing.routing.store.embed_text", fake_embed)

    client = get_chroma_client(str(tmp_path / "chroma"))
    collection = get_persona_collection(client)

    seed_personas(collection, [])

    result = collection.get()
    assert result["ids"] == []
    assert called["embed"] is False


def test_query_personas_rejects_invalid_top_k(tmp_path):
    client = get_chroma_client(str(tmp_path / "chroma"))
    collection = get_persona_collection(client)

    try:
        query_personas(collection, [0.1, 0.2, 0.3], top_k=0)
        raised = False
    except ValueError as exc:
        raised = True
        assert "top_k" in str(exc)

    assert raised is True


def test_get_persona_collection_uses_cosine_distance(monkeypatch):
    captured = {}

    class FakeClient:
        def get_or_create_collection(self, name, metadata):
            captured["name"] = name
            captured["metadata"] = metadata
            return "collection"

    collection = get_persona_collection(FakeClient())

    assert collection == "collection"
    assert captured["name"] == "bot_personas"
    assert captured["metadata"] == {"hnsw:space": "cosine"}


def test_get_chroma_client_uses_http_client_when_env_is_set(monkeypatch):
    captured = {}

    class FakeHttpClient:
        def __call__(self, host, port, ssl):
            captured["host"] = host
            captured["port"] = port
            captured["ssl"] = ssl
            return "http-client"

    monkeypatch.setenv("CHROMA_HOST", "https://example.com:8443")
    monkeypatch.setattr("cognitive_routing.routing.store.chromadb.HttpClient", FakeHttpClient())

    client = get_chroma_client()

    assert client == "http-client"
    assert captured == {"host": "example.com", "port": 8443, "ssl": True}


def test_get_chroma_client_uses_persistent_client_when_no_env(tmp_path, monkeypatch):
    captured = {}

    class FakePersistentClient:
        def __call__(self, path):
            captured["path"] = path
            return "persistent-client"

    monkeypatch.delenv("CHROMA_HOST", raising=False)
    monkeypatch.setattr("cognitive_routing.routing.store.chromadb.PersistentClient", FakePersistentClient())

    client = get_chroma_client(str(tmp_path / "persist"))

    assert client == "persistent-client"
    assert captured["path"].endswith("persist")
