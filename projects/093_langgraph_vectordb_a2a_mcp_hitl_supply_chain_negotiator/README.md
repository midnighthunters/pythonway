# Project 093: B2B Autonomous Procurement & Price Negotiator Swarm

> **Stage**: Stage 4: Quad Enterprise Systems  
> **Difficulty**: 9.5 / 10  
> **Primary Pillars**: `LangGraph`, `VectorDB`, `A2A`, `MCP`  
> **Auxiliary Disciplines**: `Multi-Agent Systems`, `Agent Memory`, `Guardrails`  

---

## 🎯 Learning Objective
Supplier price negotiator: Evaluates historical pricing memory, coordinates buyer/supplier agents, requests human manager signoff on deals >$10k.

---

## 🧠 Key Concepts Covered
- **Multi-Agent Negotiation Protocol**
- **Historical Pricing Memory**
- **MCP Order Placement**
- **Manager Approval Guardrail**

---

## 🏗️ Architecture & Control Flow
```text
Procurement Request -> Pricing VectorDB Analysis -> Buyer Agent bargains with Supplier Agent -> [HITL if >$10k] -> Order Placed
```

---

## 📂 Project Structure
```text
093_langgraph_vectordb_a2a_mcp_hitl_supply_chain_negotiator/
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
- [ ] Key architectural patterns for `LangGraph`, `VectorDB`, `A2A`, `MCP` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Multi-Agent Systems`, `Agent Memory`, `Guardrails`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
