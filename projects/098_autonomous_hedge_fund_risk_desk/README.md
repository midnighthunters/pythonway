# Project 098: Project Alpha: Autonomous Quant Hedge Fund & Risk Desk

> **Stage**: Stage 5: Pinnacle Full-Stack Ecosystems  
> **Difficulty**: 10.0 / 10 (Mastery)  
> **Primary Pillars**: `FastAPI`, `LangGraph`, `LangChain`, `VectorDB`, `RAG`, `MCP`, `A2A`  
> **Auxiliary Disciplines**: `Multi-Agent Systems`, `Guardrails`, `AI Evaluation`  

---

## 🎯 Learning Objective
Autonomous fund: Ingests market news via RAG, queries tick databases via MCP, runs Bull vs Bear A2A debate, passes risk committee HITL, streams terminal via FastAPI.

---

## 🧠 Key Concepts Covered
- **Quantitative Financial Reasoning**
- **Adversarial Market Debate**
- **Algorithmic Risk Guardrails**
- **Streaming Trading Terminal**
- **Portfolio Risk Evaluation**

---

## 🏗️ Architecture & Control Flow
```text
Market News (RAG) + Tick Data (MCP) -> Bull vs Bear Agents (A2A) -> LangGraph Risk Committee -> HITL Signoff -> FastAPI Stream
```

---

## 📂 Project Structure
```text
098_autonomous_hedge_fund_risk_desk/
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
- [ ] Key architectural patterns for `FastAPI`, `LangGraph`, `LangChain`, `VectorDB`, `RAG`, `MCP`, `A2A` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Multi-Agent Systems`, `Guardrails`, `AI Evaluation`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
