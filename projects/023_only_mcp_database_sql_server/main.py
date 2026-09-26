"""
===============================================================================
PROJECT 023: RELATIONAL DATABASE & SQL INSPECTION MCP SERVER
Stage 1: Pure Fundamentals | Difficulty: 3.0 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
How do we let AI agents inspect and query relational SQL databases safely?

If you give an AI model raw SQL execution privileges:
A hallucination, user prompt injection, or malicious query could execute:
  `DROP TABLE customers;` or `UPDATE accounts SET balance = 1000000;`
Accidental data destruction is a major hazard in enterprise AI!

THE MCP DATABASE SOLUTION:
1. Dynamic Schema Discovery: The agent can inspect tables and schema metadata
   without needing hardcoded documentation.
2. Read-Only Enforcement: Strict parsing ensures ONLY pure `SELECT` queries execute.
3. Injection Guardrails: Forbids multi-statement chaining (`;`) and destructive keywords
   (DROP, DELETE, UPDATE, INSERT, ALTER).
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import sqlite3
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. DATABASE MCP SERVER WITH READ-ONLY GUARDRAILS
# =============================================================================
class CoffeeDatabaseMCPServer:
    """
    Model Context Protocol server for inspecting and querying the cafe SQL database.
    Enforces strict read-only execution guardrails to protect against data destruction.
    """

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            self.db_path = str(Path(__file__).resolve().parent / "cozy_cafe.db")
        else:
            self.db_path = db_path

        self._initialize_database()

    def _initialize_database(self):
        """Initializes database schema and sample data."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # 1. Menu Items Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS menu_items (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL NOT NULL
                )
            """)

            # 2. Customers Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    loyalty_points INTEGER DEFAULT 0,
                    is_vip INTEGER DEFAULT 0
                )
            """)

            # 3. Orders Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY,
                    customer_id INTEGER,
                    item_id INTEGER,
                    quantity INTEGER,
                    order_date TEXT,
                    FOREIGN KEY(customer_id) REFERENCES customers(id),
                    FOREIGN KEY(item_id) REFERENCES menu_items(id)
                )
            """)

            # Seed data if empty
            cursor.execute("SELECT COUNT(*) FROM menu_items")
            if cursor.fetchone()[0] == 0:
                cursor.executemany(
                    "INSERT INTO menu_items VALUES (?, ?, ?, ?)",
                    [
                        (1, "Single Espresso", "Coffee", 3.50),
                        (2, "Vanilla Oat Latte", "Coffee", 5.25),
                        (3, "Ceremonial Matcha", "Tea", 4.75),
                        (4, "Almond Croissant", "Bakery", 4.25),
                    ],
                )
                cursor.executemany(
                    "INSERT INTO customers VALUES (?, ?, ?, ?)",
                    [
                        (1, "Alice Walker", 145, 1),
                        (2, "Bob Martin", 30, 0),
                        (3, "Claire Chen", 260, 1),
                    ],
                )
                cursor.executemany(
                    "INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
                    [
                        (101, 1, 2, 2, "2026-09-25"),
                        (102, 2, 1, 1, "2026-09-25"),
                        (103, 3, 4, 3, "2026-09-26"),
                        (104, 1, 3, 1, "2026-09-26"),
                    ],
                )
            conn.commit()

    # -------------------------------------------------------------------------
    # GUARDRAIL: VALIDATE READ-ONLY SELECT QUERY
    # -------------------------------------------------------------------------
    def _validate_safe_query(self, query: str):
        """
        Validates that the SQL query is strictly read-only.
        Blocks destructive keywords, write operations, and semicolon command chaining.
        """
        clean = query.strip()

        # Must start with SELECT or WITH
        if not re.match(r"^(SELECT|WITH)\b", clean, re.IGNORECASE):
            raise PermissionError(
                "SECURITY GUARDRAIL REJECTION: Only read-only queries starting with "
                "'SELECT' or 'WITH' are permitted on this MCP database connection."
            )

        # Forbid multi-query chaining using semicolons
        # Strips trailing semicolon and whitespace
        trimmed = clean.rstrip("; \t\n\r")
        if ";" in trimmed:
            raise PermissionError(
                "SECURITY GUARDRAIL REJECTION: Semicolon command-chaining is strictly forbidden."
            )

        # Blacklist destructive DDL and DML keywords
        forbidden_keywords = [
            "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE",
            "ATTACH", "DETACH", "CREATE", "REPLACE", "PRAGMA",
        ]
        for kw in forbidden_keywords:
            if re.search(rf"\b{kw}\b", clean, re.IGNORECASE):
                raise PermissionError(
                    f"SECURITY GUARDRAIL REJECTION: Destructive SQL keyword '{kw}' detected! "
                    "Write operations are strictly prohibited."
                )

    # -------------------------------------------------------------------------
    # MCP TOOL IMPLEMENTATIONS
    # -------------------------------------------------------------------------
    def list_database_tables(self) -> List[str]:
        """Discovers all user-created tables in the SQLite database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = [row[0] for row in cursor.fetchall()]
        return tables

    def describe_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Retrieves column names, data types, and primary key constraints."""
        # Sanitize table name against identifier injection
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", table_name):
            raise ValueError(f"Invalid table identifier name: '{table_name}'")

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = []
            for row in cursor.fetchall():
                columns.append({
                    "column_id": row[0],
                    "column_name": row[1],
                    "data_type": row[2],
                    "not_null": bool(row[3]),
                    "default_value": row[4],
                    "is_primary_key": bool(row[5]),
                })
        return columns

    def execute_read_query(self, sql_query: str) -> List[Dict[str, Any]]:
        """Executes a safe, read-only SELECT query and returns rows as dictionaries."""
        self._validate_safe_query(sql_query)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    # -------------------------------------------------------------------------
    # MCP PROTOCOL DISPATCHER
    # -------------------------------------------------------------------------
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if name == "list_database_tables":
                tables = self.list_database_tables()
                return {"isError": False, "content": [{"type": "text", "text": json.dumps(tables)}]}

            elif name == "describe_table_schema":
                table_name = arguments.get("table_name", "")
                schema = self.describe_table_schema(table_name)
                return {"isError": False, "content": [{"type": "text", "text": json.dumps(schema, indent=2)}]}

            elif name == "execute_read_query":
                sql = arguments.get("sql_query", "")
                rows = self.execute_read_query(sql)
                return {"isError": False, "content": [{"type": "text", "text": json.dumps(rows, indent=2)}]}

            else:
                return {"isError": True, "content": [{"type": "text", "text": f"Unknown tool: '{name}'"}]}

        except Exception as e:
            return {"isError": True, "content": [{"type": "text", "text": f"SQL Execution Blocked: {str(e)}"}]}


# =============================================================================
# 2. RUN DEMONSTRATION
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 023: RELATIONAL DATABASE & SQL INSPECTION MCP SERVER")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    server = CoffeeDatabaseMCPServer()

    # -------------------------------------------------------------------------
    # STEP 1: DISCOVER TABLES
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("1. MCP Tool: list_database_tables")
    print("-" * 75)
    res_tables = server.call_tool("list_database_tables", {})
    print(f"Discovered Tables:\n{res_tables['content'][0]['text']}")

    # -------------------------------------------------------------------------
    # STEP 2: INSPECT SCHEMA
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("2. MCP Tool: describe_table_schema ('customers')")
    print("-" * 75)
    res_schema = server.call_tool("describe_table_schema", {"table_name": "customers"})
    print(res_schema["content"][0]["text"])

    # -------------------------------------------------------------------------
    # STEP 3: EXECUTE VALID READ QUERY
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("3. MCP Tool: execute_read_query (Finding VIP Customers with Points)")
    print("-" * 75)
    valid_sql = "SELECT name, loyalty_points, is_vip FROM customers WHERE is_vip = 1 ORDER BY loyalty_points DESC"
    print(f"SQL Query: {valid_sql}")
    res_query = server.call_tool("execute_read_query", {"sql_query": valid_sql})
    print(f"Query Results:\n{res_query['content'][0]['text']}")

    # -------------------------------------------------------------------------
    # STEP 4: SECURITY GUARDRAIL TEST (DESTRUCTIVE QUERY BLOCKED)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("4. SECURITY GUARDRAIL TEST: Attempting 'DROP TABLE customers;'")
    print("-" * 75)
    malicious_sql = "DROP TABLE customers;"
    print(f"Malicious Query: {malicious_sql}")
    res_malicious = server.call_tool("execute_read_query", {"sql_query": malicious_sql})
    print(f"Is Error Flagged: {res_malicious['isError']}")
    print(f"Server Defense  : {res_malicious['content'][0]['text']}")

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 023 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
