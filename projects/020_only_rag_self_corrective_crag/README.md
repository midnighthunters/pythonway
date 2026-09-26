# Project 020: CRAG: Corrective RAG with AI Evaluation Metrics

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 3.5 / 10 (Intermediate)  
> **Primary Pillars**: `RAG`  
> **Auxiliary Disciplines**: `AI Evaluation`  

---

## 🎯 Learning Objective
Evaluate retrieved document relevance using AI Evaluation metrics (Faithfulness, Relevancy, Context Precision) before generating.

---

## 🧠 Key Concepts Covered
- **Corrective RAG (CRAG)**
- **Faithfulness Metric**
- **Answer Relevancy**
- **Context Precision Evaluation**

---

## 🏗️ Architecture & Control Flow
```text
Retrieved Docs -> AI Evaluation Metric Scoring -> [Pass: Generate | Fail: Query Refinement]
```

---

## 📂 Project Structure
```text
020_only_rag_self_corrective_crag/
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
- [ ] Key architectural patterns for `RAG` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`AI Evaluation`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
