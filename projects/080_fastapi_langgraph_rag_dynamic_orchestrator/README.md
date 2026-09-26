# Project 080: FastAPI + LangGraph + RAG: Adaptive Q&A API with LangSmith Tracing

> **Stage**: Stage 3: Triad Combos  
> **Difficulty**: 8.0 / 10  
> **Primary Pillars**: `FastAPI`, `LangGraph`, `RAG`  
> **Auxiliary Disciplines**: `LangSmith`  

---

## 🎯 Learning Objective
Production enterprise Q&A API running an adaptive LangGraph workflow selecting RAG strategies with full LangSmith tracing.

---

## 🧠 Key Concepts Covered
- **Query Complexity Scoring**
- **Strategy Switching**
- **LangSmith Tracing**
- **Groundedness Verification**

---

## 🏗️ Architecture & Control Flow
```text
Client -> POST /query -> Graph analyzes complexity -> [Simple: Fast RAG | Complex: Agentic RAG] -> LangSmith Trace
```

---

## 📂 Project Structure
```text
080_fastapi_langgraph_rag_dynamic_orchestrator/
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
- [ ] Key architectural patterns for `FastAPI`, `LangGraph`, `RAG` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`LangSmith`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
