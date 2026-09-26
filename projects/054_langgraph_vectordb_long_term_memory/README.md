# Project 054: LangGraph + VectorDB: Semantic Long-Term Episodic Memory

> **Stage**: Stage 2: Pairwise Combos  
> **Difficulty**: 5.5 / 10  
> **Primary Pillars**: `LangGraph`, `VectorDB`  
> **Auxiliary Disciplines**: `Agent Memory`  

---

## 🎯 Learning Objective
Equip a LangGraph agent with episodic long-term memory: writes user preferences to VectorDB and retrieves on future turns.

---

## 🧠 Key Concepts Covered
- **Long-Term Memory (LTM)**
- **Episodic vs Semantic Memory**
- **Memory Extraction Node**
- **Memory Reflection**

---

## 🏗️ Architecture & Control Flow
```text
User Message -> Memory Retrieval Node (VectorDB) -> Agent Node -> Memory Reflection Node -> VectorDB.save
```

---

## 📂 Project Structure
```text
054_langgraph_vectordb_long_term_memory/
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
- [ ] Key architectural patterns for `LangGraph`, `VectorDB` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Agent Memory`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
