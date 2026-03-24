"""
Smoke tests for g2-mcp server.
Requires G2_API_KEY env var to be set.
Tests use real API calls — run against the live G2 API.
"""

import os
import pytest
import httpx

# ---------------------------------------------------------------------------
# We test the tool logic directly by importing server functions,
# avoiding the MCP transport layer in CI.
# ---------------------------------------------------------------------------

os.environ.setdefault("G2_API_KEY", os.environ.get("G2_API_KEY", "test-placeholder"))

from server import (
    search_product,
    get_product,
    get_product_categories,
    get_competitors,
    get_product_ratings,
    get_reviews,
    get_category,
    list_categories,
    API_KEY,
)

SKIP_LIVE = API_KEY == "test-placeholder"
skip_msg = "G2_API_KEY not set — skipping live API tests"


# ---------------------------------------------------------------------------
# Unit-level: shape validation only (no live calls needed)
# ---------------------------------------------------------------------------

def test_imports():
    """All tool functions are importable."""
    assert callable(search_product)
    assert callable(get_product)
    assert callable(get_product_categories)
    assert callable(get_competitors)
    assert callable(get_product_ratings)
    assert callable(get_reviews)
    assert callable(get_category)
    assert callable(list_categories)


# ---------------------------------------------------------------------------
# Live API smoke tests (skipped when no key is set)
# ---------------------------------------------------------------------------

@pytest.mark.skipif(SKIP_LIVE, reason=skip_msg)
def test_search_product_by_name():
    result = search_product(name="Notion")
    assert "products" in result
    assert isinstance(result["products"], list)
    assert result["total"] is not None
    if result["products"]:
        p = result["products"][0]
        assert "id" in p
        assert "name" in p
        assert "slug" in p


@pytest.mark.skipif(SKIP_LIVE, reason=skip_msg)
def test_search_product_by_domain():
    result = search_product(domain="notion.so")
    assert "products" in result


@pytest.mark.skipif(SKIP_LIVE, reason=skip_msg)
def test_search_product_by_slug():
    result = search_product(slug="notion")
    assert "products" in result


@pytest.mark.skipif(SKIP_LIVE, reason=skip_msg)
def test_get_product_and_downstream():
    """Resolve Notion → UUID → use in all downstream tools."""
    search = search_product(name="Notion", page_size=5)
    products = search.get("products", [])
    assert products, "No products returned for 'Notion'"

    notion_id = products[0]["id"]

    # get_product
    product = get_product(notion_id)
    assert product["id"] == notion_id
    assert product["name"]
    assert product["star_rating"] is not None
    assert product["review_count"] is not None

    # get_product_categories
    cats = get_product_categories(notion_id)
    assert "categories" in cats
    assert isinstance(cats["categories"], list)

    # get_competitors
    competitors = get_competitors(notion_id)
    assert "competitors" in competitors
    assert isinstance(competitors["competitors"], list)
    if competitors["competitors"]:
        c = competitors["competitors"][0]
        assert "name" in c
        assert "slug" in c
        assert "g2_url" in c
        assert "star_rating" in c

    # get_product_ratings
    ratings = get_product_ratings(notion_id)
    assert "ease_of_use" in ratings
    assert "quality_of_support" in ratings
    assert "ease_of_setup" in ratings

    # get_reviews
    reviews = get_reviews(notion_id, page_size=5)
    assert "reviews" in reviews
    assert isinstance(reviews["reviews"], list)
    if reviews["reviews"]:
        r = reviews["reviews"][0]
        assert "title" in r
        assert "star_rating" in r
        assert "likes" in r
        assert "dislikes" in r


@pytest.mark.skipif(SKIP_LIVE, reason=skip_msg)
def test_list_categories():
    result = list_categories(page_size=10)
    assert "categories" in result
    assert isinstance(result["categories"], list)
    assert result["total"] is not None


@pytest.mark.skipif(SKIP_LIVE, reason=skip_msg)
def test_get_category_by_slug():
    result = get_category(slug="knowledge-management-software")
    # Returns either a single category or a list
    assert "categories" in result or "id" in result


@pytest.mark.skipif(SKIP_LIVE, reason=skip_msg)
def test_auth_error_on_bad_key(monkeypatch):
    """Confirm a bad API key raises an httpx HTTP error."""
    monkeypatch.setenv("G2_API_KEY", "bad-key-12345")
    import importlib
    import server as srv
    importlib.reload(srv)
    with pytest.raises(httpx.HTTPStatusError):
        srv.search_product(name="Notion")
