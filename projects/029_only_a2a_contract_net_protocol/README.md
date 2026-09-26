# Project 029: Contract Net Protocol: Market-Based Task Allocation

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 3.5 / 10 (Intermediate)  
> **Primary Pillars**: `A2A`  
> **Auxiliary Disciplines**: `Multi-Agent Systems`  

---

## 🎯 Learning Objective
Implement FIPA Contract Net Protocol: Manager broadcasts Call for Proposals (CFP), Agents bid, Manager awards contract.

---

## 🧠 Key Concepts Covered
- **Contract Net Protocol (CNP)**
- **Call for Proposals (CFP)**
- **Agent Bidding**
- **Market-Based Coordination**

---

## 🏗️ Architecture & Control Flow
```text
Manager Agent -> Broadcast CFP -> Worker Agents Submit Bids -> Best Bid Awarded -> Execution
```

---

## 📂 Project Structure
```text
029_only_a2a_contract_net_protocol/
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
