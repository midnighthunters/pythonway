# Project 063: LangGraph + VectorDB + RAG: Autonomous Agentic RAG with Self-Evaluation

> **Stage**: Stage 3: Triad Combos  
> **Difficulty**: 7.5 / 10  
> **Primary Pillars**: `LangGraph`, `VectorDB`, `RAG`  
> **Auxiliary Disciplines**: `AI Evaluation`, `Guardrails`  

---

## 🎯 Learning Objective
Complete Agentic RAG graph: Query rewriting, document grading, hallucination detection guardrails, and web fallback.

---

## 🧠 Key Concepts Covered
- **Agentic RAG**
- **Document Quality Grader**
- **Hallucination Guardrails**
- **AI Evaluation Metrics**

---

## 🏗️ Architecture & Control Flow
```text
START -> Rewrite Query -> VectorDB Retrieve -> Grade Docs -> [Good: Generate -> Self-Reflect | Bad: Web Search] -> END
```

---

## 📂 Project Structure
```text
063_langgraph_vectordb_rag_agentic_rag/
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
- [ ] Key architectural patterns for `LangGraph`, `VectorDB`, `RAG` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`AI Evaluation`, `Guardrails`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
