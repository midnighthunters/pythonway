# Project 017: Query Transformation, Multi-Query & Sub-Questions

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 2.5 / 10 (Intermediate)  
> **Primary Pillars**: `RAG`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Deconstruct complex multi-part user questions into independent sub-queries, retrieving complementary context.

---

## 🧠 Key Concepts Covered
- **Query Decomposition**
- **Sub-question Generation**
- **Multi-Query Retriever**
- **Context Union**

---

## 🏗️ Architecture & Control Flow
```text
Complex Question -> LLM Decomposition -> 3 Sub-queries -> Parallel Retrieval -> Merged Context
```

---

## 📂 Project Structure
```text
017_only_rag_query_decomposition/
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
- [ ] Key architectural patterns for `RAG` are explicitly demonstrated.
- [ ] Auxiliary production concerns (None (Core Focus)) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
