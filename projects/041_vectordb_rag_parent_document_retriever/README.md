# Project 041: VectorDB + RAG: Parent Document Retriever for Deep Context

> **Stage**: Stage 2: Pairwise Combos  
> **Difficulty**: 4.5 / 10  
> **Primary Pillars**: `VectorDB`, `RAG`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Index small sentence chunks for high-accuracy vector search, but retrieve their larger parent paragraphs for context.

---

## 🧠 Key Concepts Covered
- **Parent Document Retriever**
- **MultiVector Index**
- **Context Expansion**
- **Small-to-Big Retrieval**

---

## 🏗️ Architecture & Control Flow
```text
Doc -> [Split small child chunks + big parent docs] -> Query matches child -> Return parent doc
```

---

## 📂 Project Structure
```text
041_vectordb_rag_parent_document_retriever/
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
- [ ] Key architectural patterns for `VectorDB`, `RAG` are explicitly demonstrated.
- [ ] Auxiliary production concerns (None (Core Focus)) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
