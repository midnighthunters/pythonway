# Q0578 · Define tools with the @tool decorator

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangChain tools | Easy |

## Question

Define a LangChain tool with `@tool`, show the name, description and argument schema the model sees, and invoke it directly.

## Answer

```python
from langchain_core.tools import tool


@tool
def get_fx_rate(pair: str, date: str = "latest") -> float:
    """Get the FX rate for a currency pair such as GBPUSD. Use 'latest' or an ISO date (YYYY-MM-DD)."""
    return 1.27 if pair == "GBPUSD" else 0.0


assert get_fx_rate.name == "get_fx_rate"
assert get_fx_rate.description.startswith("Get the FX rate for a currency pair")
assert set(get_fx_rate.args) == {"pair", "date"}
assert get_fx_rate.invoke({"pair": "GBPUSD"}) == 1.27
schema = get_fx_rate.tool_call_schema.model_json_schema()
assert schema["required"] == ["pair"]
```

The function name becomes the tool name, the docstring becomes the description, and the type hints and defaults become the JSON Schema. These are the prompt the model uses to pick and call the tool, so write the docstring as guidance: when to use it, the argument formats, and what it returns.

## Likely follow-ups

- What would you add to this docstring to reduce wrong calls?

---

[← Q0577](../../batch_06_langgraph_langchain/0577_output_parsers/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0579 →](../../batch_06_langgraph_langchain/0579_structuredtool_with_a_pydantic_args_schema/README.md)
