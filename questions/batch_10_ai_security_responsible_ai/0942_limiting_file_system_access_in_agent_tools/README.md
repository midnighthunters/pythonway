# Q0942 · Limiting file system access in agent tools

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Agent security | Medium |

## Question

Write Python code implementing a path traversal defense for an agent file-reading tool, ensuring paths cannot escape a designated safe directory root.

## Answer

If an agent has a `read_document(filename)` tool, an attacker can input:
`"../../../../etc/shadow"` or `"..\\..\\Windows\\System32\\config\\SAM"`
to perform path traversal and access sensitive operating system files.

Defenses resolve canonical absolute paths and verify that the target path begins with the base directory.

```python
from pathlib import Path


class SafeFileSystemSandbox:
    def __init__(self, root_dir: str):
        self.root = Path(root_dir).resolve()

    def validate_safe_path(self, user_supplied_path: str) -> Path:
        target = (self.root / user_supplied_path).resolve()

        # Target must be relative to or within the root directory
        try:
            target.relative_to(self.root)
        except ValueError:
            raise PermissionError(f"Path traversal detected: {user_supplied_path} escapes sandbox root.")

        return target


sandbox = SafeFileSystemSandbox("C:/sandbox/reports")

# Safe subpath
safe = sandbox.validate_safe_path("2026/q3_report.pdf")
assert str(safe).replace("\\", "/").endswith("reports/2026/q3_report.pdf")

# Traversal attack
try:
    sandbox.validate_safe_path("../../Windows/System32/drivers/etc/hosts")
    assert False, "Should have raised PermissionError"
except PermissionError:
    pass
```

## Likely follow-ups

- How do symbolic links (symlinks) introduce path traversal vulnerabilities, and how does `.resolve(strict=False)` handle them?
- What are the advantages of read-only Docker volume mounts for agent workspaces?

---

[← Q0941](../../batch_10_ai_security_responsible_ai/0941_sandboxed_execution_environments_for_llm_generated_code/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0943 →](../../batch_10_ai_security_responsible_ai/0943_agent_credential_management_avoiding_long_lived_api_tokens/README.md)
