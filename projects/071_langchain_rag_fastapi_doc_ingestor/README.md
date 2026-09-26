# Project 071: FastAPI + LangChain + RAG: Real-Time Document Ingestion API

> **Stage**: Stage 3: Triad Combos  
> **Difficulty**: 6.5 / 10  
> **Primary Pillars**: `FastAPI`, `LangChain`, `RAG`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
File upload endpoint accepting PDFs/Markdown, chunking via text splitters, indexing, and enabling immediate Q&A.

---

## 🧠 Key Concepts Covered
- **Async File Uploads**
- **Ingestion Background Task**
- **Dynamic Knowledge Base**
- **LCEL Q&A**

---

## 🏗️ Architecture & Control Flow
```text
POST /upload -> Background Chunking & Embedding -> Index Ready -> POST /ask queries new document
```

---

## 📂 Project Structure
```text
071_langchain_rag_fastapi_doc_ingestor/
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
- [ ] Key architectural patterns for `FastAPI`, `LangChain`, `RAG` are explicitly demonstrated.
- [ ] Auxiliary production concerns (None (Core Focus)) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
