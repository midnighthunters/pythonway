# Q0621 · Implementing a tool execution timeout

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP tools | Medium |

## Question

Write Python code implementing an execution timeout wrapper for MCP tool execution using `concurrent.futures.ThreadPoolExecutor`.

## Answer

MCP tools can call external databases, internal REST services, or remote microservices that might hang. A robust server must enforce strict per-tool timeouts to avoid blocking the host.

```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import time
from typing import Any, Callable, Dict


def execute_tool_with_timeout(
    func: Callable[..., Any], args: Dict[str, Any], timeout_seconds: float
) -> Dict[str, Any]:
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(func, **args)
        try:
            res = future.result(timeout=timeout_seconds)
            return {"content": [{"type": "text", "text": str(res)}], "isError": False}
        except TimeoutError:
            return {
                "content": [{"type": "text", "text": f"Error: Tool execution timed out after {timeout_seconds}s"}],
                "isError": True,
            }
        except Exception as exc:
            return {"content": [{"type": "text", "text": f"Error: {exc}"}], "isError": True}


def fast_tool(x: int) -> int:
    return x * 2


def hanging_tool(x: int) -> int:
    time.sleep(0.5)
    return x


ok = execute_tool_with_timeout(fast_tool, {"x": 21}, timeout_seconds=1.0)
assert ok["isError"] is False
assert ok["content"][0]["text"] == "42"

slow = execute_tool_with_timeout(hanging_tool, {"x": 21}, timeout_seconds=0.05)
assert slow["isError"] is True
assert "timed out" in slow["content"][0]["text"]
```

## Likely follow-ups

- Why does a thread pool timeout not immediately terminate the underlying worker thread?
- How can `asyncio.wait_for()` be used when tools are asynchronous coroutines?

---

[← Q0620](../../batch_07_mcp_a2a_skills_assistants/0620_validating_tool_arguments_against_pydantic_models/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0622 →](../../batch_07_mcp_a2a_skills_assistants/0622_building_an_in_memory_mcp_tool_registry_and_dispatcher/README.md)
