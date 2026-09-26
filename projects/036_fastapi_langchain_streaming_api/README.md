# Project 036: FastAPI + LangChain: Token Streaming API with LangSmith Tracing

> **Stage**: Stage 2: Pairwise Combos  
> **Difficulty**: 4.0 / 10  
> **Primary Pillars**: `FastAPI`, `LangChain`  
> **Auxiliary Disciplines**: `LangSmith`  

---

## 🎯 Learning Objective
Build a production-grade FastAPI microservice streaming LCEL tokens via SSE with automatic LangSmith run tracking.

---

## 🧠 Key Concepts Covered
- **StreamingResponse**
- **chain.astream()**
- **SSE Formatting**
- **LangSmith Run Telemetry**

---

## 🏗️ Architecture & Control Flow
```text
Client -> POST /chat/stream -> LCEL Chain streaming tokens (traced in LangSmith) -> FastAPI SSE Generator
```

---

## 📂 Project Structure
```text
036_fastapi_langchain_streaming_api/
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
- [ ] Key architectural patterns for `FastAPI`, `LangChain` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`LangSmith`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
