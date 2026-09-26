# Project 085: Automated Software Factory: Jira Ticket to Verified Code PR

> **Stage**: Stage 4: Quad Enterprise Systems  
> **Difficulty**: 9.0 / 10  
> **Primary Pillars**: `FastAPI`, `LangGraph`, `A2A`, `MCP`  
> **Auxiliary Disciplines**: `Multi-Agent Systems`, `AI Evaluation`  

---

## 🎯 Learning Objective
Automated Jira ticket processor: Architect agent designs schema, Developer agent writes code via MCP filesystem, Tester agent verifies tests and code quality score.

---

## 🧠 Key Concepts Covered
- **Multi-Agent Software Swarm**
- **Code Quality Evaluation**
- **Filesystem MCP Sandbox**
- **Test Verification Loop**

---

## 🏗️ Architecture & Control Flow
```text
Jira Webhook -> Architect Agent -> Developer Agent (writes code via MCP) -> Tester Agent runs pytest -> PR Created
```

---

## 📂 Project Structure
```text
085_fastapi_langgraph_a2a_mcp_software_factory/
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
- [ ] Key architectural patterns for `FastAPI`, `LangGraph`, `A2A`, `MCP` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Multi-Agent Systems`, `AI Evaluation`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
