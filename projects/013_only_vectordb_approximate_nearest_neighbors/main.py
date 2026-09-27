"""
===============================================================================
PROJECT 013: APPROXIMATE NEAREST NEIGHBORS (ANN): HNSW & IVF GRAPHS
Stage 1: Pure Fundamentals | Difficulty: 3.0 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
Why can't we use Flat (brute-force) search for 10 million vectors?

A Flat index scales as O(N · d). If N = 10,000,000 vectors with d = 1536 dimensions,
every single query requires 15.36 BILLION floating point operations! Latency reaches
seconds or minutes per query.

THE SOLUTION: APPROXIMATE NEAREST NEIGHBORS (ANN)
We trade a tiny fraction of accuracy (e.g. 98% recall instead of 100%) for a
100x to 1000x speedup!

The two foundational ANN architectures in modern databases (FAISS, Chroma, Qdrant):
1. Inverted File Index (IVF):
   Partitions vector space into Voronoi cells using k-means clustering. At query time,
   we only scan vectors inside the closest `nprobe` centroids.
2. Hierarchical Navigable Small World (HNSW):
   A multi-layer proximity graph inspired by skip-lists. Upper layers provide long-range
   "highways" to zoom into the neighborhood in O(log N); the bottom layer performs
   local beam-search exploration.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import time
import math
import heapq
import random
from typing import List, Dict, Set, Tuple, Any, Optional
import numpy as np

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. EXACT FLAT BASELINE (GROUND TRUTH)
# =============================================================================

class ExactFlatIndex:
    """Brute-force baseline computing exact distances against all N vectors."""

    def __init__(self, vectors: np.ndarray):
        self.vectors = vectors.astype(np.float32)
        self.n, self.dim = vectors.shape

    def search(self, query: np.ndarray, k: int = 5) -> Tuple[List[int], List[float], int]:
        """
        Returns: (top_k_indices, top_k_distances, distance_evaluations_count)
        """
        diff = self.vectors - query
        dists = np.linalg.norm(diff, axis=1)
        dist_evals = self.n

        top_indices = np.argsort(dists)[:k]
        top_dists = [float(dists[i]) for i in top_indices]
        return list(top_indices), top_dists, dist_evals


# =============================================================================
# 2. INVERTED FILE INDEX (IVF) IMPLEMENTATION
# =============================================================================

class IVFIndex:
    """
    Inverted File Index (IVF):
    1. Clusters training vectors into `nlist` Voronoi centroids via K-Means.
    2. Groups vectors into inverted posting lists: centroid_id -> [doc_indices].
    3. Searches only the `nprobe` closest Voronoi cells to the query.
    """

    def __init__(self, nlist: int = 8, niter: int = 15):
        self.nlist = nlist
        self.niter = niter
        self.centroids: Optional[np.ndarray] = None
        self.posting_lists: Dict[int, List[int]] = {i: [] for i in range(nlist)}
        self.vectors: Optional[np.ndarray] = None
        self.dim = 0

    def fit_and_build(self, vectors: np.ndarray) -> None:
        """Trains centroids using K-means and builds posting lists."""
        self.vectors = vectors.astype(np.float32)
        n, self.dim = vectors.shape
        self.nlist = min(self.nlist, n)

        # 1. Initialize centroids randomly
        rng = np.random.RandomState(42)
        init_idx = rng.choice(n, self.nlist, replace=False)
        self.centroids = self.vectors[init_idx].copy()

        # 2. Run K-Means iterations
        for _ in range(self.niter):
            # Assign each vector to closest centroid
            # Pairwise distance: (N, nlist)
            dists = np.linalg.norm(self.vectors[:, None, :] - self.centroids[None, :, :], axis=2)
            cluster_assignments = np.argmin(dists, axis=1)

            # Update centroids
            for c_id in range(self.nlist):
                members = self.vectors[cluster_assignments == c_id]
                if len(members) > 0:
                    self.centroids[c_id] = members.mean(axis=0)

        # 3. Populate inverted posting lists
        self.posting_lists = {i: [] for i in range(self.nlist)}
        dists = np.linalg.norm(self.vectors[:, None, :] - self.centroids[None, :, :], axis=2)
        assignments = np.argmin(dists, axis=1)
        for idx, c_id in enumerate(assignments):
            self.posting_lists[c_id].append(idx)

    def search(self, query: np.ndarray, k: int = 5, nprobe: int = 2) -> Tuple[List[int], List[float], int]:
        """
        Searches the `nprobe` closest centroids.
        Distance evaluations = nlist (to find centroids) + total vectors in visited cells.
        """
        nprobe = min(nprobe, self.nlist)
        # 1. Find closest centroids
        centroid_dists = np.linalg.norm(self.centroids - query, axis=1)
        top_centroids = np.argsort(centroid_dists)[:nprobe]
        dist_evals = self.nlist

        # 2. Gather candidate vector indices
        candidate_indices: List[int] = []
        for c_id in top_centroids:
            candidate_indices.extend(self.posting_lists[c_id])

        if not candidate_indices:
            return [], [], dist_evals

        # 3. Compute distance against only candidate vectors
        sub_vecs = self.vectors[candidate_indices]
        dists = np.linalg.norm(sub_vecs - query, axis=1)
        dist_evals += len(candidate_indices)

        top_local = np.argsort(dists)[:k]
        top_indices = [candidate_indices[i] for i in top_local]
        top_dists = [float(dists[i]) for i in top_local]
        return top_indices, top_dists, dist_evals


# =============================================================================
# 3. HIERARCHICAL NAVIGABLE SMALL WORLD (HNSW) IMPLEMENTATION
# =============================================================================

class HNSWIndex:
    """
    Hierarchical Navigable Small World (HNSW) Graph:
    - Multi-layer proximity graph with logarithmic skip-list traversal.
    - Upper layers have sparse, long-range connections.
    - Bottom layer (Layer 0) contains all elements with dense, localized edges.
    """

    def __init__(self, dim: int, M: int = 8, efConstruction: int = 16, mL: float = 0.62):
        self.dim = dim
        self.M = M  # Max outgoing edges per node
        self.efConstruction = efConstruction
        self.mL = mL  # Normalization factor for level generation
        self.vectors: Dict[int, np.ndarray] = {}
        self.layers: List[Dict[int, Set[int]]] = []
        self.entry_point: Optional[int] = None
        self.max_level: int = -1

    def _dist(self, u: np.ndarray, v: np.ndarray) -> float:
        return float(np.linalg.norm(u - v))

    def _random_level(self) -> int:
        """Geometric distribution level generator."""
        r = random.random()
        if r == 0.0:
            r = 1e-9
        return int(-math.log(r) * self.mL)

    def insert(self, node_id: int, vec: np.ndarray) -> None:
        """Inserts a vector into the multi-layer HNSW graph."""
        vec = vec.astype(np.float32)
        self.vectors[node_id] = vec
        level = self._random_level()

        # Ensure layers exist up to level
        while len(self.layers) <= level:
            self.layers.append({})

        if self.entry_point is None:
            self.entry_point = node_id
            self.max_level = level
            for l in range(level + 1):
                self.layers[l][node_id] = set()
            return

        curr_obj = self.entry_point
        # 1. Greedy search down from max_level to level + 1
        for l in range(self.max_level, level, -1):
            changed = True
            while changed:
                changed = False
                curr_dist = self._dist(vec, self.vectors[curr_obj])
                for neighbor in self.layers[l].get(curr_obj, []):
                    d = self._dist(vec, self.vectors[neighbor])
                    if d < curr_dist:
                        curr_dist = d
                        curr_obj = neighbor
                        changed = True

        # 2. From min(level, max_level) down to 0, connect neighbors
        for l in range(min(level, self.max_level), -1, -1):
            if node_id not in self.layers[l]:
                self.layers[l][node_id] = set()

            # Find M nearest neighbors at this layer
            candidates = list(self.layers[l].keys())
            if node_id in candidates:
                candidates.remove(node_id)
            if candidates:
                dists = [(self._dist(vec, self.vectors[c]), c) for c in candidates]
                dists.sort()
                neighbors = [c for _, c in dists[:self.M]]

                for n_id in neighbors:
                    self.layers[l][node_id].add(n_id)
                    self.layers[l][n_id].add(node_id)
                    # Prune excess edges
                    if len(self.layers[l][n_id]) > self.M:
                        n_dists = [(self._dist(self.vectors[n_id], self.vectors[x]), x) for x in self.layers[l][n_id]]
                        n_dists.sort()
                        self.layers[l][n_id] = set([x for _, x in n_dists[:self.M]])

        if level > self.max_level:
            self.max_level = level
            self.entry_point = node_id

    def search(self, query: np.ndarray, k: int = 5, efSearch: int = 16) -> Tuple[List[int], List[float], int]:
        """
        Executes sub-linear greedy routing on upper layers and beam search on layer 0.
        """
        if self.entry_point is None:
            return [], [], 0

        dist_evals = 0
        curr_obj = self.entry_point

        # 1. Greedy routing on upper layers
        for l in range(self.max_level, 0, -1):
            changed = True
            while changed:
                changed = False
                curr_dist = self._dist(query, self.vectors[curr_obj])
                dist_evals += 1
                for neighbor in self.layers[l].get(curr_obj, []):
                    d = self._dist(query, self.vectors[neighbor])
                    dist_evals += 1
                    if d < curr_dist:
                        curr_dist = d
                        curr_obj = neighbor
                        changed = True

        # 2. Priority queue beam search on Layer 0 (efSearch size)
        visited = {curr_obj}
        # candidates: min-heap of (dist, id)
        candidates = [(self._dist(query, self.vectors[curr_obj]), curr_obj)]
        dist_evals += 1
        # results: max-heap of (-dist, id) to keep track of closest efSearch elements
        w = [(-candidates[0][0], curr_obj)]

        while candidates:
            c_dist, c_id = heapq.heappop(candidates)
            furthest_result_dist = -w[0][0]

            if c_dist > furthest_result_dist and len(w) >= efSearch:
                break

            for neighbor in self.layers[0].get(c_id, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    d = self._dist(query, self.vectors[neighbor])
                    dist_evals += 1
                    furthest_result_dist = -w[0][0]

                    if d < furthest_result_dist or len(w) < efSearch:
                        heapq.heappush(candidates, (d, neighbor))
                        heapq.heappush(w, (-d, neighbor))
                        if len(w) > efSearch:
                            heapq.heappop(w)

        # Extract top k from w
        final_list = [(-dist, nid) for dist, nid in w]
        final_list.sort()
        top_k = final_list[:k]

        return [nid for _, nid in top_k], [d for d, _ in top_k], dist_evals


# =============================================================================
# 4. BENCHMARK & RECALL VS LATENCY TRADEOFF SUITE
# =============================================================================

def compute_recall_at_k(retrieved: List[int], ground_truth: List[int], k: int) -> float:
    """Recall@K = |Retrieved_K ∩ GroundTruth_K| / K"""
    ret_set = set(retrieved[:k])
    gt_set = set(ground_truth[:k])
    return len(ret_set.intersection(gt_set)) / float(k)


def demo_ann_benchmark():
    """Runs a controlled benchmark comparing Flat, IVF, and HNSW on synthetic embeddings."""
    print("=" * 80)
    print("STEP 1: GENERATING CLUSTERED VECTOR SPACE BENCHMARK DATASET")
    print("=" * 80)

    np.random.seed(42)
    random.seed(42)

    n_samples = 500
    n_dim = 32
    k_neighbors = 5

    # Generate synthetic clustered embeddings (5 natural cluster centers)
    centers = np.random.randn(5, n_dim)
    cluster_labels = np.random.randint(0, 5, size=n_samples)
    dataset = np.zeros((n_samples, n_dim), dtype=np.float32)
    for i in range(n_samples):
        c = centers[cluster_labels[i]]
        dataset[i] = c + np.random.randn(n_dim) * 0.35

    # Generate 10 test queries
    queries = [dataset[idx] + np.random.randn(n_dim) * 0.1 for idx in range(10)]

    print(f"Dataset Size: {n_samples} vectors | Dimension: {n_dim} | Search Top-K: {k_neighbors}\n")

    # 1. Exact Flat Ground Truth
    flat_index = ExactFlatIndex(dataset)

    # 2. IVF Index Construction
    print("Building Inverted File Index (IVF) with 10 Voronoi clusters...")
    t0 = time.time()
    ivf_index = IVFIndex(nlist=10, niter=10)
    ivf_index.fit_and_build(dataset)
    print(f"IVF Build Time: {(time.time() - t0)*1000:.2f} ms")

    # 3. HNSW Index Construction
    print("Building Hierarchical Navigable Small World (HNSW) graph...")
    t0 = time.time()
    hnsw_index = HNSWIndex(dim=n_dim, M=8, efConstruction=16)
    for i in range(n_samples):
        hnsw_index.insert(i, dataset[i])
    print(f"HNSW Graph Built: {len(hnsw_index.layers)} layers | Build Time: {(time.time() - t0)*1000:.2f} ms\n")

    # Run Benchmark Across Query Set
    print("=" * 80)
    print(f"{'Index Type':<22} | {'Param':<10} | {'Recall@5':<10} | {'Avg Evals':<12} | {'Savings vs Flat':<16}")
    print("-" * 80)

    # Flat baseline
    flat_evals = []
    flat_gt = []
    for q in queries:
        ids, dists, evals = flat_index.search(q, k=k_neighbors)
        flat_gt.append(ids)
        flat_evals.append(evals)

    avg_flat_evals = np.mean(flat_evals)
    print(f"{'Exact Flat (Baseline)':<22} | {'N/A':<10} | {'100.0%':<10} | {avg_flat_evals:<12.1f} | {'0.0% (Reference)':<16}")

    # IVF sweeps (nprobe = 1, 2, 4)
    for nprobe in [1, 2, 4]:
        recalls, evals_list = [], []
        for q, gt in zip(queries, flat_gt):
            ids, _, evals = ivf_index.search(q, k=k_neighbors, nprobe=nprobe)
            recalls.append(compute_recall_at_k(ids, gt, k_neighbors))
            evals_list.append(evals)
        avg_rec = np.mean(recalls) * 100
        avg_ev = np.mean(evals_list)
        savings = (1.0 - (avg_ev / avg_flat_evals)) * 100
        print(f"{'IVF Index':<22} | {f'nprobe={nprobe}':<10} | {f'{avg_rec:.1f}%':<10} | {avg_ev:<12.1f} | {f'{savings:.1f}% saved':<16}")

    # HNSW sweeps (efSearch = 4, 8, 16)
    for ef in [4, 8, 16]:
        recalls, evals_list = [], []
        for q, gt in zip(queries, flat_gt):
            ids, _, evals = hnsw_index.search(q, k=k_neighbors, efSearch=ef)
            recalls.append(compute_recall_at_k(ids, gt, k_neighbors))
            evals_list.append(evals)
        avg_rec = np.mean(recalls) * 100
        avg_ev = np.mean(evals_list)
        savings = (1.0 - (avg_ev / avg_flat_evals)) * 100
        print(f"{'HNSW Graph':<22} | {f'ef={ef}':<10} | {f'{avg_rec:.1f}%':<10} | {avg_ev:<12.1f} | {f'{savings:.1f}% saved':<16}")

    print("=" * 80)


def demo_llm_tradeoff_guidance():
    """Step 2: Groq LLM provides architectural advice for index selection."""
    print("\n" + "=" * 80)
    print("STEP 2: ARCHITECTURAL DECISION MATRIX (GROQ LLM GUIDANCE)")
    print("=" * 80)
    try:
        llm = get_llm(temperature=0.1)
        prompt = (
            "Provide a crisp 3-point architectural comparison between HNSW and IVF "
            "for an AI engineer deploying a production Vector Database:\n"
            "1. When to choose HNSW over IVF.\n"
            "2. When to choose IVF over HNSW (memory constraints / build time).\n"
            "3. The impact of efSearch vs nprobe tuning on user latency."
        )
        resp = llm.invoke(prompt)
        print(f"Model ({ACTIVE_MODEL}):")
        print(resp.content)
    except Exception as e:
        print(f"Skipping LLM guidance (API offline): {e}")
    print("-" * 80)


def main():
    print("*" * 80)
    print("PROJECT 013: APPROXIMATE NEAREST NEIGHBORS (HNSW & IVF ALGORITHMS)")
    print(f"Active Model: {ACTIVE_MODEL}")
    print("*" * 80)

    demo_ann_benchmark()
    demo_llm_tradeoff_guidance()
    print("\n[SUCCESS] Project 013 executed cleanly end-to-end!")


if __name__ == "__main__":
    main()
