# Project 066: FastAPI + LangGraph + HITL: Audited Compliance & Safety Guardrails

> **Stage**: Stage 3: Triad Combos  
> **Difficulty**: 7.0 / 10  
> **Primary Pillars**: `FastAPI`, `LangGraph`, `VectorDB`  
> **Auxiliary Disciplines**: `Guardrails`  

---

## 🎯 Learning Objective
Financial action graph: pauses at compliance threshold, enforces safety guardrails, sends approval request to FastAPI.

---

## 🧠 Key Concepts Covered
- **Compliance Thresholds**
- **Safety Guardrails**
- **interrupt_before**
- **FastAPI Approval Queue**

---

## 🏗️ Architecture & Control Flow
```text
Request -> LangGraph (flags safety guardrail) -> Pauses -> Human reviews in API -> Approve -> Resume -> Execute
```

---

## 📂 Project Structure
```text
066_fastapi_langgraph_hitl_compliance/
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
- [ ] Auxiliary production concerns (`Guardrails`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
