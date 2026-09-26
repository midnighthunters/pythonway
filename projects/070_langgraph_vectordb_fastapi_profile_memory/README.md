# Project 070: FastAPI + LangGraph + VectorDB: Dynamic Agent Memory Profiling

> **Stage**: Stage 3: Triad Combos  
> **Difficulty**: 7.0 / 10  
> **Primary Pillars**: `FastAPI`, `LangGraph`, `VectorDB`  
> **Auxiliary Disciplines**: `Agent Memory`  

---

## 🎯 Learning Objective
User preference profiling service: analyzes incoming chat messages in LangGraph and updates long-term vector memory.

---

## 🧠 Key Concepts Covered
- **Profile Embedding Extraction**
- **Long-Term Agent Memory**
- **FastAPI User Accounts**
- **Stateful Graph**

---

## 🏗️ Architecture & Control Flow
```text
Chat API -> LangGraph Agent -> Extract Preferences -> VectorDB User Memory Collection -> Tailored Future Answers
```

---

## 📂 Project Structure
```text
070_langgraph_vectordb_fastapi_profile_memory/
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
