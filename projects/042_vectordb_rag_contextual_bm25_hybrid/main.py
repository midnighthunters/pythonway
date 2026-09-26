"""
===============================================================================
PROJECT 042: VECTORDB + RAG: CONTEXTUAL BM25 HYBRID SEARCH WITH RANK FUSION
Stage 2: Pairwise Combos | Difficulty: 5.0 / 10
===============================================================================

THE BIG QUESTION:
Why is pure vector search or pure keyword search insufficient for production RAG?
- Pure Dense Vector Search:
  Excels at fuzzy conceptual understanding, but frequently fails on exact serial
  numbers, SKUs, model codes, and rare technical keywords.
- Pure Sparse BM25 Search:
  Excels at exact keyword and code matching, but is completely blind to synonyms,
  paraphrasing, and conceptual intent.

THE PRODUCTION HYBRID SOLUTION (Reciprocal Rank Fusion - RRF):
1. Execute Dense Vector k-NN retrieval and Sparse BM25 retrieval in parallel.
2. Fuse candidate ranks using the industry-standard RRF formula:
      Score(d) = sum( 1 / (60 + rank_i(d)) )
3. Feed the top RRF-fused context into Groq LLM for hallucination-free generation.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import re
import math
import hashlib
import json
from collections import Counter
from typing import List, Dict, Any, Optional, Tuple

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. DENSE VECTOR ENGINE
# =============================================================================
VECTOR_DIM = 128


def embed_text(text: str, dim: int = VECTOR_DIM) -> List[float]:
    """Generates L2-normalized dense frequency vector for semantic similarity."""
    cleaned = re.sub(r"[^\w\s]", " ", text.lower()).strip()
    words = cleaned.split()
    vec = [0.0] * dim

    for w in words:
        if len(w) <= 1:
            continue
        h = int(hashlib.md5(w.encode("utf-8")).hexdigest(), 16)
        idx = h % dim
        vec[idx] += 1.0

    for i in range(len(cleaned) - 2):
        trigram = cleaned[i:i + 3]
        if "  " in trigram:
            continue
        h = int(hashlib.md5(trigram.encode("utf-8")).hexdigest(), 16)
        idx = h % dim
        vec[idx] += 0.25

    norm = math.sqrt(sum(x * x for x in vec))
    if norm > 0.0:
        vec = [x / norm for x in vec]
    return vec


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    return sum(a * b for a, b in zip(v1, v2))


# =============================================================================
# 2. SPARSE BM25 KEYWORD ENGINE
# =============================================================================
class BM25Index:
    """Standard Okapi BM25 implementation for exact keyword and token scoring."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = 0
        self.avg_doc_len = 0.0
        self.doc_lengths: Dict[str, int] = {}
        self.doc_term_freqs: Dict[str, Counter] = {}
        self.doc_texts: Dict[str, str] = {}
        self.doc_freqs: Counter = Counter()

    def tokenize(self, text: str) -> List[str]:
        # Preserve hyphens inside product codes like PART-NOZZLE-89
        tokens = re.findall(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*", text.lower())
        return tokens

    def add_document(self, doc_id: str, text: str):
        tokens = self.tokenize(text)
        self.doc_texts[doc_id] = text
        self.doc_lengths[doc_id] = len(tokens)
        tf = Counter(tokens)
        self.doc_term_freqs[doc_id] = tf

        for term in tf.keys():
            self.doc_freqs[term] += 1

        self.corpus_size = len(self.doc_lengths)
        self.avg_doc_len = sum(self.doc_lengths.values()) / max(1, self.corpus_size)

    def idf(self, term: str) -> float:
        n_q = self.doc_freqs.get(term, 0)
        return math.log(1.0 + (self.corpus_size - n_q + 0.5) / (n_q + 0.5))

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        query_tokens = self.tokenize(query)
        scores: Dict[str, float] = {}

        for doc_id, tf in self.doc_term_freqs.items():
            doc_len = self.doc_lengths[doc_id]
            doc_score = 0.0
            for q_term in query_tokens:
                if q_term in tf:
                    f = tf[q_term]
                    numerator = f * (self.k1 + 1.0)
                    denominator = f + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_len))
                    doc_score += self.idf(q_term) * (numerator / denominator)
            if doc_score > 0.0:
                scores[doc_id] = doc_score

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]


# =============================================================================
# 3. RECIPROCAL RANK FUSION (RRF) ENGINE
# =============================================================================
class HybridSearchEngine:

    def __init__(self, rrf_k: int = 60):
        self.rrf_k = rrf_k
        self.bm25 = BM25Index()
        self.dense_records: Dict[str, Dict[str, Any]] = {}

    def add_document(self, doc_id: str, title: str, text: str):
        self.bm25.add_document(doc_id, f"{title} {text}")
        vec = embed_text(f"{title} {text}")
        self.dense_records[doc_id] = {
            "doc_id": doc_id,
            "title": title,
            "text": text,
            "vector": vec,
        }

    def search(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Runs Dense Vector search and Sparse BM25 search in parallel,
        then combines rankings using Reciprocal Rank Fusion (RRF).
        """
        # 1. Sparse BM25 Search
        bm25_matches = self.bm25.search(query, top_k=10)
        bm25_ranking = [doc_id for doc_id, _ in bm25_matches]

        # 2. Dense Vector Search
        query_vec = embed_text(query)
        dense_scores = []
        for doc_id, rec in self.dense_records.items():
            sim = cosine_similarity(query_vec, rec["vector"])
            dense_scores.append((doc_id, sim))
        dense_scores.sort(key=lambda x: x[1], reverse=True)
        dense_ranking = [doc_id for doc_id, _ in dense_scores[:10]]

        # 3. Reciprocal Rank Fusion
        all_doc_ids = set(bm25_ranking) | set(dense_ranking)
        rrf_scores: Dict[str, float] = {}

        for doc_id in all_doc_ids:
            score = 0.0
            if doc_id in bm25_ranking:
                rank_bm25 = bm25_ranking.index(doc_id) + 1  # 1-indexed
                score += 1.0 / (self.rrf_k + rank_bm25)
            if doc_id in dense_ranking:
                rank_dense = dense_ranking.index(doc_id) + 1  # 1-indexed
                score += 1.0 / (self.rrf_k + rank_dense)
            rrf_scores[doc_id] = score

        fused_ranking = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        results = []
        for doc_id, rrf_score in fused_ranking:
            rec = self.dense_records[doc_id]
            results.append({
                "doc_id": doc_id,
                "title": rec["title"],
                "text": rec["text"],
                "rrf_score": round(rrf_score, 5),
                "bm25_rank": bm25_ranking.index(doc_id) + 1 if doc_id in bm25_ranking else None,
                "dense_rank": dense_ranking.index(doc_id) + 1 if doc_id in dense_ranking else None,
            })

        return {
            "query": query,
            "sparse_top": bm25_ranking[:3],
            "dense_top": dense_ranking[:3],
            "fused_results": results,
        }


# =============================================================================
# 4. KNOWLEDGE CORPUS & DEMONSTRATION
# =============================================================================
CAFE_EQUIPMENT_KNOWLEDGE = [
    {
        "doc_id": "kb_01_valve",
        "title": "Pressure Relief Valve Assembly",
        "text": "The primary boiler pressure relief valve is catalogued under SKU VALVE-TR-200. It is located in Bin #4B.",
    },
    {
        "doc_id": "kb_02_nozzle",
        "title": "Steam Wand Nozzle Maintenance",
        "text": "For steam wand milk scale, use component PART-NOZZLE-89. Clean exclusively with organic citric acid.",
    },
    {
        "doc_id": "kb_03_coffee_energy",
        "title": "Single-Origin Highland Espresso Profile",
        "text": "A velvety dark roasted specialty beverage that provides long-lasting mental stamina and rich cacao notes.",
    },
    {
        "doc_id": "kb_04_cold_brew",
        "title": "Slow-Steeped Cold Brew Tonic",
        "text": "An energizing morning pick-me-up brewed cold for 20 hours with low acidity and maximum crispness.",
    },
]


def run_hybrid_rag(query: str, engine: HybridSearchEngine) -> str:
    search_output = engine.search(query, top_k=2)
    top_matches = search_output["fused_results"]

    context = "\n".join([f"- [{m['doc_id']}] {m['title']}: {m['text']}" for m in top_matches])

    llm = get_llm(temperature=0.2)
    prompt = (
        f"You are the Operations Specialist at Cozy Cafe. Answer the query using ONLY the fused search context.\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"USER QUESTION: {query}\n"
        f"Provide an accurate 2-sentence response directly answering the inquiry."
    )
    res = llm.invoke(prompt)
    return res.content.strip()


# =============================================================================
# 5. MAIN DEMONSTRATION RUNNER
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 042: CONTEXTUAL BM25 + VECTOR DENSE-SPARSE HYBRID SEARCH")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    engine = HybridSearchEngine(rrf_k=60)

    # 1. Ingest Knowledge Documents
    for item in CAFE_EQUIPMENT_KNOWLEDGE:
        engine.add_document(item["doc_id"], item["title"], item["text"])

    # 2. Case A: Exact Keyword / Serial Code Query
    print("\n" + "-" * 75)
    print("CASE A: EXACT SERIAL NUMBER QUERY -> 'Where is VALVE-TR-200 stored?'")
    print("-" * 75)
    res_a = engine.search("Where is VALVE-TR-200 stored?", top_k=2)
    print(f"Sparse BM25 Top:  {res_a['sparse_top']}")
    print(f"Dense Vector Top: {res_a['dense_top']}")
    print(f"RRF Top Match:    {res_a['fused_results'][0]['doc_id']} (Score: {res_a['fused_results'][0]['rrf_score']})")

    # 3. Case B: Fuzzy Conceptual Query
    print("\n" + "-" * 75)
    print("CASE B: FUZZY CONCEPTUAL QUERY -> 'crisp refreshing morning wake up beverage'")
    print("-" * 75)
    res_b = engine.search("crisp refreshing morning wake up beverage", top_k=2)
    print(f"Sparse BM25 Top:  {res_b['sparse_top']}")
    print(f"Dense Vector Top: {res_b['dense_top']}")
    print(f"RRF Top Match:    {res_b['fused_results'][0]['doc_id']} (Score: {res_b['fused_results'][0]['rrf_score']})")

    # 4. Case C: Hybrid Query (Code + Conceptual Context)
    print("\n" + "-" * 75)
    print("CASE C: HYBRID QUERY -> 'How to clean PART-NOZZLE-89 with organic acid?'")
    print("-" * 75)
    res_c = engine.search("How to clean PART-NOZZLE-89 with organic acid?", top_k=2)
    print(f"Sparse BM25 Top:  {res_c['sparse_top']}")
    print(f"Dense Vector Top: {res_c['dense_top']}")
    print(f"RRF Top Match:    {res_c['fused_results'][0]['doc_id']} (Score: {res_c['fused_results'][0]['rrf_score']})")

    # 5. Groq LLM Answer Synthesis using Fused Context
    print("\n" + "-" * 75)
    print("5. GROUNDED RAG SYNTHESIS WITH RRF CONTEXT")
    print("-" * 75)
    rag_ans = run_hybrid_rag("Where is valve VALVE-TR-200 located and what is it for?", engine)
    print(f"AI Answer:\n{rag_ans}")

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 042 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
