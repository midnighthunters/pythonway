# Project 009: Human-in-the-Loop (HITL), Interrupts & State Modification

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 3.5 / 10 (Intermediate)  
> **Primary Pillar**: `LangGraph`  
> **Auxiliary Disciplines**: Production Guardrails & Governance  

---

## 🎯 Learning Objective
Master Human-in-the-Loop (HITL) workflows in LangGraph by setting breakpoints using `interrupt_before`, inspecting paused execution states, mutating state out-of-band with `update_state()`, and resuming execution seamlessly with `invoke(None, config)`.

---

## 🧠 Key Concepts Covered

1. **Deterministic Breakpoints (`interrupt_before`)**:
   - Compiling a graph with `builder.compile(checkpointer=memory, interrupt_before=["node_name"])` causes execution to automatically pause right before entering `node_name`.
   - The graph state is completely preserved in the checkpointer.
2. **State Inspection at Breakpoints**:
   - Calling `snapshot = graph.get_state(config)` on an interrupted thread reveals:
     - `snapshot.next`: A tuple showing the exact node waiting to execute next (e.g. `('execution_gate',)`).
     - `snapshot.values`: The full dictionary of accumulated state values.
3. **Out-of-Band State Mutation (`update_state`)**:
   - An administrator or human operator can alter the pending state without re-running earlier nodes:
     ```python
     graph.update_state(config, values={"amount": 22000.0, "human_approved": True})
     ```
   - This records a new checkpoint snapshot capturing the human edit.
4. **Resuming Execution (`invoke(None, config)`)**:
   - To resume a paused thread from its latest checkpoint, pass `None` (or empty dictionary) as the input payload:
     ```python
     graph.invoke(None, config=config)
     ```
   - Execution picks up right at the waiting node and continues to completion.

---

## 🏗️ Architecture & Control Flow

```mermaid
flowchart TD
    START([START]) --> Proposal[proposal_node: Parse Wire Request]
    Proposal --> Breakpoint{PAUSE: interrupt_before}
    
    subgraph Human_Intervention [Human-in-the-Loop Gate]
        Breakpoint -.-> Inspect[graph.get_state: Manager Reviews]
        Inspect -.-> Modify[graph.update_state: Approve / Reject / Edit Amount]
        Modify -.-> Resume[graph.invoke(None, config)]
    end
    
    Resume --> Gate[execution_gate_node]
    Gate --> END([END: Settled or Rejected])
```

---

## 📂 Project Structure

```text
009_only_langgraph_human_in_the_loop/
├── README.md              # Documentation, quiz & challenge
├── requirements.txt       # Dependencies
├── config.py              # LLM client & fallback resolution
├── main.py                # Financial wire transfer HITL workflow
└── test_verification.py   # Automated assertion test suite
```

---

## 🚀 Execution & Verification

### 1. Run the Main Demonstration
```bash
python main.py
```
*Observe two scenarios: (1) A high-value transfer paused, reviewed, discounted by $3,000, and approved by a supervisor; (2) A suspicious transfer rejected at the gate.*

### 2. Run the Automated Test Suite
```bash
python test_verification.py
```

---

## 💡 Concept Self-Quiz (Test Your Understanding)

1. **Question**: Why is a checkpointer mandatory when using `interrupt_before` or `interrupt_after`?
   - **Answer**: Without a checkpointer, there is no storage engine to snapshot the graph's execution point and state values when execution halts. When an interrupt is triggered, the thread must persist its state so that a future process or HTTP request can query it and resume execution.

2. **Question**: What is the difference between `interrupt_before` and `interrupt_after`?
   - **Answer**: `interrupt_before=["node_A"]` pauses execution immediately prior to running `node_A`, allowing a human to inspect inputs and modify arguments before the action occurs. `interrupt_after=["node_A"]` runs `node_A` first, then pauses immediately after, allowing a human to review the output or artifacts of `node_A` before downstream nodes consume them.

3. **Question**: When calling `graph.invoke(None, config)` to resume, why is `None` passed as the first argument?
   - **Answer**: Passing `None` signals to LangGraph: "Do not inject a new input payload; instead, resume execution directly from the state snapshot already stored in the checkpointer for this thread."

---

## 🛠️ Hands-on Stretch Challenge

Modify `main.py` to implement **Dynamic Conditional Approval Routing**:
- Only halt for human approval if `risk_level == "HIGH"` (amount >= $10,000).
- If `risk_level == "LOW"` (amount < $10,000), bypass the human approval gate and execute immediately.
- Re-run `main.py` to verify that small transactions process autonomously while large transactions pause for manager sign-off.
