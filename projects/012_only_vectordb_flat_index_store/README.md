# Project 012: In-Memory Flat Vector Store & k-NN Search Engine

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 2.5 / 10 (Intermediate)  
> **Primary Pillars**: `VectorDB`  
> **Auxiliary Disciplines**: `Agent Memory`  

---

## 🎯 Learning Objective
Build a zero-dependency in-memory vector store with insert, batch indexing, and exact k-NN search for agent memories.

---

## 🧠 Key Concepts Covered
- **Flat Index**
- **k-Nearest Neighbors (k-NN)**
- **Vector Memory Storage**
- **Query Embedding Projection**

---

## 🏗️ Architecture & Control Flow
```text
Memory Facts -> Vector Projection -> Memory Index -> Query -> Top-K Retrieved Memories
```

---

## 📂 Project Structure
```text
012_only_vectordb_flat_index_store/
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
- [ ] Auxiliary production concerns (`Agent Memory`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
