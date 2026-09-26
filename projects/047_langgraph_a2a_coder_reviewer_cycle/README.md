# Project 047: LangGraph + A2A: Multi-Agent Coder-Reviewer Dual Loop

> **Stage**: Stage 2: Pairwise Combos  
> **Difficulty**: 5.0 / 10  
> **Primary Pillars**: `LangGraph`, `A2A`  
> **Auxiliary Disciplines**: `Multi-Agent Systems`  

---

## 🎯 Learning Objective
Model an autonomous multi-agent pair: Coder Agent writes code, Reviewer Agent analyzes lint/bugs, loops until 100% clean.

---

## 🧠 Key Concepts Covered
- **Multi-Agent System Loop**
- **Review Cycles**
- **Exit Criteria Nodes**
- **Agent Code Iteration**

---

## 🏗️ Architecture & Control Flow
```text
Coder Node (Drafts Code) -> Reviewer Node (Tests Code) -> [Bugs? Loop to Coder | Clean? -> END]
```

---

## 📂 Project Structure
```text
047_langgraph_a2a_coder_reviewer_cycle/
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
- [ ] Key architectural patterns for `LangGraph`, `A2A` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Multi-Agent Systems`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
