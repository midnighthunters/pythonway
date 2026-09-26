# Project 064: LangGraph + MCP + A2A: Autonomous Multi-Agent Dev Team

> **Stage**: Stage 3: Triad Combos  
> **Difficulty**: 7.5 / 10  
> **Primary Pillars**: `LangGraph`, `MCP`, `A2A`  
> **Auxiliary Disciplines**: `Multi-Agent Systems`  

---

## 🎯 Learning Objective
Product Owner, Coder, and Tester agents collaborating in LangGraph, executing code tests via an MCP filesystem server.

---

## 🧠 Key Concepts Covered
- **Multi-Agent System**
- **Role State Transitions**
- **MCP Code Execution**
- **Feedback Cycles**

---

## 🏗️ Architecture & Control Flow
```text
Product Owner -> Coder Agent -> Code Reviewer -> Tester Agent (executes via MCP) -> Loop until green
```

---

## 📂 Project Structure
```text
064_langgraph_mcp_a2a_dev_team/
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
- [ ] Key architectural patterns for `LangGraph`, `MCP`, `A2A` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Multi-Agent Systems`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
