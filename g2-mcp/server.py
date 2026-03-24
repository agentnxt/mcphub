#!/usr/bin/env python3
"""
G2 Data API — MCP Server
Exposes G2 product, category, competitor, rating, and review data as MCP tools.

Auth: Token read from G2_API_KEY environment variable.
Base URL: https://data.g2.com
Spec: https://data.g2.com/api/docs
"""

import os
import httpx
from mcp.server.fastmcp import FastMCP

API_KEY = os.environ["G2_API_KEY"]
BASE_URL = "https://data.g2.com"
HEADERS = {
    "Authorization": f"Token token={API_KEY}",
    "Content-Type": "application/vnd.api+json",
}

mcp = FastMCP("g2-mcp")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _get(path: str, params: dict | None = None) -> dict:
    """Execute a GET request against the G2 API and return parsed JSON."""
    resp = httpx.get(
        f"{BASE_URL}{path}",
        headers=HEADERS,
        params=params or {},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def _extract_product_attrs(item: dict) -> dict:
    """Flatten a product data item into a clean dict."""
    attrs = item.get("attributes", {})
    return {
        "id": item.get("id"),
        "name": attrs.get("name"),
        "short_name": attrs.get("short_name"),
        "slug": attrs.get("slug"),
        "domain": attrs.get("domain"),
        "description": attrs.get("description"),
        "detail_description": attrs.get("detail_description"),
        "star_rating": attrs.get("star_rating"),
        "avg_rating": attrs.get("avg_rating"),
        "review_count": attrs.get("review_count"),
        "product_url": attrs.get("product_url"),
        "public_detail_url": attrs.get("public_detail_url"),
        "image_url": attrs.get("image_url"),
        "product_type": attrs.get("product_type"),
    }


# ---------------------------------------------------------------------------
# Tool 1 — search_product
# ---------------------------------------------------------------------------

@mcp.tool()
def search_product(
    name: str | None = None,
    domain: str | None = None,
    slug: str | None = None,
    page_size: int = 10,
    page_number: int = 1,
) -> dict:
    """
    Search for G2 products by name, domain, or slug.
    Returns a list of matching products with their G2 UUIDs.
    The UUID is required for all other G2 tools.

    Use this first to resolve an app name (e.g. "Notion") to its G2 product ID
    before calling get_product, get_competitors, etc.

    Args:
        name: Product name to search (e.g. "Notion", "Slack")
        domain: Product domain (e.g. "notion.so", "slack.com")
        slug: G2 URL slug (e.g. "notion", "slack")
        page_size: Number of results per page (default 10, max 100)
        page_number: Page number (default 1)
    """
    params: dict = {
        "page[size]": page_size,
        "page[number]": page_number,
    }
    if name:
        params["filter[name]"] = name
    if domain:
        params["filter[domain]"] = domain
    if slug:
        params["filter[slug]"] = slug

    data = _get("/api/v1/products", params)

    products = [_extract_product_attrs(item) for item in data.get("data", [])]
    meta = data.get("meta", {})
    return {
        "products": products,
        "total": meta.get("record_count"),
        "pages": meta.get("page_count"),
    }


# ---------------------------------------------------------------------------
# Tool 2 — get_product
# ---------------------------------------------------------------------------

@mcp.tool()
def get_product(product_id: str) -> dict:
    """
    Fetch full details for a single G2 product by its UUID.
    Returns name, slug, domain, description, star rating (0-5),
    average rating (0-10), review count, and G2 public URL.

    Args:
        product_id: G2 product UUID (obtain from search_product)
    """
    data = _get(f"/api/v1/products/{product_id}")
    item = data.get("data", {})
    return _extract_product_attrs(item)


# ---------------------------------------------------------------------------
# Tool 3 — get_product_categories
# ---------------------------------------------------------------------------

@mcp.tool()
def get_product_categories(product_id: str) -> dict:
    """
    Fetch all G2 categories that a product belongs to.
    Returns each category's UUID, name, slug, and description.
    Useful for understanding where a product sits in the G2 taxonomy
    and for finding other products in the same category.

    Args:
        product_id: G2 product UUID (obtain from search_product)
    """
    data = _get(f"/api/v1/products/{product_id}/categories")
    categories = [
        {
            "id": cat.get("id"),
            "name": cat.get("attributes", {}).get("name"),
            "slug": cat.get("attributes", {}).get("slug"),
            "description": cat.get("attributes", {}).get("description"),
            "g2_url": f"https://www.g2.com/categories/{cat.get('attributes', {}).get('slug')}",
        }
        for cat in data.get("data", [])
    ]
    return {
        "product_id": product_id,
        "categories": categories,
        "total": len(categories),
    }


# ---------------------------------------------------------------------------
# Tool 4 — get_competitors
# ---------------------------------------------------------------------------

@mcp.tool()
def get_competitors(product_id: str, limit: int | None = None) -> dict:
    """
    Fetch the full list of G2-identified competitors for a product.
    For each competitor, returns name, slug, G2 URL, star rating,
    review count, main category, and all categories.

    This is the primary tool for building an alternatives list from G2 data.

    Args:
        product_id: G2 product UUID (obtain from search_product)
        limit: Max number of competitors to return (default: all available)
    """
    params: dict = {}
    if limit:
        params["per"] = limit

    data = _get(
        f"/api/2018-01-01/syndication/products/{product_id}/competitors",
        params,
    )

    competitors = []
    for item in data.get("data", []):
        attrs = item.get("attributes", {})
        product = attrs.get("product", {})
        main_cat = attrs.get("main_category", {})
        all_cats = attrs.get("categories", {})

        competitors.append({
            "id": item.get("id"),
            "name": product.get("name"),
            "slug": product.get("slug"),
            "domain": product.get("domain"),
            "g2_url": product.get("g2crowd_url"),
            "star_rating": product.get("star_rating"),
            "avg_rating": product.get("avg_rating"),
            "review_count": product.get("review_count"),
            "description": product.get("detail_description"),
            "main_category": [
                {"id": cid, "name": cdata.get("name"), "slug": cdata.get("slug")}
                for cid, cdata in main_cat.items()
            ],
            "categories": [
                {"id": cid, "name": cdata.get("name"), "slug": cdata.get("slug")}
                for cid, cdata in all_cats.items()
            ],
        })

    return {
        "product_id": product_id,
        "competitors": competitors,
        "total": len(competitors),
    }


# ---------------------------------------------------------------------------
# Tool 5 — get_product_ratings
# ---------------------------------------------------------------------------

@mcp.tool()
def get_product_ratings(product_id: str) -> dict:
    """
    Fetch detailed feature/satisfaction ratings for a G2 product.
    Returns scores (0-10) for: ease of use, quality of support,
    and ease of setup. These complement the overall star rating
    with dimension-level insight.

    Args:
        product_id: G2 product UUID (obtain from search_product)
    """
    data = _get(
        f"/api/2018-01-01/syndication/products/{product_id}/product_ratings"
    )
    return {
        "product_id": product_id,
        "ease_of_use": data.get("ease_of_use"),
        "quality_of_support": data.get("quality_of_support"),
        "ease_of_setup": data.get("ease_of_setup"),
    }


# ---------------------------------------------------------------------------
# Tool 6 — get_reviews
# ---------------------------------------------------------------------------

@mcp.tool()
def get_reviews(
    product_id: str,
    page_size: int = 25,
    page_number: int = 1,
    submitted_after: str | None = None,
    submitted_before: str | None = None,
) -> dict:
    """
    Fetch paginated reviews for a G2 product.
    Each review includes: title, star rating, likes (love), dislikes (hate),
    recommendations, reviewer name, country, company size, and review date.

    Use this to extract feature comparison signals from what real users say
    they love/hate about a product vs. its competitors.

    Args:
        product_id: G2 product UUID (obtain from search_product)
        page_size: Reviews per page (default 25, max 100)
        page_number: Page number (default 1)
        submitted_after: Only reviews submitted after this date (rfc3339 format)
        submitted_before: Only reviews submitted before this date (rfc3339 format)
    """
    params: dict = {
        "page[size]": page_size,
        "page[number]": page_number,
    }
    if submitted_after:
        params["filter[submitted_at_gt]"] = submitted_after
    if submitted_before:
        params["filter[submitted_at_lt]"] = submitted_before

    data = _get(f"/api/v1/products/{product_id}/survey-responses", params)

    reviews = []
    for item in data.get("data", []):
        attrs = item.get("attributes", {})
        comment_answers = attrs.get("comment_answers", {})
        reviews.append({
            "id": item.get("id"),
            "title": attrs.get("title"),
            "star_rating": attrs.get("star_rating"),
            "submitted_at": attrs.get("submitted_at"),
            "reviewer": attrs.get("user_name"),
            "country": attrs.get("country_name"),
            "review_source": attrs.get("review_source"),
            "likes": comment_answers.get("love", {}).get("value"),
            "dislikes": comment_answers.get("hate", {}).get("value"),
            "recommendations": comment_answers.get("recommendations", {}).get("value"),
            "benefits": comment_answers.get("benefits", {}).get("value"),
            "votes_up": attrs.get("votes_up"),
            "votes_down": attrs.get("votes_down"),
            "g2_url": f"https://www.g2.com/products/{attrs.get('product_name', '').lower().replace(' ', '-')}/reviews/{attrs.get('slug', '')}",
        })

    meta = data.get("meta", {})
    return {
        "product_id": product_id,
        "reviews": reviews,
        "total": meta.get("record_count"),
        "pages": meta.get("page_count"),
        "page": page_number,
    }


# ---------------------------------------------------------------------------
# Tool 7 — get_category
# ---------------------------------------------------------------------------

@mcp.tool()
def get_category(
    category_id: str | None = None,
    slug: str | None = None,
    name: str | None = None,
) -> dict:
    """
    Fetch a G2 category by UUID, slug, or name.
    Returns the category name, slug, description, and G2 URL.
    Also returns links to child categories, ancestors, and descendants
    for navigating the G2 taxonomy tree.

    Args:
        category_id: G2 category UUID
        slug: Category URL slug (e.g. "knowledge-management-software")
        name: Category name to search (used only if no id or slug)
    """
    if category_id:
        data = _get(f"/api/v1/categories/{category_id}")
        item = data.get("data", {})
        attrs = item.get("attributes", {})
        return {
            "id": item.get("id"),
            "name": attrs.get("name"),
            "slug": attrs.get("slug"),
            "description": attrs.get("description"),
            "g2_url": f"https://www.g2.com/categories/{attrs.get('slug')}",
        }

    # Fall back to list search
    params: dict = {"page[size]": 10}
    if slug:
        params["slug"] = slug
    if name:
        params["name"] = name

    data = _get("/api/v1/categories", params)
    items = data.get("data", [])
    return {
        "categories": [
            {
                "id": cat.get("id"),
                "name": cat.get("attributes", {}).get("name"),
                "slug": cat.get("attributes", {}).get("slug"),
                "description": cat.get("attributes", {}).get("description"),
                "g2_url": f"https://www.g2.com/categories/{cat.get('attributes', {}).get('slug')}",
            }
            for cat in items
        ],
        "total": data.get("meta", {}).get("record_count"),
    }


# ---------------------------------------------------------------------------
# Tool 8 — list_categories
# ---------------------------------------------------------------------------

@mcp.tool()
def list_categories(
    name: str | None = None,
    slug: str | None = None,
    page_size: int = 25,
    page_number: int = 1,
) -> dict:
    """
    Search and list G2 software categories.
    Useful for discovering which G2 category a product market belongs to,
    or for browsing the G2 taxonomy.

    Args:
        name: Filter by category name (partial match supported)
        slug: Filter by category slug
        page_size: Results per page (default 25, max 100)
        page_number: Page number (default 1)
    """
    params: dict = {
        "page[size]": page_size,
        "page[number]": page_number,
    }
    if name:
        params["name"] = name
    if slug:
        params["slug"] = slug

    data = _get("/api/v1/categories", params)
    meta = data.get("meta", {})
    return {
        "categories": [
            {
                "id": cat.get("id"),
                "name": cat.get("attributes", {}).get("name"),
                "slug": cat.get("attributes", {}).get("slug"),
                "description": cat.get("attributes", {}).get("description"),
                "g2_url": f"https://www.g2.com/categories/{cat.get('attributes', {}).get('slug')}",
            }
            for cat in data.get("data", [])
        ],
        "total": meta.get("record_count"),
        "pages": meta.get("page_count"),
    }


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
