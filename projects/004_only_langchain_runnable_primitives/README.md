# Project 004: Advanced LCEL: RunnableParallel, Passthrough & Lambdas

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 2.5 / 10 (Intermediate)  
> **Primary Pillars**: `LangChain`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Master advanced data plumbing and non-linear DAG composition in LangChain Expression Language (LCEL): running concurrent multi-branch evaluations with `RunnableParallel`, preserving inputs with `RunnablePassthrough`, injecting computed fields with `.assign()`, and wrapping custom Python logic in `RunnableLambda`.

---

## 🧠 Key Concepts Covered
- **`RunnableParallel`**: Concurrently executing multiple independent runnable pipelines over identical inputs.
- **`RunnablePassthrough`**: Forwarding unmodified input parameters down the chain.
- **`RunnablePassthrough.assign()`**: Adding or overriding specific keys in an existing input dictionary without mutating the rest.
- **`RunnableLambda`**: Turning arbitrary Python callables, functions, or lambdas into native `Runnable` components compatible with the pipe operator (`|`).

---

## 🏗️ Architecture & Control Flow
```text
                     Technical Proposal
                             │
            ┌────────────────┴────────────────┐
            │        RunnableParallel         │
            ▼                ▼                ▼
     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
     │   Security   │ │    FinOps    │ │   Velocity   │
     │    Branch    │ │    Branch    │ │    Branch    │
     └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
            └────────────────┬────────────────┘
                             ▼
              RunnablePassthrough.assign()  (injects calculated risk_tier)
                             │
                             ▼
                    CTO Synthesis Prompt
                             │
                             ▼
                      ChatGroq Engine
                             │
                             ▼
                    Final Executive Memo
```

---

## 📂 Project Structure
```text
004_only_langchain_runnable_primitives/
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

1. **How does `RunnableParallel` improve system throughput compared to sequential chaining?**
   * *Answer*: When multiple LLM calls are independent (e.g. assessing security, cost, and velocity), `RunnableParallel` triggers them concurrently using thread pools or async event loops. This reduces total latency from $T_1 + T_2 + T_3$ down to approximately $\max(T_1, T_2, T_3)$.

2. **What is the difference between `RunnablePassthrough()` and `RunnablePassthrough.assign()`?**
   * *Answer*: `RunnablePassthrough()` passes its exact input through unchanged. `RunnablePassthrough.assign(new_key=...)` takes an existing dictionary input, calculates the value for `new_key`, and returns the original dictionary merged with the new key-value pair.

3. **Can any Python function be wrapped in `RunnableLambda`?**
   * *Answer*: Yes, any callable that takes a single input argument (or dictionary) can be wrapped. It instantly inherits `.invoke()`, `.batch()`, `.stream()`, and async support.

---

## 🏆 Stretch Challenge
**Task**: Modify `main.py` to add a 4th parallel branch evaluating **Legal & Regulatory Compliance (GDPR / HIPAA)**, and update the CTO synthesis prompt to reject proposals if GDPR violations are flagged.
