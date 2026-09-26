"""
Verification Test Suite for Project 022: Local Filesystem MCP Server
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
from pathlib import Path
from main import BakeryVaultMCPServer


def test_vault_read_write_operations():
    print("Testing safe vault file operations...")
    server = BakeryVaultMCPServer()

    # Test List
    res_list = server.call_tool("list_vault_files", {})
    assert res_list["isError"] is False
    files = json.loads(res_list["content"][0]["text"])
    filenames = [f["filename"] for f in files]
    assert "cinnamon_swirl_bun.txt" in filenames
    print(f"  [PASSED] Vault file listing verified ({len(files)} files found).")

    # Test Read
    res_read = server.call_tool("read_vault_file", {"filename": "cinnamon_swirl_bun.txt"})
    assert res_read["isError"] is False
    assert "cinnamon" in res_read["content"][0]["text"].lower()
    print("  [PASSED] Vault file read verified.")

    # Test Write
    test_content = "Test Croissant: 300g butter, 3 turns."
    res_write = server.call_tool("write_vault_file", {"filename": "test_croissant.txt", "content": test_content})
    assert res_write["isError"] is False

    read_back = server.call_tool("read_vault_file", {"filename": "test_croissant.txt"})
    assert read_back["content"][0]["text"] == test_content
    print("  [PASSED] Vault write and persistence verified.")


def test_path_traversal_guardrails():
    print("\nTesting path traversal defense guardrails...")
    server = BakeryVaultMCPServer()

    attacks = [
        "../../.env",
        "../config.py",
        "nested/../../../../etc/passwd",
        "/windows/system32/cmd.exe",
    ]

    for attack in attacks:
        res = server.call_tool("read_vault_file", {"filename": attack})
        assert res["isError"] is True, f"Attack '{attack}' should have failed!"
        error_msg = res["content"][0]["text"]
        assert "SECURITY VIOLATION" in error_msg or "Path traversal blocked" in error_msg, (
            f"Expected traversal defense error, got: {error_msg}"
        )

    print(f"  [PASSED] All {len(attacks)} path traversal attacks successfully intercepted.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 022")
    print("=" * 60)
    test_vault_read_write_operations()
    test_path_traversal_guardrails()
    print("\n[ALL TESTS PASSED] Project 022 verified successfully!")
