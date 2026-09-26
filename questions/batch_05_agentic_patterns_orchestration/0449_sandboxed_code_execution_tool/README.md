# Q0449 · Sandboxed code execution tool

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Tooling | Hard |

## Question

Implement a code-execution tool that runs model-written Python in a separate isolated interpreter process with a timeout, a cleared environment and capped output. Explain why a subprocess alone is not a sufficient sandbox.

## Answer

```python
import subprocess
import sys


def run_python(code: str, timeout: float = 2.0, max_output: int = 2_000) -> dict:
    try:
        proc = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, timeout=timeout,
                              env={"PYTHONIOENCODING": "utf-8", "SYSTEMROOT": __import__("os").environ.get("SYSTEMROOT", "")})
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"timed out after {timeout}s"}
    out = (proc.stdout + proc.stderr)[:max_output]
    return {"ok": proc.returncode == 0, "exit_code": proc.returncode, "output": out}


assert run_python("print(sum(range(10)))") == {"ok": True, "exit_code": 0, "output": "45\n"}
assert run_python("while True: pass", timeout=1.0)["error"].startswith("timed out")
leak = run_python("import os; print(os.environ.get('OPENAI_API_KEY'))")
assert leak["output"].strip() == "None"
assert not run_python("raise SystemExit(3)")["ok"]
```

`-I` is isolated mode: it ignores environment variables and the user site-packages. The cleared `env` keeps secrets out of the child (`SYSTEMROOT` is only there because Windows needs it). The timeout stops runaway loops.

A subprocess still runs as the same OS user, with filesystem and network access. Production sandboxes use containers or microVMs (gVisor, Firecracker, managed code interpreters) with no network (or an egress allowlist), a read-only filesystem plus a scratch directory, CPU, memory and process limits, non-root users, and per-run disposal. Treat all model-written code as untrusted.

## Likely follow-ups

- What resources must a production code sandbox limit besides time?

---

[← Q0448](../../batch_05_agentic_patterns_orchestration/0448_scope_tools_to_the_task_with_capability_tokens/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0450 →](../../batch_05_agentic_patterns_orchestration/0450_computer_use_and_browser_agents/README.md)
