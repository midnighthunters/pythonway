# Project 072: LangGraph + A2A + RAG: Adversarial Fact-Checking with LLM Judge

> **Stage**: Stage 3: Triad Combos  
> **Difficulty**: 7.5 / 10  
> **Primary Pillars**: `LangGraph`, `A2A`, `RAG`  
> **Auxiliary Disciplines**: `Multi-Agent Systems`, `AI Evaluation`  

---

## 🎯 Learning Objective
Generator Agent drafts assertions; Critic Agent queries RAG to verify facts; Judge Agent evaluates veracity score.

---

## 🧠 Key Concepts Covered
- **Multi-Agent Fact-Checking**
- **LLM-as-a-Judge Evaluation**
- **Claim Extraction Node**
- **Truth Scoring**

---

## 🏗️ Architecture & Control Flow
```text
Drafting Agent -> Extract Claims -> Fact-Checker Agent verifies against RAG -> Judge scores -> [Pass | Revise]
```

---

## 📂 Project Structure
```text
072_langgraph_a2a_rag_adversarial_factchecker/
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
- [ ] Key architectural patterns for `LangGraph`, `A2A`, `RAG` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Multi-Agent Systems`, `AI Evaluation`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
