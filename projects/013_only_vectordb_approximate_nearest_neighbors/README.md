# Project 013: Approximate Nearest Neighbors (ANN): HNSW & IVF Graphs

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 3.0 / 10 (Intermediate)  
> **Primary Pillars**: `VectorDB`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Understand and configure scalable Approximate Nearest Neighbor (ANN) index structures (HNSW and IVF) using Chroma/FAISS.

---

## 🧠 Key Concepts Covered
- **HNSW (Hierarchical Navigable Small World)**
- **IVF (Inverted File Index)**
- **Recall vs Latency Tradeoff**

---

## 🏗️ Architecture & Control Flow
```text
Dense Vectors -> Multi-layer HNSW Graph Construction -> Sub-linear Top-K Graph Traversal
```

---

## 📂 Project Structure
```text
013_only_vectordb_approximate_nearest_neighbors/
├── README.md              # Project specifications and concepts (this file)
├── requirements.txt       # Isolated dependencies for this project
├── config.py              # Model and environment configuration
└── main.py                # Core runnable implementation
```

---

## 🚀 Execution & Verification Guide

### 1. Setup Environment
Ensure your virtual environment is active and dependencies are installed:
```bash
pip install -r requirements.txt
```

### 2. Run Project
```bash
python main.py
```

### 3. Acceptance Criteria
- [ ] Code runs end-to-end with zero runtime or validation errors.
- [ ] Key architectural patterns for `VectorDB` are explicitly demonstrated.
- [ ] Auxiliary production concerns (None (Core Focus)) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
