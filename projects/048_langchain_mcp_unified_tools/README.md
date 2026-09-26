# Project 048: LangChain + MCP: Dynamically Piping MCP Tools into LCEL

> **Stage**: Stage 2: Pairwise Combos  
> **Difficulty**: 4.5 / 10  
> **Primary Pillars**: `LangChain`, `MCP`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Fetch tool declarations from an MCP server and bind them dynamically into a LangChain LCEL model execution pipeline.

---

## 🧠 Key Concepts Covered
- **Dynamic Tool Binding**
- **LCEL Tool Binding**
- **Protocol Conversion**
- **Model Tool Routing**

---

## 🏗️ Architecture & Control Flow
```text
MCP Server (tools catalog) -> Dynamic @tool conversion -> llm.bind_tools() -> LCEL Chain Execution
```

---

## 📂 Project Structure
```text
048_langchain_mcp_unified_tools/
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
- [ ] Key architectural patterns for `LangChain`, `MCP` are explicitly demonstrated.
- [ ] Auxiliary production concerns (None (Core Focus)) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
