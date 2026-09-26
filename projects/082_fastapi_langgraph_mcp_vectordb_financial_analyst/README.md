# Project 082: Autonomous Financial Analyst with SEC Filings & SQL Tools

> **Stage**: Stage 4: Quad Enterprise Systems  
> **Difficulty**: 8.5 / 10  
> **Primary Pillars**: `FastAPI`, `LangGraph`, `MCP`, `VectorDB`  
> **Auxiliary Disciplines**: `Guardrails`  

---

## 🎯 Learning Objective
Market intelligence API querying SQL financial tables via MCP, comparing with SEC 10-K vector filings with hallucination guardrails.

---

## 🧠 Key Concepts Covered
- **Financial SQL MCP**
- **SEC 10-K Vector Store**
- **Hallucination Guardrails**
- **Audited Output Schema**

---

## 🏗️ Architecture & Control Flow
```text
User Request -> LangGraph Analyst -> Query balance sheet via MCP -> Query 10-K via VectorDB -> Guardrail Verification -> Report
```

---

## 📂 Project Structure
```text
082_fastapi_langgraph_mcp_vectordb_financial_analyst/
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
- [ ] Key architectural patterns for `FastAPI`, `LangGraph`, `MCP`, `VectorDB` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Guardrails`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
