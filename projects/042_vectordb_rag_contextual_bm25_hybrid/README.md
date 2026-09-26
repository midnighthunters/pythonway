# Project 042: VectorDB + RAG: Contextual Hybrid Search with Rank Fusion

> **Stage**: Stage 2: Pairwise Combos  
> **Difficulty**: 5.0 / 10  
> **Primary Pillars**: `VectorDB`, `RAG`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Build a hybrid RAG pipeline fusing VectorDB embeddings and BM25 keywords, evaluating retrieval recall improvements.

---

## 🧠 Key Concepts Covered
- **Hybrid Search**
- **Reciprocal Rank Fusion**
- **BM25 Scoring**
- **Dense-Sparse Fusion**

---

## 🏗️ Architecture & Control Flow
```text
Query -> [Chroma Vector Collection + In-memory BM25] -> RRF Fusion -> RAG Context Assembly -> LLM
```

---

## 📂 Project Structure
```text
042_vectordb_rag_contextual_bm25_hybrid/
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
- [ ] Key architectural patterns for `VectorDB`, `RAG` are explicitly demonstrated.
- [ ] Auxiliary production concerns (None (Core Focus)) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
