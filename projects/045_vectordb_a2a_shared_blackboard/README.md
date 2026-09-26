# Project 045: VectorDB + A2A: Collaborative Multi-Agent Blackboard Memory

> **Stage**: Stage 2: Pairwise Combos  
> **Difficulty**: 5.5 / 10  
> **Primary Pillars**: `VectorDB`, `A2A`  
> **Auxiliary Disciplines**: `Multi-Agent Systems`, `Agent Memory`  

---

## 🎯 Learning Objective
Create a shared semantic vector memory space where multi-agent swarms post findings and search peer discoveries.

---

## 🧠 Key Concepts Covered
- **Multi-Agent Blackboard**
- **Shared Semantic Memory**
- **Agent Fact Tagging**
- **Knowledge Propagation**

---

## 🏗️ Architecture & Control Flow
```text
Agent A -> VectorDB.insert(topic, source='Agent A') -> Agent B queries VectorDB -> Synthesizes
```

---

## 📂 Project Structure
```text
045_vectordb_a2a_shared_blackboard/
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
- [ ] Key architectural patterns for `VectorDB`, `A2A` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Multi-Agent Systems`, `Agent Memory`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
