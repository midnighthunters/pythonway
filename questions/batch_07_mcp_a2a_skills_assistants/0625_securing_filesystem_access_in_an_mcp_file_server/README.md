# Q0625 · Securing filesystem access in an MCP file server

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP tools | Hard |

## Question

An MCP server exposes local files to an agent. Write Python code that prevents path traversal attacks (`../../etc/passwd`) by validating paths against an allowed root directory.

## Answer

File access MCP servers must strictly sandbox paths to authorized directories. Attackers can embed `../` in user prompts to trick an agent into reading private system keys or configuration files.

```python
from pathlib import Path
import tempfile
from typing import Any, Dict


class SandboxedFileServer:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir.resolve()

    def read_file(self, rel_path: str) -> Dict[str, Any]:
        target = (self.root_dir / rel_path).resolve()

        if not target.is_relative_to(self.root_dir):
            return {
                "content": [{"type": "text", "text": "Access denied: Path is outside authorized workspace root."}],
                "isError": True,
            }

        if not target.exists():
            return {
                "content": [{"type": "text", "text": f"File '{rel_path}' does not exist."}],
                "isError": True,
            }

        if target.is_dir():
            return {
                "content": [{"type": "text", "text": f"Cannot read directory '{rel_path}' as file."}],
                "isError": True,
            }

        content = target.read_text(encoding="utf-8")
        return {"content": [{"type": "text", "text": content}], "isError": False}


with tempfile.TemporaryDirectory() as tmp_dir:
    root = Path(tmp_dir)
    safe_file = root / "report.txt"
    safe_file.write_text("Confidential Trade Log", encoding="utf-8")

    server = SandboxedFileServer(root)

    res = server.read_file("report.txt")
    assert res["isError"] is False
    assert res["content"][0]["text"] == "Confidential Trade Log"

    attack = server.read_file("../../windows/system32/cmd.exe")
    assert attack["isError"] is True
    assert "Access denied" in attack["content"][0]["text"]
```

## Likely follow-ups

- Why is `target.resolve()` essential before checking `is_relative_to()`?
- How should symbolic links pointing outside the sandbox root be handled?

---

[← Q0624](../../batch_07_mcp_a2a_skills_assistants/0624_dynamic_tool_registration_and_tools_list_changed/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0626 →](../../batch_07_mcp_a2a_skills_assistants/0626_sandboxing_database_query_execution_in_an_sql_mcp_server/README.md)
