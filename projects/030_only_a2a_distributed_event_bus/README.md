# Project 030: Asynchronous Pub/Sub Agent Event Bus with Dead Letters

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 3.5 / 10 (Intermediate)  
> **Primary Pillars**: `A2A`  
> **Auxiliary Disciplines**: `Multi-Agent Systems`  

---

## 🎯 Learning Objective
Build an asynchronous agent event bus with topic subscriptions, message filtering, and dead-letter handling.

---

## 🧠 Key Concepts Covered
- **Pub/Sub Architecture**
- **Topic Subscriptions**
- **Dead-Letter Queues**
- **Async Event Processing**

---

## 🏗️ Architecture & Control Flow
```text
Publisher Agent -> Event Bus (Topic: 'security_alert') -> Subscriber Agents 1, 2, 3
```

---

## 📂 Project Structure
```text
030_only_a2a_distributed_event_bus/
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
- [ ] Key architectural patterns for `A2A` are explicitly demonstrated.
- [ ] Auxiliary production concerns (`Multi-Agent Systems`) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
