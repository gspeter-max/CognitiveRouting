from cognitive_routing import embeddings


def test_embed_text_returns_non_empty_vector(monkeypatch):
    class FakeModel:
        def encode(self, text, normalize_embeddings=True, convert_to_numpy=True):
            assert normalize_embeddings is True
            assert convert_to_numpy is True
            assert text == "AI is changing software development"
            return [0.1, 0.2, 0.3]

    monkeypatch.setattr(embeddings, "get_embedding_model", lambda: FakeModel())

    vector = embeddings.embed_text("AI is changing software development")

    assert vector == [0.1, 0.2, 0.3]


def test_embed_texts_returns_same_number_of_vectors_as_inputs(monkeypatch):
    class FakeModel:
        def encode(self, texts, normalize_embeddings=True, convert_to_numpy=True):
            assert normalize_embeddings is True
            assert convert_to_numpy is True
            assert texts == ["AI", "crypto", "markets"]
            return [[1.0], [2.0], [3.0]]

    monkeypatch.setattr(embeddings, "get_embedding_model", lambda: FakeModel())

    vectors = embeddings.embed_texts(["AI", "crypto", "markets"])

    assert vectors == [[1.0], [2.0], [3.0]]


def test_embed_texts_returns_empty_list_for_no_inputs(monkeypatch):
    called = {"encode": False}

    class FakeModel:
        def encode(self, texts, normalize_embeddings=True, convert_to_numpy=True):
            called["encode"] = True
            return []

    monkeypatch.setattr(embeddings, "get_embedding_model", lambda: FakeModel())

    vectors = embeddings.embed_texts([])

    assert vectors == []
    assert called["encode"] is False


def test_get_embedding_model_is_cached(monkeypatch):
    embeddings.get_embedding_model.cache_clear()
    calls = {"count": 0}

    class FakeModel:
        pass

    def fake_sentence_transformer(model_name):
        calls["count"] += 1
        assert model_name == "BAAI/bge-small-en-v1.5"
        return FakeModel()

    monkeypatch.setattr(embeddings, "SentenceTransformer", fake_sentence_transformer)

    first = embeddings.get_embedding_model()
    second = embeddings.get_embedding_model()

    assert first is second
    assert calls["count"] == 1

    embeddings.get_embedding_model.cache_clear()
