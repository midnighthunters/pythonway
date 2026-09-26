# Project 014: Metadata Payloads, Namespaces & Boolean Filtering

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 3.0 / 10 (Intermediate)  
> **Primary Pillars**: `VectorDB`  
> **Auxiliary Disciplines**: `Guardrails`  

---

## 🎯 Learning Objective
Execute pre-filtering with rich boolean expressions and tenant namespace guardrails to prevent data leakage.

---

## 🧠 Key Concepts Covered
- **Metadata Payloads**
- **Pre-filtering Guardrails**
- **Namespace Partitioning**
- **Filter Queries**

---

## 🏗️ Architecture & Control Flow
```text
Query Vector + Tenant Guardrail Filter -> Index Filter Engine -> Secure Top-K Results
```

---

## 📂 Project Structure
```text
014_only_vectordb_payload_metadata_filtering/
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
- [ ] Key architectural patterns for `VectorDB` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Guardrails`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
