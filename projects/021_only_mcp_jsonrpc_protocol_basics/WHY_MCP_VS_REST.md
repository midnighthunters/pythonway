# Why MCP & LLMs? (And Why Not Just a REST API?)

A plain-English guide answering the most common architectural question in AI engineering:
> *"Why do we need an LLM and MCP to run database queries when we can just build a standard REST API?"*

---

## 1. The Short Answer

* **If your app has a fixed button** (*"Click here to load top 5 pending orders"*), you **DO NOT** need an LLM or MCP. A plain REST API is 100x faster, costs $0 in tokens, and never hallucinates.
* **You need an LLM** when a human asks **unpredictable, open-ended questions** that no developer had time to hardcode into an API endpoint.
* **You need MCP** so your AI can connect to tools (Supabase, GitHub, Slack) **instantly without developers writing custom translation glue code for every tool and every AI client**.

---

## 2. Why Do We Need an LLM? (Dynamic Intent vs. Hardcoded Code)

### Scenario A: A Traditional Web Application (Use REST!)
You are building an e-commerce dashboard. The product manager wants a screen showing *"Top 5 Pending Orders"*.
* A backend engineer writes:
  ```python
  @app.get("/api/orders/pending")
  def get_pending_orders():
      return db.query("SELECT * FROM orders WHERE status = 'pending' LIMIT 5")
  ```
* The frontend team attaches that endpoint to a button.
* **Verdict:** Perfect! Zero AI needed. Fast, cheap, and reliable.

---

### Scenario B: The Real World (Why You Need an LLM)
Now the store owner comes along and asks in natural language:
> *"Find all customers who haven't ordered anything in the last 4 months, but spent over $500 last year, and draft a personalized discount email to each of them based on their favorite coffee blend."*

#### Without an LLM:
1. The developer must write a custom SQL query.
2. Build a brand-new REST API endpoint (`/api/marketing/dormant-high-value-customers`).
3. Deploy the backend code.
4. Export the data to a spreadsheet.
5. Manually write and send personalized emails.

#### With an LLM:
The LLM understands the messy human request, figures out the required logic, generates the correct SQL query, executes it, analyzes the customer data, and drafts the personalized emails in seconds.

---

## 3. If We Have REST APIs, Why Do We Need MCP?

*"Okay, the LLM can write SQL. But why can't the LLM just call our existing REST API?"*

Because **every REST API is a completely different snowflake**:

| System | Authentication Format | Pagination Parameter | Error Response Format |
| :--- | :--- | :--- | :--- |
| **GitHub** | `Authorization: Bearer <token>` | `?page=1&per_page=30` | `{"message": "Not Found"}` |
| **Jira** | `Authorization: Basic <base64>` | `?startAt=0&maxResults=50` | `{"errorMessages": [...]}` |
| **Supabase** | `apikey: <key>` header | `?limit=10&offset=20` | `{"code": "PGRST116"}` |
| **Custom Company API** | Custom token header | `?cursor=xyz` | `{"status": 500, "err": "..."}` |

### The "N × M" Integration Problem
If you have **4 AI Clients** (Claude Desktop, Cursor, LangChain, Custom Agent) and **10 Tools** (Supabase, GitHub, Slack, Postgres, Jira...):
* Without a standard, you must write **40 custom integrations** (4 × 10).
* Every time an API changes a header or field, code breaks.

---

## 4. MCP: The "USB-C" Standard for AI

Before USB-C, every electronic device had a different charger (lightning, micro-USB, barrel jacks). USB-C created one universal shape.

**MCP (Model Context Protocol)** is the USB-C cable for AI:

```text
Without MCP (The Spaghetti Mess):
  Claude Desktop ────► Custom GitHub code ────► GitHub
  Cursor IDE     ────► Custom Supabase code ──► Supabase
  LangChain      ────► Custom Slack code    ────► Slack

With MCP (Universal Standard):
  ANY AI Client ──────► JSON-RPC 2.0 ──────► Supabase MCP Server ──► Database
                                      ──────► GitHub MCP Server   ──► Git Repo
                                      ──────► Slack MCP Server    ──► Channels
```

### The 3 Key Superpowers of MCP

1. **Plug-and-Play Discovery (`tools/list`):**
   You don't write code to connect an AI to Supabase. You add 2 lines to a config file:
   ```json
   "supabase": { "command": "npx", "args": ["-y", "@supabase/mcp-server"] }
   ```
   The AI automatically asks the server `tools/list`, reads the JSON Schema of available tools, and knows how to use them instantly.

2. **Zero Open Ports (`stdio`):**
   REST APIs require opening network ports on your machine, managing CORS, configuring SSL certificates, and exposing endpoints to the internet.  
   MCP runs locally inside your machine using **`stdio`** (standard in/out pipes). No ports are opened, and your database credentials never leave your machine.

3. **Standardized Responses:**
   Every MCP server returns data in the exact same shape:
   ```json
   {
     "jsonrpc": "2.0",
     "id": 1,
     "result": {
       "content": [{"type": "text", "text": "..."}],
       "isError": false
     }
   }
   ```
   The AI model knows exactly how to read the result, regardless of which tool produced it.

---

## 5. Summary Cheat Sheet

| Situation | Best Architecture | Reason |
| :--- | :--- | :--- |
| Hardcoded button on a website (*"View Orders"*) | **Plain REST API** | Fast, free, zero hallucination risk. |
| Chatting with Cursor / Claude to inspect your DB or fix bugs | **LLM + MCP** | AI can explore tables and run diagnostic queries autonomously. |
| Autonomous agents researching data across multiple tools | **LLM + MCP** | The agent can discover and call Supabase, GitHub, and Slack through one single protocol. |
