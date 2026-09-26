# Project 037: FastAPI + LangGraph: Multi-Turn Stateful Chatbot with Working Memory

> **Stage**: Stage 2: Pairwise Combos  
> **Difficulty**: 4.5 / 10  
> **Primary Pillars**: `FastAPI`, `LangGraph`  
> **Auxiliary Disciplines**: `Agent Memory`  

---

## 🎯 Learning Objective
Expose a stateful LangGraph conversation engine over FastAPI with persistent session threads and working memory.

---

## 🧠 Key Concepts Covered
- **Thread Checkpoints**
- **Working Memory**
- **Session ID Headers**
- **State Restoration**

---

## 🏗️ Architecture & Control Flow
```text
Client (with thread_id) -> FastAPI -> LangGraph.invoke(working_memory) -> State Snapshot -> Response
```

---

## 📂 Project Structure
```text
037_fastapi_langgraph_stateful_chat/
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
- [ ] Key architectural patterns for `FastAPI`, `LangGraph` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Agent Memory`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
