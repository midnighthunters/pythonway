# Project 044: VectorDB + LangGraph: Cyclic Self-Correcting RAG with Evaluation

> **Stage**: Stage 2: Pairwise Combos  
> **Difficulty**: 5.0 / 10  
> **Primary Pillars**: `VectorDB`, `LangGraph`  
> **Auxiliary Disciplines**: `AI Evaluation`  

---

## 🎯 Learning Objective
Construct a LangGraph cycle that queries VectorDB, evaluates document relevance with grading prompts, and rewrites queries.

---

## 🧠 Key Concepts Covered
- **Cyclic RAG**
- **Relevance Grader Node**
- **AI Evaluation Scoring**
- **Query Rewriter Node**

---

## 🏗️ Architecture & Control Flow
```text
START -> Query VectorDB -> Evaluate Relevance Score -> [Pass: Generate -> END | Fail: Rewrite -> Query VectorDB]
```

---

## 📂 Project Structure
```text
044_vectordb_langgraph_self_correcting_rag/
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
- [ ] Key architectural patterns for `VectorDB`, `LangGraph` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`AI Evaluation`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
