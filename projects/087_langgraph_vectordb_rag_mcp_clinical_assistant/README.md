# Project 087: Evidence-Based Clinical Decision Support & Dosage Calculator

> **Stage**: Stage 4: Quad Enterprise Systems  
> **Difficulty**: 9.0 / 10  
> **Primary Pillars**: `LangGraph`, `VectorDB`, `RAG`, `MCP`  
> **Auxiliary Disciplines**: `Guardrails`  

---

## 🎯 Learning Objective
Evidence-based medical query assistant checking PubMed vector papers, calculating drug dosages via MCP tools, with human physician approval gate and medical guardrails.

---

## 🧠 Key Concepts Covered
- **Medical Literature RAG**
- **Clinical Calculation MCP**
- **Human Guardrail Approval**
- **Medical Safety Filter**

---

## 🏗️ Architecture & Control Flow
```text
Doctor Query -> Vector RAG (Medical Guidelines) -> MCP Dosage Calculator -> [PAUSE: HITL Guardrail] -> Prescribed Plan
```

---

## 📂 Project Structure
```text
087_langgraph_vectordb_rag_mcp_clinical_assistant/
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
- [ ] Key architectural patterns for `LangGraph`, `VectorDB`, `RAG`, `MCP` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Guardrails`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
