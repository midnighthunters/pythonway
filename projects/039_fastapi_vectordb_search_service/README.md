# Project 039: FastAPI + VectorDB: Semantic Search & Embedding Microservice

> **Stage**: Stage 2: Pairwise Combos  
> **Difficulty**: 4.0 / 10  
> **Primary Pillars**: `FastAPI`, `VectorDB`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Build a high-performance vector search API supporting document upsert, metadata filtering, and k-NN queries.

---

## 🧠 Key Concepts Covered
- **Vector Upsert API**
- **k-NN Search Endpoints**
- **Payload Filters**
- **Vector Store Service**

---

## 🏗️ Architecture & Control Flow
```text
Client -> POST /vectors/upsert -> Vector Index | GET /vectors/search -> Top-K Nearest Matches
```

---

## 📂 Project Structure
```text
039_fastapi_vectordb_search_service/
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
- [ ] Key architectural patterns for `FastAPI`, `VectorDB` are explicitly demonstrated.
- [ ] Auxiliary production concerns (None (Core Focus)) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
