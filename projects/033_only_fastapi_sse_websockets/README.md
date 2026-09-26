# Project 033: Real-Time Streaming: Server-Sent Events (SSE) & WebSockets

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 3.0 / 10 (Intermediate)  
> **Primary Pillars**: `FastAPI`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Implement HTTP StreamingResponse with text/event-stream (SSE) and full-duplex WebSocket connections for AI tokens.

---

## 🧠 Key Concepts Covered
- **StreamingResponse**
- **Server-Sent Events (SSE)**
- **WebSocket Endpoints**
- **Connection Manager**

---

## 🏗️ Architecture & Control Flow
```text
Client -> EventSource / WS Connection -> FastAPI Async Generator -> Chunk-by-chunk stream
```

---

## 📂 Project Structure
```text
033_only_fastapi_sse_websockets/
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
- [ ] Key architectural patterns for `FastAPI` are explicitly demonstrated.
- [ ] Auxiliary production concerns (None (Core Focus)) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
