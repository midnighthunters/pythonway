# Project 074: LangGraph + MCP + VectorDB: Autonomous BI Data Analyst

> **Stage**: Stage 3: Triad Combos  
> **Difficulty**: 7.5 / 10  
> **Primary Pillars**: `LangGraph`, `MCP`, `VectorDB`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Autonomous analyst agent querying relational SQL data via MCP and comparing with quarterly reports in VectorDB.

---

## 🧠 Key Concepts Covered
- **SQL MCP Tool**
- **Unstructured Vector Match**
- **Data Reconciliation**
- **Analytical Brief Generation**

---

## 🏗️ Architecture & Control Flow
```text
Query -> Pull SQL Aggregates via MCP -> Pull Qualitative Commentary from VectorDB -> Reconcile & Output
```

---

## 📂 Project Structure
```text
074_langgraph_mcp_vectordb_data_analyst/
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
- [ ] Key architectural patterns for `LangGraph`, `MCP`, `VectorDB` are explicitly demonstrated.
- [ ] Auxiliary production concerns (None (Core Focus)) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
