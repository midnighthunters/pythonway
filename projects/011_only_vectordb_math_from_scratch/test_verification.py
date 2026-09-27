"""
Automated Verification Suite for Project 011: Vector Mathematics from Scratch.
Validates normalization, cosine similarity, Euclidean distance, batch matrix math,
and ranking consistency.
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import math
import numpy as np
from main import (
    l2_norm,
    l2_normalize,
    dot_product,
    cosine_similarity,
    euclidean_distance,
    manhattan_distance,
    batch_pairwise_cosine,
    batch_pairwise_euclidean,
    top_k_ranked_indices,
    embed_text,
)


def test_l2_norm_and_normalization():
    print("Testing L2 Norm and Normalization...")
    v = np.array([3.0, 4.0])
    assert abs(l2_norm(v) - 5.0) < 1e-9, f"Expected norm 5.0, got {l2_norm(v)}"

    v_norm = l2_normalize(v)
    assert abs(l2_norm(v_norm) - 1.0) < 1e-9, "Normalized vector norm must be 1.0"
    assert np.allclose(v_norm, np.array([0.6, 0.8])), "Components must be [0.6, 0.8]"

    # Test 2D matrix normalization
    mat = np.array([[3.0, 4.0], [1.0, 1.0]])
    mat_norm = l2_normalize(mat)
    assert abs(l2_norm(mat_norm[0]) - 1.0) < 1e-9
    assert abs(l2_norm(mat_norm[1]) - 1.0) < 1e-9

    # Zero vector safety
    zero_vec = np.zeros(5)
    normalized_zero = l2_normalize(zero_vec)
    assert np.all(normalized_zero == 0.0), "Zero vector should remain zero without crashing"
    print("  [PASSED] L2 norm and normalization passed.")


def test_geometric_cases():
    print("Testing Fundamental Geometric Angles...")
    u = np.array([1.0, 0.0, 0.0])
    v_ident = np.array([1.0, 0.0, 0.0])
    v_ortho = np.array([0.0, 1.0, 0.0])
    v_opp = np.array([-1.0, 0.0, 0.0])

    # Identical
    assert abs(cosine_similarity(u, v_ident) - 1.0) < 1e-9
    assert abs(euclidean_distance(u, v_ident) - 0.0) < 1e-9

    # Orthogonal
    assert abs(cosine_similarity(u, v_ortho) - 0.0) < 1e-9
    assert abs(euclidean_distance(u, v_ortho) - math.sqrt(2.0)) < 1e-9

    # Opposite
    assert abs(cosine_similarity(u, v_opp) - (-1.0)) < 1e-9
    assert abs(euclidean_distance(u, v_opp) - 2.0) < 1e-9
    print("  [PASSED] Geometric cases passed.")


def test_mathematical_identity():
    print("Testing Mathematical Identity on Unit Vectors...")
    np.random.seed(99)
    for _ in range(20):
        a = l2_normalize(np.random.randn(64))
        b = l2_normalize(np.random.randn(64))

        cos = cosine_similarity(a, b)
        euc = euclidean_distance(a, b)
        predicted_euc = math.sqrt(max(0.0, 2.0 * (1.0 - cos)))

        assert abs(euc - predicted_euc) < 1e-7, (
            f"Mathematical identity failed: euc={euc}, predicted={predicted_euc}"
        )
    print("  [PASSED] Euclidean-Cosine equivalence identity verified.")


def test_vectorized_batch_parity():
    print("Testing Vectorized Matrix Math Parity...")
    np.random.seed(123)
    corpus = l2_normalize(np.random.randn(50, 32))
    query = l2_normalize(np.random.randn(32))

    batch_cos = batch_pairwise_cosine(corpus, query)
    batch_euc = batch_pairwise_euclidean(corpus, query)

    for i in range(len(corpus)):
        single_cos = cosine_similarity(corpus[i], query)
        single_euc = euclidean_distance(corpus[i], query)
        assert abs(batch_cos[i] - single_cos) < 1e-7, f"Mismatch in batch cosine at index {i}"
        assert abs(batch_euc[i] - single_euc) < 1e-7, f"Mismatch in batch euclidean at index {i}"
    print("  [PASSED] Batch matrix calculations match element-wise loops.")


def test_top_k_ranking_equivalence():
    print("Testing Top-K Ranking Order Equivalence...")
    corpus_texts = [
        "Specialty coffee brewing and espresso extraction parameters.",
        "Espresso steam wand frothing and milk steaming techniques.",
        "Fixing kitchen POS system network connection errors.",
        "Artisan bakery recipe for warm chocolate croissants.",
        "Cold brew coffee beans steeping in chilled water.",
    ]
    corpus_vecs = np.array([embed_text(t) for t in corpus_texts])
    query_vec = embed_text("Steaming milk for flat white and latte")

    cosine_scores = batch_pairwise_cosine(corpus_vecs, query_vec)
    euclidean_dists = batch_pairwise_euclidean(corpus_vecs, query_vec)

    top_cos = top_k_ranked_indices(cosine_scores, k=3, highest_first=True)
    top_euc = top_k_ranked_indices(euclidean_dists, k=3, highest_first=False)

    cos_indices = [idx for idx, _ in top_cos]
    euc_indices = [idx for idx, _ in top_euc]

    assert cos_indices == euc_indices, f"Ranks differed: cos={cos_indices}, euc={euc_indices}"
    # Index 1 (milk steaming) must be top ranked
    assert cos_indices[0] == 1, f"Expected document 1 to be top rank, got {cos_indices[0]}"
    print("  [PASSED] Top-K ranking equivalence verified across Cosine and Euclidean.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 011")
    print("=" * 60)
    test_l2_norm_and_normalization()
    test_geometric_cases()
    test_mathematical_identity()
    test_vectorized_batch_parity()
    test_top_k_ranking_equivalence()
    print("\n[ALL TESTS PASSED] Project 011 verified successfully!")
