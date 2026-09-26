# Project 018: Contextual Compression & Cross-Encoder Re-ranking

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 3.0 / 10 (Intermediate)  
> **Primary Pillars**: `RAG`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Eliminate irrelevant noise and reduce prompt token overhead using cross-encoder re-ranking models.

---

## 🧠 Key Concepts Covered
- **Cross-Encoder Re-ranking**
- **Contextual Compression**
- **FlashRank**
- **Token Efficiency**

---

## 🏗️ Architecture & Control Flow
```text
Retrieved Chunks (Top-20) -> Cross-Encoder Scorer -> Filtered Relevant Chunks (Top-3) -> LLM
```

---

## 📂 Project Structure
```text
018_only_rag_reranking_compression/
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
- [ ] Auxiliary production concerns (None (Core Focus)) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
