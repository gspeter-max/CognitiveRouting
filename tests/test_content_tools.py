from cognitive_routing.content_engine.tools import mock_searxng_search


def test_mock_search_returns_ai_headline():
    result = mock_searxng_search.invoke({"query": "latest AI coding tools"})
    assert "OpenAI" in result or "AI" in result


def test_mock_search_is_case_insensitive():
    result = mock_searxng_search.invoke({"query": "CRYPTO ETF approval"})
    assert "Bitcoin" in result


def test_mock_search_has_safe_fallback():
    result = mock_searxng_search.invoke({"query": "obscure unknown keyword"})
    assert "No recent matching headlines found" in result
