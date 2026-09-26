# Project 023: Relational Database & SQL Inspection MCP Server

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 3.0 / 10 (Intermediate)  
> **Primary Pillars**: `MCP`  
> **Auxiliary Disciplines**: `Guardrails`  

---

## 🎯 Learning Objective
Construct an MCP server exposing read-only SQL queries with strict SQL injection and write-block guardrails.

---

## 🧠 Key Concepts Covered
- **Database Tools**
- **Read-Only Enforcers**
- **SQL Guardrails**
- **Schema Introspection**

---

## 🏗️ Architecture & Control Flow
```text
LLM -> MCP Call (read_query) -> SQL Guardrail Filter -> SQLite Engine -> Tabular JSON Result
```

---

## 📂 Project Structure
```text
023_only_mcp_database_sql_server/
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
- [ ] Key architectural patterns for `MCP` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Guardrails`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
