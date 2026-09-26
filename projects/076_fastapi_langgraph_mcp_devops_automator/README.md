# Project 076: FastAPI + LangGraph + MCP: Self-Healing DevOps Automator

> **Stage**: Stage 3: Triad Combos  
> **Difficulty**: 7.5 / 10  
> **Primary Pillars**: `FastAPI`, `LangGraph`, `MCP`  
> **Auxiliary Disciplines**: `Guardrails`  

---

## 🎯 Learning Objective
Alert webhook triggers LangGraph workflow: inspects server logs via MCP, diagnoses incident, runs guarded remediation.

---

## 🧠 Key Concepts Covered
- **Incident Remediation**
- **Self-Healing State Graph**
- **MCP Diagnostic Tools**
- **Action Guardrails**

---

## 🏗️ Architecture & Control Flow
```text
POST /alerts/webhook -> LangGraph diagnoses issue -> Calls guarded MCP tool to restart pod -> Verifies -> END
```

---

## 📂 Project Structure
```text
076_fastapi_langgraph_mcp_devops_automator/
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
- [ ] Key architectural patterns for `FastAPI`, `LangGraph`, `MCP` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Guardrails`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
