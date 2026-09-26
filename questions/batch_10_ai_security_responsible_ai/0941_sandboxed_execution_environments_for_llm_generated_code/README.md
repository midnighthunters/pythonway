# Q0941 · Sandboxed execution environments for LLM-generated code

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Agent security | Hard |

## Question

Explain how sandboxed runtimes (gVisor, Firecracker, WebAssembly) safely execute LLM-generated Python code, and write Python code simulating resource-limited subprocess execution.

## Answer

LLMs generating and executing Python code (e.g. data analysis, chart generation) represent extreme security risks. If run in the main application environment, the code can execute `os.system("rm -rf /")` or read memory secrets.

Isolation mechanisms:
1. **gVisor (runsc)**: Intercepts and virtualizes Linux syscalls in user space.
2. **Firecracker microVMs**: Boots dedicated minimal Linux kernels in < 5ms with hardware virtualization.
3. **Subprocess Resource Limits (`prlimit` / `resource`)**: Restricts CPU time, memory limits, and disables network access.

```python
import subprocess
import sys


def execute_sandboxed_snippet(code: str, timeout_sec: float = 2.0) -> dict:
    """Executes code in an isolated subprocess with strict timeouts."""
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
        return {
            "success": proc.returncode == 0,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "returncode": proc.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Execution timed out (infinite loop protection)"}


# Safe calculation
res1 = execute_sandboxed_snippet("print(sum([i*2 for i in range(10)]))")
assert res1["success"] is True
assert res1["stdout"] == "90"

# Infinite loop protection
res2 = execute_sandboxed_snippet("while True: pass", timeout_sec=0.1)
assert res2["success"] is False
assert "timed out" in res2["error"]
```

## Likely follow-ups

- Why is Python's built-in `exec()` with a restricted `globals` dictionary fundamentally insecure?
- How does WebAssembly (WASM) provide deterministic, memory-safe execution inside browsers and servers?

---

[← Q0940](../../batch_10_ai_security_responsible_ai/0940_server_side_request_forgery_prevention_in_agent_web/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0942 →](../../batch_10_ai_security_responsible_ai/0942_limiting_file_system_access_in_agent_tools/README.md)
