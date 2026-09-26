# Project 092: Autonomous Enterprise ERP & Supply Chain Invoice Auditor

> **Stage**: Stage 4: Quad Enterprise Systems  
> **Difficulty**: 9.0 / 10  
> **Primary Pillars**: `FastAPI`, `LangGraph`, `MCP`, `RAG`  
> **Auxiliary Disciplines**: `Guardrails`  

---

## 🎯 Learning Objective
Enterprise supply chain workflow: Ingests supplier invoices, queries inventory databases via MCP, verifies SLA policies via RAG with audit guardrails.

---

## 🧠 Key Concepts Covered
- **ERP Integration**
- **SQL Inventory MCP**
- **SLA Policy RAG**
- **Financial Audit Guardrails**

---

## 🏗️ Architecture & Control Flow
```text
Invoice Ingested -> Extract Line Items -> Verify Stock in SQL via MCP -> Check SLA Penalties via RAG -> Approved/Flagged
```

---

## 📂 Project Structure
```text
092_fastapi_langgraph_mcp_rag_erp_workflow/
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
- [ ] Key architectural patterns for `FastAPI`, `LangGraph`, `MCP`, `RAG` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Guardrails`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
