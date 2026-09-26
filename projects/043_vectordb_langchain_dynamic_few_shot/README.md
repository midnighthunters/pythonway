# Project 043: VectorDB + LangChain: Dynamic Semantic Few-Shot Selector

> **Stage**: Stage 2: Pairwise Combos  
> **Difficulty**: 4.5 / 10  
> **Primary Pillars**: `VectorDB`, `LangChain`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Store 100+ task examples in a VectorDB; dynamically retrieve the top-3 most similar examples for few-shot prompts.

---

## 🧠 Key Concepts Covered
- **SemanticSimilarityExampleSelector**
- **Dynamic Prompts**
- **Few-Shot Optimization**

---

## 🏗️ Architecture & Control Flow
```text
User Input -> VectorDB similarity search over example repository -> Top-3 Examples -> Prompt Template -> Model
```

---

## 📂 Project Structure
```text
043_vectordb_langchain_dynamic_few_shot/
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
- [ ] Key architectural patterns for `VectorDB`, `LangChain` are explicitly demonstrated.
- [ ] Auxiliary production concerns (None (Core Focus)) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
