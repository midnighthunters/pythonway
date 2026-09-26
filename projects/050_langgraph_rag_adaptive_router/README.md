# Project 050: LangGraph + RAG: Adaptive Query Routing State Machine

> **Stage**: Stage 2: Pairwise Combos  
> **Difficulty**: 5.0 / 10  
> **Primary Pillars**: `LangGraph`, `RAG`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Use LangGraph conditional edges to classify user queries and route between Vector RAG, SQL RAG, or direct LLM reasoning.

---

## 🧠 Key Concepts Covered
- **Adaptive Routing**
- **Query Classification Node**
- **Specialized Knowledge Handlers**
- **Graph Convergence**

---

## 🏗️ Architecture & Control Flow
```text
START -> Query Classifier -> [Unstructured? Vector RAG | Tabular? SQL RAG | General? Direct LLM] -> END
```

---

## 📂 Project Structure
```text
050_langgraph_rag_adaptive_router/
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
- [ ] Key architectural patterns for `LangGraph`, `RAG` are explicitly demonstrated.
- [ ] Auxiliary production concerns (None (Core Focus)) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
