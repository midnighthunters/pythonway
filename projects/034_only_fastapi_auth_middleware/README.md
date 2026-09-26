# Project 034: JWT Security, Rate-Limiting & Prompt Injection Guardrails

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 3.0 / 10 (Intermediate)  
> **Primary Pillars**: `FastAPI`  
> **Auxiliary Disciplines**: `Guardrails`  

---

## 🎯 Learning Objective
Secure AI endpoints with JWT Bearer tokens, token bucket rate limiting, CORS headers, and prompt injection guardrails.

---

## 🧠 Key Concepts Covered
- **JWT Authentication**
- **Middleware**
- **Prompt Injection Guardrails**
- **Rate Limiting**
- **Global Exception Handlers**

---

## 🏗️ Architecture & Control Flow
```text
HTTP Request -> Injection Guardrail Middleware -> Rate Limiter -> JWT Auth -> Endpoint Handler
```

---

## 📂 Project Structure
```text
034_only_fastapi_auth_middleware/
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
- [ ] Auxiliary production concerns (`Guardrails`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
