"""
Automated Verification Suite for Project 013: Approximate Nearest Neighbors (ANN): HNSW & IVF Graphs.
Validates IVF K-means clustering, HNSW graph navigation, Recall@K metric math, and search efficiency.
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import numpy as np
from main import (
    ExactFlatIndex,
    IVFIndex,
    HNSWIndex,
    compute_recall_at_k,
)


def test_exact_flat_baseline():
    print("Testing Exact Flat Baseline...")
    vecs = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.8, 0.6, 0.0],
    ], dtype=np.float32)

    index = ExactFlatIndex(vecs)
    q = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    ids, dists, evals = index.search(q, k=2)

    assert ids[0] == 0, f"Expected top match index 0, got {ids[0]}"
    assert dists[0] == 0.0, f"Distance to itself should be 0, got {dists[0]}"
    assert evals == 4, f"Flat search should evaluate all 4 vectors, got {evals}"
    print("  [PASSED] Exact flat baseline verified.")


def test_ivf_construction_and_search():
    print("Testing IVF Clustering and Posting Lists...")
    np.random.seed(42)
    vecs = np.random.randn(100, 16).astype(np.float32)
    ivf = IVFIndex(nlist=5, niter=10)
    ivf.fit_and_build(vecs)

    assert ivf.centroids.shape == (5, 16), f"Centroids shape mismatch: {ivf.centroids.shape}"
    total_assigned = sum(len(lst) for lst in ivf.posting_lists.values())
    assert total_assigned == 100, f"All 100 vectors must be assigned to posting lists, got {total_assigned}"

    q = vecs[10]
    ids, dists, evals = ivf.search(q, k=3, nprobe=2)
    assert len(ids) == 3, f"Expected 3 neighbors, got {len(ids)}"
    assert evals < 100, f"IVF should evaluate fewer than all 100 vectors, got {evals}"
    print("  [PASSED] IVF construction and posting lists verified.")


def test_hnsw_construction_and_search():
    print("Testing HNSW Multi-Layer Graph and Search...")
    np.random.seed(42)
    vecs = np.random.randn(50, 16).astype(np.float32)
    hnsw = HNSWIndex(dim=16, M=6, efConstruction=12)

    for i in range(50):
        hnsw.insert(i, vecs[i])

    assert hnsw.entry_point is not None
    assert len(hnsw.layers) >= 1
    assert len(hnsw.layers[0]) == 50, f"Layer 0 must contain all 50 nodes, got {len(hnsw.layers[0])}"

    q = vecs[5]
    ids, dists, evals = hnsw.search(q, k=3, efSearch=8)
    assert len(ids) == 3
    assert ids[0] == 5, f"Expected node 5 to be found as top neighbor, got {ids[0]}"
    assert dists[0] < 1e-5, f"Distance should be ~0.0, got {dists[0]}"
    print("  [PASSED] HNSW multi-layer insertion and greedy search verified.")


def test_recall_metric_math():
    print("Testing Recall@K Metric Math...")
    retrieved = [1, 2, 3, 4, 5]
    gt = [1, 2, 8, 9, 10]
    recall = compute_recall_at_k(retrieved, gt, k=5)
    # Common elements: {1, 2} -> 2/5 = 0.4
    assert abs(recall - 0.4) < 1e-9, f"Expected recall 0.4, got {recall}"

    perfect_recall = compute_recall_at_k([1, 2, 3], [1, 2, 3], k=3)
    assert abs(perfect_recall - 1.0) < 1e-9
    print("  [PASSED] Recall@K metric calculation verified.")


def test_monotonic_recall_tradeoff():
    print("Testing Monotonic Recall Improvement with Tuning Parameters...")
    np.random.seed(99)
    vecs = np.random.randn(150, 16).astype(np.float32)
    flat = ExactFlatIndex(vecs)
    ivf = IVFIndex(nlist=8, niter=10)
    ivf.fit_and_build(vecs)

    q = vecs[0] + np.random.randn(16) * 0.05
    gt_ids, _, _ = flat.search(q, k=5)

    ids_p1, _, evals_p1 = ivf.search(q, k=5, nprobe=1)
    ids_p8, _, evals_p8 = ivf.search(q, k=5, nprobe=8)

    rec_p1 = compute_recall_at_k(ids_p1, gt_ids, 5)
    rec_p8 = compute_recall_at_k(ids_p8, gt_ids, 5)

    assert rec_p8 >= rec_p1, f"Expected higher/equal recall with nprobe=8 vs nprobe=1 (got {rec_p8} vs {rec_p1})"
    assert evals_p8 > evals_p1, "Evaluating more clusters must consume more distance evaluations"
    print("  [PASSED] Monotonic recall tradeoff verified.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 013")
    print("=" * 60)
    test_exact_flat_baseline()
    test_ivf_construction_and_search()
    test_hnsw_construction_and_search()
    test_recall_metric_math()
    test_monotonic_recall_tradeoff()
    print("\n[ALL TESTS PASSED] Project 013 verified successfully!")
