# Q0668 · Contract Net Protocol in A2A multi-agent systems

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A orchestration | Hard |

## Question

Explain the Contract Net Protocol (CNP) for task allocation in multi-agent systems and its relevance to enterprise A2A architectures.

## Answer

Contract Net Protocol (CNP) is a market-driven negotiation protocol for decentralized task allocation among autonomous agents:

Roles:
1. Manager (Initiator): An agent with a complex goal that requires subcontracting.
2. Contractors (Bidders): Specialized agents that can evaluate their availability, cost, and capability to perform a task.

Lifecycle Phases:
1. Call for Proposal (CFP): Manager broadcasts task requirements (e.g. "Reconcile 10,000 trades within 60 seconds; max cost $5").
2. Bidding: Contractors evaluate the specification and respond with bids (e.g. estimated latency, price/token cost, accuracy confidence score), or refuse.
3. Award / Rejection: Manager compares bids, awards the contract to the best bidder, and sends rejection notices to the others.
4. Execution & Reporting: Awarded contractor executes the task and sends the final result back to the manager.

Relevance to Banks: Dynamically assigns analytical workloads (e.g. bond pricing, OCR on scanned loan docs) to the most cost-effective or least-loaded agent cluster.

## Likely follow-ups

- What bidding criteria beyond price are relevant in financial systems?
- How does CNP handle situations where no contractors submit acceptable bids?

---

[← Q0667](../../batch_07_mcp_a2a_skills_assistants/0667_implementing_an_a2a_peer_to_peer_messaging_bus/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0669 →](../../batch_07_mcp_a2a_skills_assistants/0669_implementing_a2a_call_for_proposal_and_bidding/README.md)
