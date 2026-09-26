# Project 068: LangGraph + RAG + MCP: Deep Research Agent with Live Tools

> **Stage**: Stage 3: Triad Combos  
> **Difficulty**: 7.5 / 10  
> **Primary Pillars**: `LangGraph`, `RAG`, `MCP`  
> **Auxiliary Disciplines**: `AI Evaluation`  

---

## 🎯 Learning Objective
Research agent combining local document RAG with live external web tools provided over an MCP server and fact evaluation.

---

## 🧠 Key Concepts Covered
- **Local vs Remote Context**
- **MCP Web Tools**
- **Iterative Synthesis**
- **Fact Evaluation**

---

## 🏗️ Architecture & Control Flow
```text
Question -> Query Local RAG -> If Gaps Found -> Call MCP Web Tool -> Synthesize Master Research Brief
```

---

## 📂 Project Structure
```text
068_langgraph_rag_mcp_live_researcher/
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
- [ ] Key architectural patterns for `LangGraph`, `RAG`, `MCP` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`AI Evaluation`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
