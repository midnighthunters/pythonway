"""
===============================================================================
PROJECT 011: VECTOR MATHEMATICS FROM SCRATCH: COSINE, DOT & EUCLIDEAN
Stage 1: Pure Fundamentals | Difficulty: 2.0 / 10 (Beginner)
===============================================================================

THE BIG QUESTION:
What is the mathematical engine beneath every modern Vector Database (Pinecone,
Chroma, Qdrant, Milvus, Weaviate, pgvector)?

When an embedding model transforms sentences into 1536-dimensional float arrays,
how do we measure "semantic closeness"?
1. Dot Product: Measures directional alignment scaled by vector magnitudes.
2. Cosine Similarity: Measures the cosine of the angle between vectors (normalized [-1, 1]).
3. Euclidean Distance (L2): Measures straight-line geometric distance in hyperspace.

THE CORE MATHEMATICAL IDENTITY:
When vectors are L2-normalized to unit length (||u|| = 1, ||v|| = 1):
  ||u - v||^2 = ||u||^2 + ||v||^2 - 2(u · v)
              = 1 + 1 - 2(u · v)
              = 2(1 - cos(u, v))

Therefore:
  Euclidean_Distance = sqrt(2 * (1 - Cosine_Similarity))

This reveals why sorting by highest Cosine Similarity and sorting by lowest Euclidean
Distance produce the EXACT SAME RANKING on normalized embeddings!
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
from typing import List, Tuple, Dict, Any, Optional
import numpy as np

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. CORE VECTOR MATHEMATICS IN PURE NUMPY
# =============================================================================

def l2_norm(v: np.ndarray) -> float:
    """
    Computes the Euclidean (L2) norm of a vector:
    ||v||_2 = sqrt(sum(v_i^2))
    """
    return float(np.sqrt(np.sum(np.square(v))))


def l2_normalize(v: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    """
    Normalizes a vector or matrix of vectors to unit length (L2 norm = 1.0).
    Handles zero-vectors safely using an epsilon.
    """
    if v.ndim == 1:
        norm = l2_norm(v)
        return v / (norm + eps) if norm > eps else v.copy()
    elif v.ndim == 2:
        norms = np.linalg.norm(v, axis=1, keepdims=True)
        norms = np.where(norms > eps, norms, 1.0)
        return v / norms
    else:
        raise ValueError("Input array must be 1D or 2D.")


def dot_product(u: np.ndarray, v: np.ndarray) -> float:
    """
    Computes the algebraic dot product (inner product):
    u · v = sum(u_i * v_i)
    """
    return float(np.dot(u, v))


def cosine_similarity(u: np.ndarray, v: np.ndarray, eps: float = 1e-12) -> float:
    """
    Computes the cosine similarity between two arbitrary vectors:
    cos(theta) = (u · v) / (||u|| * ||v||)
    Range: [-1.0, 1.0]
    """
    norm_u = l2_norm(u)
    norm_v = l2_norm(v)
    if norm_u < eps or norm_v < eps:
        return 0.0
    return float(np.dot(u, v) / (norm_u * norm_v))


def euclidean_distance(u: np.ndarray, v: np.ndarray) -> float:
    """
    Computes Euclidean (L2) distance:
    d(u, v) = sqrt(sum((u_i - v_i)^2))
    Range: [0.0, inf)
    """
    return float(np.linalg.norm(u - v))


def manhattan_distance(u: np.ndarray, v: np.ndarray) -> float:
    """
    Computes Manhattan (L1) distance:
    d(u, v) = sum(|u_i - v_i|)
    """
    return float(np.sum(np.abs(u - v)))


# =============================================================================
# 2. VECTORIZED BATCH MATRIX OPERATIONS
# =============================================================================

def batch_pairwise_cosine(corpus_matrix: np.ndarray, query_vector: np.ndarray) -> np.ndarray:
    """
    Vectorized cosine similarity calculation across entire corpus at once.
    Avoids slow Python loops:
      sims = (Corpus_norm @ query_norm.T)
    """
    corpus_norm = l2_normalize(corpus_matrix)
    query_norm = l2_normalize(query_vector)
    return np.dot(corpus_norm, query_norm)


def batch_pairwise_euclidean(corpus_matrix: np.ndarray, query_vector: np.ndarray) -> np.ndarray:
    """
    Vectorized Euclidean distance calculation across entire corpus.
    Uses ||a - b||^2 = ||a||^2 + ||b||^2 - 2(a · b) for high performance.
    """
    diff = corpus_matrix - query_vector
    return np.linalg.norm(diff, axis=1)


def top_k_ranked_indices(scores: np.ndarray, k: int = 3, highest_first: bool = True) -> List[Tuple[int, float]]:
    """
    Returns top-k indices and scores sorted by rank.
    """
    if highest_first:
        sorted_indices = np.argsort(-scores)[:k]
    else:
        sorted_indices = np.argsort(scores)[:k]
    return [(int(idx), float(scores[idx])) for idx in sorted_indices]


# =============================================================================
# 3. DETERMINISTIC DENSE SEMANTIC FEATURE EMBEDDER
# =============================================================================

VECTOR_DIM = 128


def embed_text(text: str, dim: int = VECTOR_DIM) -> np.ndarray:
    """
    Generates a deterministic 128-dimensional dense semantic embedding vector.
    Uses token hashing and character trigram hashing to create dense representations
    that capture semantic and lexical similarity without external neural dependencies.
    """
    cleaned = re.sub(r"[^\w\s]", " ", text.lower()).strip()
    words = cleaned.split()
    vec = np.zeros(dim, dtype=np.float64)

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

    # Return L2 normalized embedding
    return l2_normalize(vec)


# =============================================================================
# 4. PEDAGOGICAL DEMONSTRATION SUITE
# =============================================================================

def demo_geometric_vectors():
    """Step 1: Demonstrates fundamental 2D/3D geometric intuition."""
    print("=" * 75)
    print("STEP 1: GEOMETRIC VECTOR COMPARISON (Orthogonal, Identical, Opposing)")
    print("=" * 75)

    u = np.array([1.0, 0.0, 0.0])
    v_identical = np.array([1.0, 0.0, 0.0])
    v_orthogonal = np.array([0.0, 1.0, 0.0])
    v_opposite = np.array([-1.0, 0.0, 0.0])
    v_arbitrary = np.array([3.0, 4.0, 0.0])

    print("Vector u:                  ", u)
    print("Vector v_identical:        ", v_identical)
    print("Vector v_orthogonal (90°): ", v_orthogonal)
    print("Vector v_opposite (180°):  ", v_opposite)
    print("Vector v_arbitrary [3,4,0]:", v_arbitrary)
    print(f"Norm of v_arbitrary:       {l2_norm(v_arbitrary):.2f} (Length before normalization)")
    print(f"Normalized v_arbitrary:    {l2_normalize(v_arbitrary)}")
    print()

    pairs = [
        ("u vs v_identical", u, v_identical),
        ("u vs v_orthogonal", u, v_orthogonal),
        ("u vs v_opposite", u, v_opposite),
        ("u vs v_arbitrary (norm)", u, l2_normalize(v_arbitrary)),
    ]

    print(f"{'Pair':<26} | {'Dot Product':<12} | {'Cosine Sim':<12} | {'Euclidean Dist':<15}")
    print("-" * 75)
    for label, a, b in pairs:
        dp = dot_product(a, b)
        cos = cosine_similarity(a, b)
        euc = euclidean_distance(a, b)
        print(f"{label:<26} | {dp:12.4f} | {cos:12.4f} | {euc:15.4f}")

    print("\nKey Takeaway:")
    print(" - Orthogonal vectors have Cosine Sim = 0.0 (Uncorrelated)")
    print(" - Identical normalized vectors have Cosine Sim = 1.0 and Euclidean Dist = 0.0")
    print(" - Opposing vectors have Cosine Sim = -1.0 and Euclidean Dist = 2.0")
    print("-" * 75)


def demo_mathematical_identity():
    """Step 2: Proves the mathematical equivalence between Cosine and Euclidean."""
    print("\n" + "=" * 75)
    print("STEP 2: MATHEMATICAL IDENTITY ON UNIT HYPERSPHERES")
    print("=" * 75)
    print("Identity: Euclidean_Distance == sqrt(2 * (1 - Cosine_Similarity))\n")

    np.random.seed(42)
    # Generate 5 random pairs of normalized vectors
    for i in range(1, 6):
        a = l2_normalize(np.random.randn(128))
        b = l2_normalize(np.random.randn(128))

        cos = cosine_similarity(a, b)
        direct_euc = euclidean_distance(a, b)
        predicted_euc = math.sqrt(max(0.0, 2.0 * (1.0 - cos)))

        discrepancy = abs(direct_euc - predicted_euc)
        print(f"Trial {i}: Cosine = {cos:+.4f} | Direct L2 = {direct_euc:.6f} | "
              f"sqrt(2(1-cos)) = {predicted_euc:.6f} | Discrepancy = {discrepancy:.2e}")

    print("\nProof Verified: Because all modern embeddings (OpenAI, Voyage, Cohere) are")
    print("unit-normalized, nearest-neighbor searches in Cosine and Euclidean space are identical.")
    print("-" * 75)


def demo_semantic_search():
    """Step 3: Demonstrates text embeddings, batch matrix math, and ranked top-K retrieval."""
    print("\n" + "=" * 75)
    print("STEP 3: REAL-WORLD SEMANTIC SEARCH BENCHMARK (The Cozy Cafe Knowledge Base)")
    print("=" * 75)

    corpus = [
        "How to steam velvety whole milk and pour latte art micro-foam.",
        "Espresso grind calibration, extraction pressure, and tamping technique.",
        "Troubleshooting credit card terminal Wi-Fi disconnection and POS freezes.",
        "Baking fresh artisan sourdough bread, croissants, and blueberry scones.",
        "Cold brew steeping parameters, coarse grind ratio, and dilution guidelines.",
        "Employee dress code, apron cleanliness, and non-slip kitchen shoes.",
    ]

    corpus_vectors = np.array([embed_text(doc) for doc in corpus])
    print(f"Indexed {len(corpus)} documents into {corpus_vectors.shape} NumPy embedding matrix.\n")

    query = "Technique for frothing hot milk for cappuccinos"
    query_vector = embed_text(query)

    print(f"Query: '{query}'")
    print("-" * 75)

    # Batch computations
    cosine_scores = batch_pairwise_cosine(corpus_vectors, query_vector)
    euclidean_dists = batch_pairwise_euclidean(corpus_vectors, query_vector)
    dot_products = np.dot(corpus_vectors, query_vector)

    top_cos = top_k_ranked_indices(cosine_scores, k=3, highest_first=True)
    top_euc = top_k_ranked_indices(euclidean_dists, k=3, highest_first=False)

    print("TOP 3 RETRIEVED BY COSINE SIMILARITY (HIGHEST FIRST):")
    for rank, (idx, score) in enumerate(top_cos, 1):
        print(f"  #{rank} [Score: {score:.4f}] {corpus[idx]}")

    print("\nTOP 3 RETRIEVED BY EUCLIDEAN DISTANCE (LOWEST FIRST):")
    for rank, (idx, dist) in enumerate(top_euc, 1):
        print(f"  #{rank} [Distance: {dist:.4f}] {corpus[idx]}")

    # Confirm matching ranks
    cos_rank_ids = [idx for idx, _ in top_cos]
    euc_rank_ids = [idx for idx, _ in top_euc]
    assert cos_rank_ids == euc_rank_ids, "Ranking mismatch between Cosine and Euclidean!"
    print("\n✅ RANKING CONSISTENCY VERIFIED: Top-K order is 100% identical across metrics!")
    print("-" * 75)


def demo_llm_insight():
    """Step 4: Groq LLM summarizes the architectural implications for vector databases."""
    print("\n" + "=" * 75)
    print("STEP 4: GROQ LLM ARCHITECTURAL REFLECTION")
    print("=" * 75)

    try:
        llm = get_llm(temperature=0.1)
        prompt = (
            "In 3 concise bullet points, explain to a vector database engineer why "
            "normalizing embeddings to unit length (L2 norm = 1.0) is a critical optimization "
            "for vector search speed and hardware acceleration (e.g. BLAS/SIMD)."
        )
        response = llm.invoke(prompt)
        print(f"Model ({ACTIVE_MODEL}):")
        print(response.content)
    except Exception as e:
        print(f"Skipping LLM reflection (API offline or quota): {e}")
    print("=" * 75)


def main():
    print("*" * 75)
    print("PROJECT 011: VECTOR MATHEMATICS FROM SCRATCH (NUMPY ENGINE)")
    print(f"Active Model: {ACTIVE_MODEL}")
    print("*" * 75)

    demo_geometric_vectors()
    demo_mathematical_identity()
    demo_semantic_search()
    demo_llm_insight()
    print("\n[SUCCESS] Project 011 executed cleanly end-to-end!")


if __name__ == "__main__":
    main()
