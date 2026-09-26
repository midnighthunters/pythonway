# Project 046: LangGraph + MCP: ReAct Agent Connected to External MCP

> **Stage**: Stage 2: Pairwise Combos  
> **Difficulty**: 5.0 / 10  
> **Primary Pillars**: `LangGraph`, `MCP`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Equip a LangGraph ReAct agent with tools dynamically exposed by a standalone external Model Context Protocol server.

---

## 🧠 Key Concepts Covered
- **MCP Tool Invocation**
- **LangGraph ToolNode**
- **External Tool Protocol**
- **Schema Marshalling**

---

## 🏗️ Architecture & Control Flow
```text
LangGraph Agent Node -> Decides MCP Tool Call -> ToolNode invokes external MCP Server -> Cycles back -> Answer
```

---

## 📂 Project Structure
```text
046_langgraph_mcp_tool_integration/
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
- [ ] Key architectural patterns for `LangGraph`, `MCP` are explicitly demonstrated.
- [ ] Auxiliary production concerns (None (Core Focus)) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
