# Project 013: Approximate Nearest Neighbors (ANN): HNSW & IVF Graphs

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 3.0 / 10 (Intermediate)  
> **Primary Pillars**: `VectorDB`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Understand the algorithmic trade-offs of Approximate Nearest Neighbors (ANN). Implement both **Inverted File Index (IVF)** and **Hierarchical Navigable Small World (HNSW)** graphs from scratch in pure Python/NumPy, evaluate Recall@K against an exact brute-force Flat baseline, and quantify the Recall vs Latency Pareto frontier.

---

## 🧠 Key Concepts Covered
- **The ANN Paradigm**: Exchanging guaranteed 100% recall for a 100x to 1000x latency reduction when scaling beyond 1 million vectors.
- **Inverted File Index (IVF)**: Space partitioning using K-Means clustering to create Voronoi cells and inverted posting lists.
- **IVF Tuning Parameters**:
  - `nlist`: Number of cluster centroids trained across the dataset.
  - `nprobe`: Number of nearest centroids visited per query at search time.
- **HNSW (Hierarchical Navigable Small World)**: A multi-layer proximity graph applying the skip-list principle to high-dimensional metric spaces.
- **HNSW Routing Mechanics**:
  - Upper Layers: Sparse, long-range "highways" traversed greedily in $O(\log N)$ time.
  - Layer 0: Dense, local graph traversed via priority-queue beam search (`efSearch`).
  - Key Parameters: $M$ (max connections per node), $efConstruction$ (build beam width), $efSearch$ (query beam width).
- **Recall@K Metric**: $\text{Recall}@K = \frac{|\text{Retrieved}_K \cap \text{GroundTruth}_K|}{K}$.
- **Distance Evaluation Counts**: Directly quantifying computational savings by counting Euclidean distance evaluations.

---

## 🏗️ Architecture & Control Flow
```text
                  [Query Vector q]
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
┌────────────────────────┐      ┌────────────────────────┐
│    IVF Partitioning    │      │    HNSW Multi-Layer    │
├────────────────────────┤      ├────────────────────────┤
│ 1. Find nprobe closest │      │ 1. Start at entry point│
│    Voronoi centroids   │      │    on top sparse layer │
│ 2. Scan only vectors   │      │ 2. Greedy drop down to │
│    in candidate lists  │      │    next layer          │
│                        │      │ 3. Beam search on L0   │
│                        │      │    using efSearch size │
└───────────┬────────────┘      └───────────┬────────────┘
            │                               │
            └───────────────┬───────────────┘
                            │
                            ▼
          ┌───────────────────────────────────┐
          │   Recall@K Evaluation vs Flat    │
          │   Distance Calculation Savings %  │
          └───────────────────────────────────┘
```

---

## 📂 Project Structure
```text
013_only_vectordb_approximate_nearest_neighbors/
├── README.md              # Project specifications, self-quiz & stretch challenge
├── requirements.txt       # Dependencies for this project
├── config.py              # Groq model and environment configuration
├── main.py                # Pure Python/NumPy IVF and HNSW implementations & benchmark
└── test_verification.py   # Automated assertion tests
```

---

## 🚀 Execution & Verification Guide

### 1. Run Main Demonstration
```bash
python main.py
```

### 2. Run Automated Verification Tests
```bash
python test_verification.py
```

---

## 📝 Self-Assessment Interview Quiz (Test Your Understanding)

1. **Why does HNSW deliver significantly higher queries-per-second (QPS) and recall than IVF on high-dimensional vectors?**
   * *Answer*: In high dimensions (e.g. $d > 256$), the "curse of dimensionality" causes Voronoi cell boundaries in IVF to bleed: nearest neighbors frequently land in neighboring clusters that are not selected unless `nprobe` is set very high, collapsing search into near-linear scanning. In contrast, HNSW graphs exploit small-world clustering: Delaunay-like local connectivity guides graph traversal directly along the actual manifold of the data.

2. **What is the primary operational trade-off of HNSW compared to IVF-PQ in enterprise production?**
   * *Answer*: Memory consumption and build time. HNSW requires storing graph adjacency lists (pointers) for every node across multiple layers, often tripling the RAM footprint over raw vectors and requiring long index construction times. IVF-PQ (Product Quantization) compresses vectors into compact 8-bit codes with negligible index overhead, making IVF preferable when RAM budgets are strictly limited.

3. **How does tuning `efSearch` affect latency and recall during live production traffic?**
   * *Answer*: `efSearch` sets the size of the priority queue candidate pool during Layer 0 graph exploration. A smaller `efSearch` terminates graph expansion early, yielding sub-millisecond latencies at the cost of lower recall. Increasing `efSearch` expands the exploration frontier, asymptotically approaching 100% recall while linearly increasing distance evaluations and request latency.

---

## 🏆 Stretch Challenge
**Task**: Extend the `IVFIndex` class with **Product Quantization (PQ)**: divide each 32-dimensional vector into 4 sub-vectors of 8 dimensions, run mini-K-Means on each sub-space to generate 16 sub-centroids, and represent each vector as a compact 4-byte code.
