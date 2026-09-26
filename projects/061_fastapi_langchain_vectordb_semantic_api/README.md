# Project 061: FastAPI + LangChain + VectorDB: Enterprise Search API with Tracing

> **Stage**: Stage 3: Triad Combos  
> **Difficulty**: 6.5 / 10  
> **Primary Pillars**: `FastAPI`, `LangChain`, `VectorDB`  
> **Auxiliary Disciplines**: `LangSmith`  

---

## 🎯 Learning Objective
Build an enterprise semantic search platform with query expansion, vector search, and LangSmith latency telemetry.

---

## 🧠 Key Concepts Covered
- **Query Expansion LCEL**
- **Vector Similarity API**
- **Hybrid Scoring**
- **LangSmith Tracing**

---

## 🏗️ Architecture & Control Flow
```text
Client -> FastAPI POST /search -> LCEL Query Expander -> VectorDB Search -> Formatted Results (Traced)
```

---

## 📂 Project Structure
```text
061_fastapi_langchain_vectordb_semantic_api/
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
- [ ] Key architectural patterns for `FastAPI`, `LangChain`, `VectorDB` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`LangSmith`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
