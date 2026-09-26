"""
===============================================================================
PROJECT 039: FASTAPI + VECTORDB: SEMANTIC SEARCH & EMBEDDING MICROSERVICE
Stage 2: Pairwise Combos | Difficulty: 4.0 / 10
===============================================================================

THE BIG QUESTION:
How do enterprise AI microservices provide lightning-fast k-NN vector search,
metadata filtering, document upsert, and grounded RAG answer synthesis over
standard REST APIs?

ARCHITECTURE:
1. High-Precision Vector Engine:
   - Normalized 128-dimensional dense semantic hashing & cosine similarity.
   - Filter predicate evaluator (exact match, range comparisons, booleans).
2. REST Microservice Endpoints:
   - POST /vectors/upsert: Upserts documents with automatic embedding generation.
   - POST /vectors/search: Fast k-NN similarity retrieval with payload filtering.
   - POST /vectors/ask: Grounded RAG endpoint marrying vector search with Groq LLM.
   - GET /vectors/stats: Index telemetry and collection metrics.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import math
import hashlib
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. DENSE VECTOR EMBEDDING & SIMILARITY ENGINE
# =============================================================================
VECTOR_DIM = 128


def embed_text(text: str, dim: int = VECTOR_DIM) -> List[float]:
    """
    Computes a deterministic, L2-normalized dense embedding vector for text.
    Combines token unigrams and character trigrams hashed across fixed dimensions.
    """
    cleaned = text.lower().strip()
    tokens = cleaned.split()
    vec = [0.0] * dim

    # Add token unigram features
    for token in tokens:
        h = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)
        idx = h % dim
        sign = 1.0 if ((h >> 8) % 2 == 0) else -1.0
        vec[idx] += sign * 1.5

    # Add character trigrams for morphological and spelling tolerance
    for i in range(len(cleaned) - 2):
        trigram = cleaned[i:i + 3]
        h = int(hashlib.sha256(trigram.encode("utf-8")).hexdigest(), 16)
        idx = h % dim
        sign = 1.0 if ((h >> 8) % 2 == 0) else -1.0
        vec[idx] += sign * 0.8

    # L2 Normalization so dot product equals cosine similarity
    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 0.0:
        vec = [v / norm for v in vec]
    return vec


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Calculates dot product between two unit vectors."""
    return sum(a * b for a, b in zip(v1, v2))


# =============================================================================
# 2. IN-MEMORY VECTOR STORE WITH PAYLOAD FILTERING
# =============================================================================
class VectorRecord:

    def __init__(self, doc_id: str, text: str, vector: List[float], metadata: Dict[str, Any]):
        self.doc_id = doc_id
        self.text = text
        self.vector = vector
        self.metadata = metadata


class InMemoryVectorStore:

    def __init__(self):
        self.records: Dict[str, VectorRecord] = {}

    def upsert(self, doc_id: str, text: str, metadata: Optional[Dict[str, Any]] = None) -> VectorRecord:
        vector = embed_text(text)
        record = VectorRecord(
            doc_id=doc_id,
            text=text,
            vector=vector,
            metadata=metadata or {},
        )
        self.records[doc_id] = record
        return record

    def search(
        self,
        query_text: str,
        top_k: int = 3,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        query_vec = embed_text(query_text)
        results = []

        for record in self.records.values():
            # Check filter criteria if provided
            if filters:
                match = True
                for key, expected_val in filters.items():
                    if key.startswith("max_"):
                        real_key = key[4:]
                        if record.metadata.get(real_key, float("inf")) > expected_val:
                            match = False
                            break
                    elif key.startswith("min_"):
                        real_key = key[4:]
                        if record.metadata.get(real_key, 0.0) < expected_val:
                            match = False
                            break
                    else:
                        if record.metadata.get(key) != expected_val:
                            match = False
                            break
                if not match:
                    continue

            score = cosine_similarity(query_vec, record.vector)
            results.append({
                "id": record.doc_id,
                "text": record.text,
                "score": round(score, 4),
                "metadata": record.metadata,
            })

        results.sort(key=lambda r: r["score"], reverse=True)
        return results[:top_k]

    def stats(self) -> Dict[str, Any]:
        categories = set(r.metadata.get("category") for r in self.records.values() if "category" in r.metadata)
        return {
            "total_documents": len(self.records),
            "vector_dimension": VECTOR_DIM,
            "unique_categories": list(categories),
        }


vector_store = InMemoryVectorStore()


# =============================================================================
# 3. FASTAPI SCHEMAS & API ENDPOINTS
# =============================================================================
app = FastAPI(title="VectorDB Semantic Search & RAG Microservice", version="1.0.0")


class DocumentItem(BaseModel):
    id: str = Field(..., description="Unique document identifier")
    text: str = Field(..., description="Text content to embed and store")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom metadata attributes")


class UpsertRequest(BaseModel):
    documents: List[DocumentItem]


class SearchRequest(BaseModel):
    query: str = Field(..., description="Semantic search query")
    top_k: int = Field(default=3, ge=1, le=20, description="Max nearest neighbors to return")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Metadata filtering criteria")


class AskRAGRequest(BaseModel):
    question: str = Field(..., description="User query requiring RAG synthesis")
    top_k: int = Field(default=3, description="Context chunks to retrieve")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Optional metadata filters")


@app.post("/vectors/upsert", status_code=status.HTTP_201_CREATED)
def upsert_vectors(req: UpsertRequest):
    """Embeds and indexes incoming documents with metadata."""
    upserted_ids = []
    for doc in req.documents:
        record = vector_store.upsert(doc_id=doc.id, text=doc.text, metadata=doc.metadata)
        upserted_ids.append(record.doc_id)
    return {
        "status": "SUCCESS",
        "upserted_count": len(upserted_ids),
        "document_ids": upserted_ids,
    }


@app.post("/vectors/search")
def search_vectors(req: SearchRequest):
    """Executes k-NN cosine similarity search with optional metadata predicate filtering."""
    results = vector_store.search(
        query_text=req.query,
        top_k=req.top_k,
        filters=req.filters,
    )
    return {
        "query": req.query,
        "returned_count": len(results),
        "results": results,
    }


@app.post("/vectors/ask")
def ask_grounded_rag(req: AskRAGRequest):
    """
    End-to-end RAG pipeline:
    1. Retrieves top-k semantic matches matching filters.
    2. Synthesizes a grounded answer via Groq LLM.
    """
    matches = vector_store.search(query_text=req.question, top_k=req.top_k, filters=req.filters)
    if not matches:
        return {
            "question": req.question,
            "answer": "No relevant menu items or records found matching your criteria.",
            "citations": [],
        }

    context_str = "\n".join(
        [f"- [{m['id']}] {m['text']} (Metadata: {json.dumps(m['metadata'])})" for m in matches]
    )

    llm = get_llm(temperature=0.2)
    prompt = (
        f"You are the Concierge AI at Cozy Cafe. Answer the user's question using ONLY the provided catalog context.\n\n"
        f"CATALOG CONTEXT:\n{context_str}\n\n"
        f"USER QUESTION: {req.question}\n"
        f"Provide a friendly, helpful 2-sentence response citing the matching items."
    )

    response = llm.invoke(prompt)
    return {
        "question": req.question,
        "answer": response.content.strip(),
        "citations": [m["id"] for m in matches],
        "top_match_score": matches[0]["score"],
    }


@app.get("/vectors/stats")
def get_store_stats():
    """Returns vector store metrics and telemetry."""
    return vector_store.stats()


# =============================================================================
# 4. MAIN DEMONSTRATION RUNNER
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 039: FASTAPI + VECTORDB SEMANTIC SEARCH & RAG SERVICE")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    client = TestClient(app)

    # 1. Bulk Upsert Documents
    print("\n" + "-" * 75)
    print("1. POST /vectors/upsert (Indexing Cafe Menu Catalog)")
    print("-" * 75)
    catalog = [
        {
            "id": "item_001",
            "text": "Artisanal Double Espresso pulled with single-origin Ethiopian beans. Notes of dark chocolate and jasmine.",
            "metadata": {"category": "beverage", "price": 3.75, "vegan": True, "caffeine": "high"},
        },
        {
            "id": "item_002",
            "text": "Nitro Cold Brew steeped for 20 hours, infused with nitrogen for an ultra-smooth velvety head.",
            "metadata": {"category": "beverage", "price": 5.50, "vegan": True, "caffeine": "very_high"},
        },
        {
            "id": "item_003",
            "text": "Golden Butter Croissant freshly baked each morning with organic European butter, flaky and golden.",
            "metadata": {"category": "pastry", "price": 4.25, "vegan": False, "caffeine": "none"},
        },
        {
            "id": "item_004",
            "text": "Ceremonial Grade Matcha Latte whisked with creamy oat milk and lightly sweetened with organic agave.",
            "metadata": {"category": "beverage", "price": 6.00, "vegan": True, "caffeine": "medium"},
        },
        {
            "id": "item_005",
            "text": "Vegan Wild Blueberry Muffin made with almond flour, fresh berries, and raw turbinado sugar topping.",
            "metadata": {"category": "pastry", "price": 4.50, "vegan": True, "caffeine": "none"},
        },
    ]
    upsert_res = client.post("/vectors/upsert", json={"documents": catalog})
    print(f"Status Code: {upsert_res.status_code}")
    print(json.dumps(upsert_res.json(), indent=2))

    # 2. k-NN Semantic Search with Metadata Filter
    print("\n" + "-" * 75)
    print("2. POST /vectors/search (Query: 'cold refreshing drink' with category='beverage')")
    print("-" * 75)
    search_res = client.post(
        "/vectors/search",
        json={"query": "cold refreshing drink", "top_k": 2, "filters": {"category": "beverage"}},
    )
    print(f"Status: {search_res.status_code}")
    print(json.dumps(search_res.json(), indent=2))

    # 3. Filter with Numeric Price Boundary
    print("\n" + "-" * 75)
    print("3. POST /vectors/search (Query: 'sweet morning bakery breakfast' with max_price=4.30)")
    print("-" * 75)
    filter_res = client.post(
        "/vectors/search",
        json={"query": "sweet morning bakery breakfast", "top_k": 2, "filters": {"max_price": 4.30}},
    )
    print(f"Status: {filter_res.status_code}")
    print(json.dumps(filter_res.json(), indent=2))

    # 4. Grounded RAG Synthesis
    print("\n" + "-" * 75)
    print("4. POST /vectors/ask (Grounded RAG: 'What vegan pastry do you have under $5.00?')")
    print("-" * 75)
    ask_res = client.post(
        "/vectors/ask",
        json={
            "question": "What vegan pastry do you have under $5.00?",
            "top_k": 2,
            "filters": {"category": "pastry", "vegan": True},
        },
    )
    print(f"Status: {ask_res.status_code}")
    print(json.dumps(ask_res.json(), indent=2))

    # 5. Collection Statistics
    print("\n" + "-" * 75)
    print("5. GET /vectors/stats (Telemetry & Inventory Metrics)")
    print("-" * 75)
    stats_res = client.get("/vectors/stats")
    print(json.dumps(stats_res.json(), indent=2))

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 039 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
