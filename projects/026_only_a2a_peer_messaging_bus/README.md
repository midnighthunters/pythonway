# Project 026: Peer-to-Peer Agent Messaging Protocol & Addressing

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 2.5 / 10 (Intermediate)  
> **Primary Pillars**: `A2A`  
> **Auxiliary Disciplines**: `Multi-Agent Systems`  

---

## 🎯 Learning Objective
Build a multi-agent peer-to-peer message envelope system with unique agent IDs, conversational thread routing, and mailboxes.

---

## 🧠 Key Concepts Covered
- **A2A Message Envelopes**
- **Agent Addressing**
- **Multi-Agent Protocol**
- **Conversation Threading**

---

## 🏗️ Architecture & Control Flow
```text
Agent A -> MessageEnvelope(sender, recipient, payload) -> Message Bus -> Agent B Mailbox
```

---

## 📂 Project Structure
```text
026_only_a2a_peer_messaging_bus/
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
