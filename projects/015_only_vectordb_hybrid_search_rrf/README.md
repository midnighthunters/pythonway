# Project 015: Hybrid Search: Dense Vectors + Sparse BM25 with RRF

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 3.5 / 10 (Intermediate)  
> **Primary Pillars**: `VectorDB`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Combine semantic dense embeddings with exact keyword BM25 retrieval using Reciprocal Rank Fusion (RRF).

---

## 🧠 Key Concepts Covered
- **Dense Vector Search**
- **Sparse BM25**
- **Reciprocal Rank Fusion (RRF)**
- **Rank Normalization**

---

## 🏗️ Architecture & Control Flow
```text
Query -> [Dense Vector Search + BM25 Keyword Search] -> RRF Re-ranker -> Fused Results
```

---

## 📂 Project Structure
```text
015_only_vectordb_hybrid_search_rrf/
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
