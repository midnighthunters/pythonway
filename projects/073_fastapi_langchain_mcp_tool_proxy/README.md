# Project 073: FastAPI + LangChain + MCP: Secure AI Tool Proxy & Guardrails

> **Stage**: Stage 3: Triad Combos  
> **Difficulty**: 7.0 / 10  
> **Primary Pillars**: `FastAPI`, `LangChain`, `MCP`  
> **Auxiliary Disciplines**: `Guardrails`  

---

## 🎯 Learning Objective
Secure proxy server verifying API keys, enforcing tool execution guardrails, and routing tool calls between LangChain and MCP.

---

## 🧠 Key Concepts Covered
- **Tool Execution Guardrails**
- **API Key Auth**
- **Tool Invocation Telemetry**
- **LCEL Integration**

---

## 🏗️ Architecture & Control Flow
```text
LangChain Agent -> POST /proxy/tool -> FastAPI Auth & Guardrail Check -> MCP Server Execution -> Result
```

---

## 📂 Project Structure
```text
073_fastapi_langchain_mcp_tool_proxy/
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
- [ ] Key architectural patterns for `FastAPI`, `LangChain`, `MCP` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Guardrails`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
