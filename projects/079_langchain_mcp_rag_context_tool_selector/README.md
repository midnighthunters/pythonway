# Project 079: LangChain + MCP + RAG: Context-Aware Dynamic Tool Selector

> **Stage**: Stage 3: Triad Combos  
> **Difficulty**: 7.5 / 10  
> **Primary Pillars**: `LangChain`, `MCP`, `RAG`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
In an ecosystem of 50+ MCP tools, use vector retrieval (RAG) to dynamically select only the top-3 relevant tools for prompt context.

---

## 🧠 Key Concepts Covered
- **Tool RAG (Retrieval of Tools)**
- **Prompt Bloat Prevention**
- **Dynamic Tool Binding**
- **LCEL Selection**

---

## 🏗️ Architecture & Control Flow
```text
User Query -> Vector search over 50 MCP Tool Schemas -> Top-3 Tools Bound to Model -> Accurate Execution
```

---

## 📂 Project Structure
```text
079_langchain_mcp_rag_context_tool_selector/
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
- [ ] Key architectural patterns for `LangChain`, `MCP`, `RAG` are explicitly demonstrated.
- [ ] Auxiliary production concerns (None (Core Focus)) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
