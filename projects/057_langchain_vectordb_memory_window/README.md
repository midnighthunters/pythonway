# Project 057: LangChain + VectorDB: Semantic Chat History Retrieval Window

> **Stage**: Stage 2: Pairwise Combos  
> **Difficulty**: 4.5 / 10  
> **Primary Pillars**: `LangChain`, `VectorDB`  
> **Auxiliary Disciplines**: `Agent Memory`  

---

## 🎯 Learning Objective
Replace rigid sliding conversation buffers with vector semantic history retrieval in an LCEL conversational chain.

---

## 🧠 Key Concepts Covered
- **VectorStoreRetrieverMemory**
- **Semantic Chat History**
- **Agent Memory Buffer**
- **LCEL Memory Plumbing**

---

## 🏗️ Architecture & Control Flow
```text
User Query -> VectorDB search over past conversation turns -> Inject relevant past context -> LCEL Chain
```

---

## 📂 Project Structure
```text
057_langchain_vectordb_memory_window/
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
- [ ] Key architectural patterns for `LangChain`, `VectorDB` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Agent Memory`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
