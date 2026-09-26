# Project 021: MCP Architecture: JSON-RPC 2.0 & Handshake Protocol

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 2.5 / 10 (Intermediate)  
> **Primary Pillars**: `MCP`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Understand the low-level Model Context Protocol (MCP) specification, stdio transport, and JSON-RPC 2.0 protocol.

---

## 🧠 Key Concepts Covered
- **JSON-RPC 2.0**
- **stdio Transport**
- **Protocol Handshake**
- **Tool/Resource Registration**

---

## 🏗️ Architecture & Control Flow
```text
Client -> JSON-RPC stdio Request -> MCP Server -> Protocol Response Handler
```

---

## 📂 Project Structure
```text
021_only_mcp_jsonrpc_protocol_basics/
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
- [ ] Key architectural patterns for `MCP` are explicitly demonstrated.
- [ ] Auxiliary production concerns (None (Core Focus)) are integrated cleanly where applicable.
- [ ] Concise, pedagogical terminal logging explains the internal state at every step.
