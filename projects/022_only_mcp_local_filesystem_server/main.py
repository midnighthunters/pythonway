"""
===============================================================================
PROJECT 022: CUSTOM LOCAL FILESYSTEM MCP SERVER
Stage 1: Pure Fundamentals | Difficulty: 3.0 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
How do we give AI agents access to local files without risking server security?

If you give an AI agent a naive `read_file(path)` tool:
An attacker or confused model could request:
  `read_file("../../../../etc/passwd")` or `read_file("../../.env")`
This vulnerability is called "Directory Path Traversal" (CWE-22).

THE MCP SOLUTION:
1. Sandboxed Root Directory: All file operations are locked to a specific base path.
2. Canonical Path Resolution: Every requested path is resolved to its absolute target
   and verified with `.is_relative_to(sandbox_root)`.
3. Standard MCP File Tools:
   - `list_vault_files`
   - `read_vault_file`
   - `write_vault_file`
4. Security Guardrails: Instant interception and denial of any path escaping the sandbox!
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. SECURE FILESYSTEM MCP SERVER
# =============================================================================
class BakeryVaultMCPServer:
    """
    Model Context Protocol server managing a sandboxed bakery recipe vault.
    Enforces strict path traversal defenses on all I/O operations.
    """

    def __init__(self, vault_dir: Optional[Path] = None):
        if vault_dir is None:
            self.vault_dir = Path(__file__).resolve().parent / "bakery_vault"
        else:
            self.vault_dir = Path(vault_dir).resolve()

        # Ensure sandbox directory exists
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        self._seed_default_recipes()

    def _seed_default_recipes(self):
        """Seeds initial sample recipes into the vault."""
        r1 = self.vault_dir / "cinnamon_swirl_bun.txt"
        if not r1.exists():
            r1.write_text(
                "Cinnamon Swirl Bun Recipe:\n"
                "- 500g bread flour\n- 250ml warm oat milk\n- 15g cinnamon & brown sugar filling\n"
                "Bake at 375F for 22 minutes until golden brown.\n",
                encoding="utf-8",
            )

        r2 = self.vault_dir / "sourdough_bagel.txt"
        if not r2.exists():
            r2.write_text(
                "Sourdough Bagel Recipe:\n"
                "- 400g high-protein flour\n- 100g active sourdough starter\n- 1 tbsp barley malt syrup\n"
                "Boil 1 min each side in malt water, bake at 425F for 20 minutes.\n",
                encoding="utf-8",
            )

    def _resolve_safe_path(self, relative_path: str) -> Path:
        """
        Validates that the target path does NOT escape the sandbox boundary.
        Rejects absolute paths and raises PermissionError if traversal is detected.
        """
        # Reject absolute paths and drive letters immediately
        p = Path(relative_path)
        if p.is_absolute() or p.drive or relative_path.startswith("/") or relative_path.startswith("\\"):
            raise PermissionError(
                f"SECURITY VIOLATION: Absolute paths are strictly forbidden! '{relative_path}'"
            )

        candidate = (self.vault_dir / relative_path).resolve()

        # Check if candidate is strictly inside vault_dir
        try:
            candidate.relative_to(self.vault_dir)
        except ValueError:
            raise PermissionError(
                f"SECURITY VIOLATION: Path traversal blocked! '{relative_path}' "
                f"attempts to escape the sandboxed vault: '{self.vault_dir}'"
            )

        return candidate

    # -------------------------------------------------------------------------
    # MCP TOOL IMPLEMENTATIONS
    # -------------------------------------------------------------------------
    def list_vault_files(self) -> List[Dict[str, Any]]:
        """Lists all files stored inside the secure bakery vault."""
        results = []
        for p in self.vault_dir.rglob("*"):
            if p.is_file():
                rel = p.relative_to(self.vault_dir)
                results.append({
                    "filename": str(rel),
                    "size_bytes": p.stat().st_size,
                })
        return results

    def read_vault_file(self, filename: str) -> str:
        """Reads a file from the vault with path traversal protection."""
        safe_path = self._resolve_safe_path(filename)
        if not safe_path.exists():
            raise FileNotFoundError(f"File '{filename}' does not exist in vault.")
        return safe_path.read_text(encoding="utf-8")

    def write_vault_file(self, filename: str, content: str) -> str:
        """Writes or creates a recipe file safely inside the vault."""
        safe_path = self._resolve_safe_path(filename)
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        safe_path.write_text(content, encoding="utf-8")
        return f"Successfully saved {len(content)} characters to '{filename}'."

    # -------------------------------------------------------------------------
    # MCP JSON-RPC DISPATCHER
    # -------------------------------------------------------------------------
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if tool_name == "list_vault_files":
                files = self.list_vault_files()
                return {"isError": False, "content": [{"type": "text", "text": json.dumps(files, indent=2)}]}

            elif tool_name == "read_vault_file":
                filename = arguments.get("filename", "")
                text = self.read_vault_file(filename)
                return {"isError": False, "content": [{"type": "text", "text": text}]}

            elif tool_name == "write_vault_file":
                filename = arguments.get("filename", "")
                content = arguments.get("content", "")
                msg = self.write_vault_file(filename, content)
                return {"isError": False, "content": [{"type": "text", "text": msg}]}

            else:
                return {"isError": True, "content": [{"type": "text", "text": f"Unknown tool: {tool_name}"}]}

        except Exception as e:
            return {"isError": True, "content": [{"type": "text", "text": f"Tool Execution Failed: {str(e)}"}]}


# =============================================================================
# 2. RUN DEMONSTRATION
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 022: CUSTOM LOCAL FILESYSTEM MCP SERVER")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    server = BakeryVaultMCPServer()
    print(f"Secure Sandbox Root Directory:\n  {server.vault_dir}")

    # -------------------------------------------------------------------------
    # TEST 1: LIST FILES
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("1. MCP Tool Call: list_vault_files")
    print("-" * 75)
    res_list = server.call_tool("list_vault_files", {})
    print(res_list["content"][0]["text"])

    # -------------------------------------------------------------------------
    # TEST 2: READ FILE
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("2. MCP Tool Call: read_vault_file ('cinnamon_swirl_bun.txt')")
    print("-" * 75)
    res_read = server.call_tool("read_vault_file", {"filename": "cinnamon_swirl_bun.txt"})
    print(res_read["content"][0]["text"])

    # -------------------------------------------------------------------------
    # TEST 3: WRITE NEW FILE
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("3. MCP Tool Call: write_vault_file ('matcha_scone.txt')")
    print("-" * 75)
    scone_recipe = (
        "Matcha Glazed Scone Recipe:\n"
        "- 300g flour\n- 2 tbsp ceremonial matcha powder\n- 100g chilled butter\n"
        "Bake at 400F for 15 minutes, drizzle with white chocolate glaze.\n"
    )
    res_write = server.call_tool("write_vault_file", {"filename": "matcha_scone.txt", "content": scone_recipe})
    print(res_write["content"][0]["text"])

    # -------------------------------------------------------------------------
    # TEST 4: PATH TRAVERSAL SECURITY ATTACK (MUST BE INTERCEPTED)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("4. SECURITY GUARDRAIL TEST: Malicious Path Traversal ('../../.env')")
    print("-" * 75)
    malicious_call = server.call_tool("read_vault_file", {"filename": "../../.env"})
    print(f"Is Error Flagged: {malicious_call['isError']}")
    print(f"Server Defense  : {malicious_call['content'][0]['text']}")

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 022 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
