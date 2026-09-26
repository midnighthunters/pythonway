"""
Verification Test Suite for Project 024: MCP Resources & Prompts Provider
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
from main import CoffeeResourceAndPromptMCPServer


def test_resources_lifecycle():
    print("Testing MCP resources/list and resources/read...")
    server = CoffeeResourceAndPromptMCPServer()

    # 1. Test resources/list
    res_list = server.handle_message({"id": 1, "method": "resources/list"})
    assert "result" in res_list, "Missing result in resources/list"
    resources = res_list["result"]["resources"]
    uris = [r["uri"] for r in resources]
    assert "coffee://menu/seasonal" in uris
    assert "coffee://operations/roast-schedule" in uris
    print(f"  [PASSED] Discovered {len(resources)} registered resource URIs.")

    # 2. Test resources/read
    res_read = server.handle_message({
        "id": 2,
        "method": "resources/read",
        "params": {"uri": "coffee://menu/seasonal"},
    })
    assert "result" in res_read
    contents = res_read["result"]["contents"]
    assert len(contents) == 1
    assert contents[0]["mimeType"] == "application/json"
    menu_data = json.loads(contents[0]["text"])
    assert "specials" in menu_data
    assert len(menu_data["specials"]) >= 3
    print("  [PASSED] Successfully read and parsed JSON resource payload.")

    # 3. Test resources/read error handling
    res_err = server.handle_message({
        "id": 3,
        "method": "resources/read",
        "params": {"uri": "coffee://invalid/uri"},
    })
    assert "error" in res_err
    assert "not found" in res_err["error"]["message"].lower()
    print("  [PASSED] Invalid resource URI cleanly returned error response.")


def test_prompts_lifecycle():
    print("\nTesting MCP prompts/list and prompts/get...")
    server = CoffeeResourceAndPromptMCPServer()

    # 1. Test prompts/list
    p_list = server.handle_message({"id": 10, "method": "prompts/list"})
    prompts = p_list["result"]["prompts"]
    names = [p["name"] for p in prompts]
    assert "barista_upsell_recommender" in names
    assert "customer_service_recovery" in names
    print(f"  [PASSED] Discovered {len(prompts)} registered prompt templates.")

    # 2. Test prompts/get
    p_get = server.handle_message({
        "id": 11,
        "method": "prompts/get",
        "params": {
            "name": "barista_upsell_recommender",
            "arguments": {"customer_mood": "stressed", "dietary_preference": "gluten-free"},
        },
    })
    assert "result" in p_get
    messages = p_get["result"]["messages"]
    assert len(messages) >= 1
    rendered_text = messages[0]["content"]["text"]
    assert "stressed" in rendered_text
    assert "gluten-free" in rendered_text
    print("  [PASSED] Successfully rendered parameterized prompt with injected arguments.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 024")
    print("=" * 60)
    test_resources_lifecycle()
    test_prompts_lifecycle()
    print("\n[ALL TESTS PASSED] Project 024 verified successfully!")
