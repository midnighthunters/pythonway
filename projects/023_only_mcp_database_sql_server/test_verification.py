"""
Verification Test Suite for Project 023: Relational Database & SQL Inspection MCP Server
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
from main import CoffeeDatabaseMCPServer


def test_schema_discovery_and_query():
    print("Testing database table discovery and read queries...")
    server = CoffeeDatabaseMCPServer()

    # Test list tables
    res_tables = server.call_tool("list_database_tables", {})
    assert res_tables["isError"] is False
    tables = json.loads(res_tables["content"][0]["text"])
    assert "menu_items" in tables
    assert "customers" in tables
    assert "orders" in tables
    print(f"  [PASSED] Table discovery confirmed: {tables}")

    # Test describe schema
    res_schema = server.call_tool("describe_table_schema", {"table_name": "menu_items"})
    assert res_schema["isError"] is False
    cols = json.loads(res_schema["content"][0]["text"])
    col_names = [c["column_name"] for c in cols]
    assert "price" in col_names and "name" in col_names
    print(f"  [PASSED] Schema introspection verified columns: {col_names}")

    # Test read query
    res_query = server.call_tool("execute_read_query", {
        "sql_query": "SELECT name, price FROM menu_items WHERE price > 4.0",
    })
    assert res_query["isError"] is False
    rows = json.loads(res_query["content"][0]["text"])
    assert len(rows) >= 2
    assert all(r["price"] > 4.0 for r in rows)
    print(f"  [PASSED] Safe read query returned {len(rows)} matching records.")


def test_sql_guardrails():
    print("\nTesting SQL injection and destructive query guardrails...")
    server = CoffeeDatabaseMCPServer()

    forbidden_queries = [
        "DROP TABLE customers;",
        "DELETE FROM orders WHERE id=101;",
        "UPDATE customers SET loyalty_points = 99999;",
        "INSERT INTO menu_items VALUES (99, 'Hacked', 'Fake', 0.0);",
        "ALTER TABLE customers ADD COLUMN secret TEXT;",
        "SELECT * FROM customers; DROP TABLE orders;",
        "TRUNCATE TABLE orders;",
    ]

    for sql in forbidden_queries:
        res = server.call_tool("execute_read_query", {"sql_query": sql})
        assert res["isError"] is True, f"Destructive query '{sql}' should have been blocked!"
        err_text = res["content"][0]["text"]
        assert "SECURITY GUARDRAIL REJECTION" in err_text, (
            f"Expected guardrail rejection message, got: {err_text}"
        )

    print(f"  [PASSED] All {len(forbidden_queries)} destructive queries successfully intercepted by guardrails.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 023")
    print("=" * 60)
    test_schema_discovery_and_query()
    test_sql_guardrails()
    print("\n[ALL TESTS PASSED] Project 023 verified successfully!")
