"""
Test verification suite for Project 039: FastAPI + VectorDB Semantic Search Service
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import math
from fastapi.testclient import TestClient
from main import app, embed_text, cosine_similarity, vector_store, VECTOR_DIM


def test_embedding_engine():
    v1 = embed_text("Nitro Cold Brew Coffee")
    assert len(v1) == VECTOR_DIM
    norm = math.sqrt(sum(x * x for x in v1))
    assert abs(norm - 1.0) < 1e-4

    v2 = embed_text("Nitro Cold Brew Coffee")
    # Deterministic
    assert v1 == v2

    # High similarity with related text
    sim_self = cosine_similarity(v1, v2)
    assert abs(sim_self - 1.0) < 1e-4


def test_upsert_and_stats():
    vector_store.records.clear()
    client = TestClient(app)

    docs = [
        {"id": "doc1", "text": "Espresso dark roast", "metadata": {"category": "coffee", "price": 3.50}},
        {"id": "doc2", "text": "Almond croissant pastry", "metadata": {"category": "pastry", "price": 4.50}},
        {"id": "doc3", "text": "Cold brew iced beverage", "metadata": {"category": "coffee", "price": 5.00}},
    ]
    res = client.post("/vectors/upsert", json={"documents": docs})
    assert res.status_code == 201
    assert res.json()["upserted_count"] == 3

    stats = client.get("/vectors/stats").json()
    assert stats["total_documents"] == 3
    assert "coffee" in stats["unique_categories"]
    assert "pastry" in stats["unique_categories"]


def test_search_and_metadata_filter():
    client = TestClient(app)

    # Search with category filter
    res = client.post(
        "/vectors/search",
        json={"query": "breakfast snack", "top_k": 5, "filters": {"category": "pastry"}},
    )
    assert res.status_code == 200
    results = res.json()["results"]
    assert len(results) == 1
    assert results[0]["id"] == "doc2"
    assert results[0]["metadata"]["category"] == "pastry"

    # Search with max_price filter
    res_price = client.post(
        "/vectors/search",
        json={"query": "coffee", "top_k": 5, "filters": {"max_price": 4.00}},
    )
    assert res_price.status_code == 200
    p_results = res_price.json()["results"]
    assert len(p_results) == 1
    assert p_results[0]["id"] == "doc1"
    assert p_results[0]["metadata"]["price"] <= 4.00


def test_rag_ask_endpoint():
    client = TestClient(app)
    res = client.post(
        "/vectors/ask",
        json={"question": "What iced coffee do you have?", "top_k": 2},
    )
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data
    assert len(data["answer"]) > 0
    assert len(data["citations"]) > 0


if __name__ == "__main__":
    test_embedding_engine()
    test_upsert_and_stats()
    test_search_and_metadata_filter()
    test_rag_ask_endpoint()
    print("Project 039: All verification tests PASSED successfully!")
