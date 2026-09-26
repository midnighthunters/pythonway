# Q0681 · Sandboxing skill execution in isolated runtimes

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Agent skills | Hard |

## Question

An enterprise skill contains custom Python scripts. How do you sandbox script execution to prevent malicious code execution or data exfiltration?

## Answer

Untrusted or dynamically generated agent scripts present critical security vulnerabilities:
1. Container Isolation: Run scripts inside ephemeral rootless containers (e.g. Docker, gVisor, or AWS Firecracker microVMs) with strict CPU, memory, and disk quotas.
2. Network Isolation: Disable outbound internet access (`--network none`) or route through an enterprise proxy with a domain whitelist.
3. Read-Only Root Filesystem: Mount root as read-only, providing only an ephemeral scratch directory for intermediate calculation files.
4. Dropped Capabilities: Drop Linux kernel capabilities (`CAP_NET_RAW`, `CAP_SYS_ADMIN`), and enforce seccomp syscall filters.
5. Execution Timeouts: Enforce a hard process kill after N seconds.

## Likely follow-ups

- Why is running `exec()` inside the main agent Python process unacceptable in enterprise production?
- What are the latency overheads of spinning up Firecracker microVMs for short scripts?

---

[← Q0680](../../batch_07_mcp_a2a_skills_assistants/0680_validating_skill_configuration_and_metadata_with_pydantic/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0682 →](../../batch_07_mcp_a2a_skills_assistants/0682_skill_composition_combining_multiple_skills_for_compound/README.md)
