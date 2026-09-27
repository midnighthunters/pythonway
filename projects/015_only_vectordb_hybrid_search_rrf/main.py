"""
===============================================================================
PROJECT 015: HYBRID SEARCH: DENSE VECTORS + SPARSE BM25 WITH RRF
Stage 1: Pure Fundamentals | Difficulty: 3.5 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
Why do production search engines and enterprise RAG systems combine Dense Vectors
with Sparse BM25, and why is Reciprocal Rank Fusion (RRF) the industry standard?

THE TWO RETRIEVAL PARADIGMS:
1. Dense Vector Search (Semantic Understanding):
   - Encodes concepts and semantic intent into dense continuous vectors.
   - Excels at synonyms: "cozy warm morning drink" matches "hot cappuccino".
   - FAILS at exact tokens: Completely misses serial codes, model numbers, or rare SKUs.

2. Sparse BM25 Search (Exact Lexical Precision):
   - Uses Term Frequency-Inverse Document Frequency (TF-IDF) on exact word tokens.
   - Excels at exact matches: "ERR-STEAM-8821" or "PUMP-ROTARY-V9".
   - FAILS at paraphrasing: Returns 0 results if the user uses synonyms.

THE SCORE FUSION CHALLENGE:
Why can't we simply add BM25 and Vector scores together (Dense + BM25)?
- Cosine similarity is strictly bounded in [-1.0, 1.0].
- BM25 scores are unbounded [0, inf) and depend heavily on document length and corpus size.
Adding them directly causes BM25 to overwhelm Dense scores, creating erratic results!

THE RRF SOLUTION (Reciprocal Rank Fusion):
RRF discards raw scores entirely and operates purely on ordinal ranks:
  RRF_Score(d) = sum_{m in Models} [ weight_m / (k + rank_m(d)) ]
  (where k is a smoothing constant, typically 60)
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
from collections import Counter
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple, Set
import numpy as np

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. DATA STRUCTURES
# =============================================================================

@dataclass
class Document:
    doc_id: str
    title: str
    text: str


@dataclass
class ScoredResult:
    doc_id: str
    score: float
    rank: int
    retriever: str


# =============================================================================
# 2. DENSE VECTOR ENGINE
# =============================================================================
VECTOR_DIM = 128


def embed_text(text: str, dim: int = VECTOR_DIM) -> np.ndarray:
    """Computes a deterministic, L2-normalized dense embedding vector."""
    cleaned = re.sub(r"[^\w\s]", " ", text.lower()).strip()
    words = cleaned.split()
    vec = np.zeros(dim, dtype=np.float32)

    for w in words:
        if len(w) <= 1:
            continue
        h = int(hashlib.md5(w.encode("utf-8")).hexdigest(), 16)
        vec[h % dim] += 1.0

    for i in range(len(cleaned) - 2):
        trigram = cleaned[i:i + 3]
        if "  " in trigram:
            continue
        h = int(hashlib.md5(trigram.encode("utf-8")).hexdigest(), 16)
        vec[h % dim] += 0.35

    norm = float(np.linalg.norm(vec))
    if norm > 1e-12:
        vec = vec / norm
    return vec


class DenseVectorEngine:
    """Dense semantic vector retriever using cosine similarity."""

    def __init__(self, dim: int = VECTOR_DIM):
        self.dim = dim
        self.doc_ids: List[str] = []
        self.vectors: np.ndarray = np.empty((0, dim), dtype=np.float32)

    def index_documents(self, documents: List[Document]) -> None:
        self.doc_ids = [d.doc_id for d in documents]
        vecs = [embed_text(d.text, dim=self.dim) for d in documents]
        self.vectors = np.array(vecs, dtype=np.float32)

    def search(self, query: str, top_k: int = 5) -> List[ScoredResult]:
        if len(self.doc_ids) == 0:
            return []

        q_vec = embed_text(query, dim=self.dim)
        scores = np.dot(self.vectors, q_vec)
        top_indices = np.argsort(-scores)[:top_k]

        results = []
        for rank, idx in enumerate(top_indices, 1):
            results.append(ScoredResult(
                doc_id=self.doc_ids[idx],
                score=float(scores[idx]),
                rank=rank,
                retriever="DenseVector",
            ))
        return results


# =============================================================================
# 3. SPARSE OKAPI BM25 ENGINE
# =============================================================================

class BM25Engine:
    """
    Okapi BM25 implementation for lexical keyword search:
    IDF(t) = ln( (N - df(t) + 0.5) / (df(t) + 0.5) + 1.0 )
    Score(D, Q) = sum_{t in Q} [ IDF(t) * (TF(t, D) * (k1 + 1)) / (TF(t, D) + k1 * (1 - b + b * (|D| / avgdl))) ]
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = 0
        self.avg_doc_len = 0.0
        self.doc_ids: List[str] = []
        self.doc_lengths: Dict[str, int] = {}
        self.doc_term_freqs: Dict[str, Counter] = {}
        self.doc_freqs: Counter = Counter()

    def _tokenize(self, text: str) -> List[str]:
        # Preserve hyphens and alphanumeric codes like ERR-STEAM-8821
        cleaned = re.sub(r"[^\w\-]", " ", text.lower())
        return [tok for tok in cleaned.split() if len(tok) > 1]

    def index_documents(self, documents: List[Document]) -> None:
        self.corpus_size = len(documents)
        self.doc_ids = []
        self.doc_lengths = {}
        self.doc_term_freqs = {}
        self.doc_freqs = Counter()

        total_length = 0
        for doc in documents:
            tokens = self._tokenize(doc.text)
            doc_len = len(tokens)
            self.doc_ids.append(doc.doc_id)
            self.doc_lengths[doc.doc_id] = doc_len
            total_length += doc_len

            tf = Counter(tokens)
            self.doc_term_freqs[doc.doc_id] = tf
            for term in tf.keys():
                self.doc_freqs[term] += 1

        self.avg_doc_len = total_length / float(self.corpus_size) if self.corpus_size > 0 else 0.0

    def _idf(self, term: str) -> float:
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            return 0.0
        # Standard Lucene/BM25 formula
        return math.log(1.0 + (self.corpus_size - df + 0.5) / (df + 0.5))

    def search(self, query: str, top_k: int = 5) -> List[ScoredResult]:
        q_tokens = self._tokenize(query)
        if not q_tokens or self.corpus_size == 0:
            return []

        doc_scores: Dict[str, float] = {}
        for term in q_tokens:
            idf = self._idf(term)
            if idf <= 0.0:
                continue

            for doc_id, tf_map in self.doc_term_freqs.items():
                freq = tf_map.get(term, 0)
                if freq == 0:
                    continue
                d_len = self.doc_lengths[doc_id]
                num = freq * (self.k1 + 1.0)
                denom = freq + self.k1 * (1.0 - self.b + self.b * (d_len / self.avg_doc_len))
                term_score = idf * (num / denom)
                doc_scores[doc_id] = doc_scores.get(doc_id, 0.0) + term_score

        # Sort descending
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        results = []
        for rank, (doc_id, score) in enumerate(sorted_docs, 1):
            results.append(ScoredResult(
                doc_id=doc_id,
                score=score,
                rank=rank,
                retriever="SparseBM25",
            ))
        return results


# =============================================================================
# 4. RECIPROCAL RANK FUSION (RRF) & LINEAR FUSION
# =============================================================================

class ReciprocalRankFusion:
    """
    Reciprocal Rank Fusion (RRF) algorithm:
    RRF(d) = sum_{m in Models} [ w_m / (k + rank_m(d)) ]
    - Invariant to raw score distributions.
    - Standard industry constant: k = 60.
    """

    def __init__(self, k: int = 60, weights: Optional[Dict[str, float]] = None):
        self.k = k
        self.weights = weights or {"DenseVector": 1.0, "SparseBM25": 1.0}

    def fuse(self, ranked_lists: List[List[ScoredResult]], top_k: int = 5) -> List[Dict[str, Any]]:
        rrf_scores: Dict[str, float] = {}
        breakdowns: Dict[str, Dict[str, int]] = {}

        for r_list in ranked_lists:
            for item in r_list:
                w = self.weights.get(item.retriever, 1.0)
                contribution = w / (self.k + item.rank)

                rrf_scores[item.doc_id] = rrf_scores.get(item.doc_id, 0.0) + contribution
                if item.doc_id not in breakdowns:
                    breakdowns[item.doc_id] = {}
                breakdowns[item.doc_id][item.retriever] = item.rank

        # Sort descending by fused RRF score
        sorted_candidates = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        fused_results = []
        for final_rank, (doc_id, score) in enumerate(sorted_candidates, 1):
            fused_results.append({
                "doc_id": doc_id,
                "rrf_score": score,
                "final_rank": final_rank,
                "ranks_by_retriever": breakdowns.get(doc_id, {}),
            })
        return fused_results


def linear_score_combination(
    dense_results: List[ScoredResult],
    bm25_results: List[ScoredResult],
    alpha: float = 0.5,
    top_k: int = 5,
) -> List[Tuple[str, float]]:
    """
    Min-max normalized score fusion for empirical comparison:
    Score = alpha * norm(Dense) + (1 - alpha) * norm(BM25)
    """
    def min_max_normalize(results: List[ScoredResult]) -> Dict[str, float]:
        if not results:
            return {}
        scores = [r.score for r in results]
        min_s, max_s = min(scores), max(scores)
        diff = max_s - min_s
        if diff < 1e-12:
            return {r.doc_id: 1.0 for r in results}
        return {r.doc_id: (r.score - min_s) / diff for r in results}

    norm_dense = min_max_normalize(dense_results)
    norm_bm25 = min_max_normalize(bm25_results)

    all_docs = set(norm_dense.keys()).union(norm_bm25.keys())
    combined = {}
    for doc in all_docs:
        s_d = norm_dense.get(doc, 0.0)
        s_b = norm_bm25.get(doc, 0.0)
        combined[doc] = alpha * s_d + (1.0 - alpha) * s_b

    return sorted(combined.items(), key=lambda x: x[1], reverse=True)[:top_k]


# =============================================================================
# 5. TECHNICAL CAFE KNOWLEDGE BASE & EXPERIMENT SUITE
# =============================================================================

SAMPLE_CORPUS = [
    Document(
        "manual_steam_valve",
        "Steam Pressure Relief Valve",
        "Commercial espresso machine emergency pressure relief valve troubleshooting for code ERR-STEAM-8821. "
        "Located behind secondary panel 4B. If whistling, twist release bolt counter-clockwise."
    ),
    Document(
        "guide_latte_art",
        "Milk Steaming & Latte Art Microfoam",
        "Guide to steaming cold whole milk into velvety microfoam for pouring rosettas "
        "and tulip latte art in flat white and cappuccino cups."
    ),
    Document(
        "manual_rotary_pump",
        "Espresso Rotary Vane Pump",
        "Replacing the high pressure fluid-o-tech rotary pump part PUMP-ROTARY-V9. "
        "Requires 9-bar static pressure calibration using the brass bypass screw."
    ),
    Document(
        "recipe_cold_brew",
        "Cold Immersion Brewing",
        "Steeping coarse ground Ethiopian coffee beans in cold filtered water for 18 hours. "
        "Produces refreshing low-acidity iced coffee."
    ),
    Document(
        "pos_terminal_reset",
        "Cash Register Hardware Troubleshooting",
        "POS touch terminal hardware reset for error code ERR-POS-OFFLINE-04. "
        "Hold the yellow button for 10 seconds to cycle ethernet bridge power."
    ),
]


class HybridSearchPipeline:
    """Unified hybrid pipeline coordinating Dense, Sparse, and RRF re-ranking."""

    def __init__(self, documents: List[Document], rrf_k: int = 60):
        self.doc_map = {d.doc_id: d for d in documents}
        self.dense_engine = DenseVectorEngine()
        self.bm25_engine = BM25Engine()
        self.rrf = ReciprocalRankFusion(k=rrf_k)

        self.dense_engine.index_documents(documents)
        self.bm25_engine.index_documents(documents)

    def search(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        dense_hits = self.dense_engine.search(query, top_k=5)
        bm25_hits = self.bm25_engine.search(query, top_k=5)
        fused = self.rrf.fuse([dense_hits, bm25_hits], top_k=top_k)

        return {
            "query": query,
            "dense_results": dense_hits,
            "bm25_results": bm25_hits,
            "fused_results": fused,
        }


# =============================================================================
# 6. PEDAGOGICAL DEMONSTRATIONS
# =============================================================================

def demo_exact_token_lookup():
    """Case 1: Exact error code lookup where BM25 crushes Dense."""
    print("=" * 80)
    print("CASE 1: EXACT SERIAL/ERROR CODE QUERY: 'ERR-STEAM-8821 valve whistling'")
    print("=" * 80)

    pipeline = HybridSearchPipeline(SAMPLE_CORPUS)
    results = pipeline.search("ERR-STEAM-8821 valve whistling", top_k=3)

    print("DENSE VECTOR RESULTS (Semantic Vector Search):")
    for r in results["dense_results"][:3]:
        print(f"  #{r.rank} [{r.doc_id}] Score: {r.score:.4f} | {SAMPLE_CORPUS[0].title if r.doc_id == SAMPLE_CORPUS[0].doc_id else r.doc_id}")

    print("\nSPARSE BM25 RESULTS (Exact Token Matching):")
    for r in results["bm25_results"][:3]:
        print(f"  #{r.rank} [{r.doc_id}] Score: {r.score:.4f}")

    print("\nFUSED HYBRID RRF RESULTS (Reciprocal Rank Fusion):")
    for r in results["fused_results"]:
        print(f"  #{r['final_rank']} [{r['doc_id']}] RRF Score: {r['rrf_score']:.5f} | Ranks: {r['ranks_by_retriever']}")

    top_doc = results["fused_results"][0]["doc_id"]
    assert top_doc == "manual_steam_valve", "RRF should rank exact error code doc #1!"
    print("\n✅ Verification: RRF successfully promoted the exact error manual to Rank #1!")
    print("-" * 80)


def demo_conceptual_paraphrase():
    """Case 2: Conceptual paraphrase where Dense crushes BM25."""
    print("\n" + "=" * 80)
    print("CASE 2: CONCEPTUAL PARAPHRASE QUERY: 'frothy warm milk morning beverage'")
    print("=" * 80)

    pipeline = HybridSearchPipeline(SAMPLE_CORPUS)
    results = pipeline.search("frothy warm milk morning beverage", top_k=3)

    print("DENSE VECTOR RESULTS (Semantic Vector Search):")
    for r in results["dense_results"][:3]:
        print(f"  #{r.rank} [{r.doc_id}] Score: {r.score:.4f}")

    print("\nSPARSE BM25 RESULTS (Exact Token Matching):")
    if not results["bm25_results"]:
        print("  [0 matches! BM25 failed completely because query tokens were synonyms.]")
    else:
        for r in results["bm25_results"][:3]:
            print(f"  #{r.rank} [{r.doc_id}] Score: {r.score:.4f}")

    print("\nFUSED HYBRID RRF RESULTS (Reciprocal Rank Fusion):")
    for r in results["fused_results"]:
        print(f"  #{r['final_rank']} [{r['doc_id']}] RRF Score: {r['rrf_score']:.5f} | Ranks: {r['ranks_by_retriever']}")

    top_doc = results["fused_results"][0]["doc_id"]
    assert top_doc == "guide_latte_art", "RRF should rank milk steaming doc #1!"
    print("\n✅ Verification: Dense vector semantic understanding carried RRF to Rank #1!")
    print("-" * 80)


def demo_grounded_rag_answer():
    """Case 3: Grounded technical question answered via Groq LLM using RRF retrieved context."""
    print("\n" + "=" * 80)
    print("CASE 3: HYBRID RAG ANSWER GENERATION WITH GROQ LLM")
    print("=" * 80)

    pipeline = HybridSearchPipeline(SAMPLE_CORPUS)
    query = "The espresso machine is whistling and showing error ERR-STEAM-8821. How do I fix it?"
    print(f"Customer Question: '{query}'\n")

    search_res = pipeline.search(query, top_k=3)
    top_hits = search_res["fused_results"]

    context_snippets = []
    for hit in top_hits:
        doc = pipeline.doc_map[hit["doc_id"]]
        context_snippets.append(f"Title: {doc.title}\nContent: {doc.text}")
    context_str = "\n\n".join(context_snippets)

    llm = get_llm(temperature=0.0)
    prompt = (
        f"You are the Commercial Espresso Technician Assistant.\n"
        f"Customer Question: '{query}'\n\n"
        f"Retrieved Technical Documentation (Fused via Hybrid RRF):\n{context_str}\n\n"
        "Instructions: Provide exact, step-by-step repair instructions using the documentation. "
        "Cite the specific panel location and required bolt turn direction."
    )
    answer = llm.invoke(prompt)

    print(f"Model Answer ({ACTIVE_MODEL}):")
    print(answer.content)
    print("=" * 80)


def main():
    print("*" * 80)
    print("PROJECT 015: HYBRID SEARCH (DENSE VECTORS + BM25 + RRF)")
    print(f"Active Model: {ACTIVE_MODEL}")
    print("*" * 80)

    demo_exact_token_lookup()
    demo_conceptual_paraphrase()
    demo_grounded_rag_answer()
    print("\n[SUCCESS] Project 015 executed cleanly end-to-end!")


if __name__ == "__main__":
    main()
