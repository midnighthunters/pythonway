# Project 005: Resilient Chains: Fallbacks, Retries & LangSmith Observability

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 3.0 / 10 (Intermediate)  
> **Primary Pillars**: `LangChain`  
> **Auxiliary Disciplines**: `LangSmith`  

---

## 🎯 Learning Objective
Master fault tolerance and enterprise reliability in LangChain: setting up automatic model fallbacks with `.with_fallbacks()`, configuring exponential backoff retries with `.with_retry()`, implementing whole-chain recovery pathways, and capturing execution traces in LangSmith.

---

## 🧠 Key Concepts Covered
- **`.with_fallbacks()`**: Seamlessly redirecting requests to backup models when primary providers experience rate limits (HTTP 429), timeouts, or downtime (HTTP 500).
- **`.with_retry()`**: Automatically retrying transient network blips with configurable backoff curves without application restarts.
- **Chain-Level Recovery**: Intercepting parsing exceptions downstream and returning safe default payloads.
- **LangSmith Observability**: Tagging runs, monitoring fallback switchover rates, and tracking latency deltas.

---

## 🏗️ Architecture & Control Flow
```text
                       Incoming Request
                              │
                              ▼
┌───────────────────────────────────────────────────────────┐
│               Primary LLM (Fails / Times Out)             │
└─────────────────────────────┬─────────────────────────────┘
                              │
                              │ [Exception Caught]
                              ▼
┌───────────────────────────────────────────────────────────┐
│              .with_fallbacks([Backup LLM])                │  switches transparently
└─────────────────────────────┬─────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────┐
│                    StrOutputParser                        │
└─────────────────────────────┬─────────────────────────────┘
                              │
                              ▼
                     Clean Response String
               (Fallback Trace logged in LangSmith)
```

---

## 📂 Project Structure
```text
005_only_langchain_fallbacks_and_retries/
├── README.md              # Project specifications, self-quiz & stretch challenge
├── requirements.txt       # Dependencies for this project
├── config.py              # Groq model and environment configuration
├── main.py                # Pedagogical runnable demonstration
└── test_verification.py   # Automated assertion tests
```

---

## 🚀 Execution & Verification Guide

### 1. Run Main Demonstration
```bash
python main.py
```

### 2. Run Automated Verification Tests
```bash
python test_verification.py
```

---

## 📝 Self-Assessment Interview Quiz (Test Your Understanding)

1. **What types of errors should trigger `.with_fallbacks()` versus `.with_retry()`?**
   * *Answer*: Use `.with_retry()` for transient, recoverable errors (e.g. socket timeouts, momentary network disconnects, HTTP 503). Use `.with_fallbacks()` for persistent or quota-based errors (e.g. HTTP 429 rate limit exceeded, model deprecation/404, or complete provider downtime).

2. **Can `.with_fallbacks()` be applied to entire LCEL chains, or only to individual models?**
   * *Answer*: It can be applied to **any** `Runnable`, including full chains. For example, `(prompt | complex_model | strict_parser).with_fallbacks([simple_fallback_chain])` protects against both model errors and output parsing failures.

3. **In LangSmith, how does a fallback execution appear in the trace tree?**
   * *Answer*: LangSmith displays the parent `RunnableWithFallbacks` span. Underneath it, the failed primary child span shows an `Error` status with the exception traceback, followed immediately by a successful child span for the fallback model, providing complete auditing transparency.

---

## 🏆 Stretch Challenge
**Task**: Build a 3-tier fallback chain:
1. Primary: Fast low-latency model
2. Secondary: High-accuracy heavy model (if primary throws an exception)
3. Tertiary: Static cached dictionary response (if both models are unreachable)
Log a custom alert message whenever the tertiary fallback is activated.
