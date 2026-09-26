# Project 062: FastAPI + LangGraph + VectorDB: Stateful Support with Working Memory

> **Stage**: Stage 3: Triad Combos  
> **Difficulty**: 7.0 / 10  
> **Primary Pillars**: `FastAPI`, `LangGraph`, `VectorDB`  
> **Auxiliary Disciplines**: `Agent Memory`  

---

## 🎯 Learning Objective
Multi-turn support chatbot: preserves conversation thread in LangGraph and retrieves relevant knowledge from VectorDB.

---

## 🧠 Key Concepts Covered
- **Persistent Threads**
- **Agent Working Memory**
- **Customer Intent Routing**
- **Streaming Chat API**

---

## 🏗️ Architecture & Control Flow
```text
Client -> FastAPI -> LangGraph -> VectorDB Node -> Intent Router -> Agent Node -> Thread Saved -> Response
```

---

## 📂 Project Structure
```text
062_fastapi_langgraph_vectordb_support_bot/
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
- [ ] Key architectural patterns for `FastAPI`, `LangGraph`, `VectorDB` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Agent Memory`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
