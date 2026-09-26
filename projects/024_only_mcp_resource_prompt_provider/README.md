# Project 024: Dynamic Resources & Reusable Prompt Templates via MCP

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 3.5 / 10 (Intermediate)  
> **Primary Pillars**: `MCP`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Implement dynamic MCP Resources (live application logs, system metrics) and server-side Prompt templates.

---

## 🧠 Key Concepts Covered
- **MCP Resources**
- **Resource Subscriptions**
- **MCP Prompt Templates**
- **URI Schemes (system://)**

---

## 🏗️ Architecture & Control Flow
```text
Client -> Read Resource URI -> MCP Server returns dynamic streaming context -> LLM Context
```

---

## 📂 Project Structure
```text
024_only_mcp_resource_prompt_provider/
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
- [ ] Auxiliary production concerns (None (Core Focus)) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
