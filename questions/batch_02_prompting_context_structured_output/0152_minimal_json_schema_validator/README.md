# Q0152 · Minimal JSON Schema validator

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Structured output | Medium |

## Question

Without external libraries, implement a small JSON Schema subset validator (type, properties, required, additionalProperties false, enum, items, min/max length) that returns error paths. Watch out for Python's `bool` being an `int`.

## Answer

```python
TYPES = {"object": dict, "array": list, "string": str, "number": (int, float), "integer": int,
         "boolean": bool, "null": type(None)}


def validate(instance, schema: dict, path: str = "$") -> list[str]:
    errors = []
    t = schema.get("type")
    if t:
        ok = isinstance(instance, TYPES[t])
        if t in ("number", "integer") and isinstance(instance, bool):
            ok = False
        if not ok:
            return [f"{path}: expected {t}, got {type(instance).__name__}"]
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {instance!r} not in {schema['enum']}")
    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            errors.append(f"{path}: shorter than {schema['minLength']}")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append(f"{path}: longer than {schema['maxLength']}")
    if isinstance(instance, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}.{key}: required")
        for key, value in instance.items():
            if key in props:
                errors += validate(value, props[key], f"{path}.{key}")
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}.{key}: not allowed")
    if isinstance(instance, list) and "items" in schema:
        for i, item in enumerate(instance):
            errors += validate(item, schema["items"], f"{path}[{i}]")
    return errors


schema = {"type": "object", "required": ["label", "scores"], "additionalProperties": False,
          "properties": {"label": {"type": "string", "enum": ["hr", "it"]},
                         "scores": {"type": "array", "items": {"type": "number"}},
                         "note": {"type": "string", "maxLength": 5}}}
assert validate({"label": "it", "scores": [0.9, 1]}, schema) == []
errs = validate({"label": "legal", "scores": [True], "note": "too long", "x": 1}, schema)
assert errs == ["$.label: 'legal' not in ['hr', 'it']", "$.scores[0]: expected number, got bool",
                "$.note: longer than 5", "$.x: not allowed"]
assert validate({"scores": []}, schema) == ["$.label: required"]
```

In production use the `jsonschema` library (or Pydantic), which covers the full specification including `$ref`, formats and composition. Writing a subset like this is a common interview exercise in recursion and careful type handling.

## Likely follow-ups

- How would you add `$ref` support without infinite recursion on cyclic schemas?

---

[← Q0151](../../batch_02_prompting_context_structured_output/0151_coerce_and_validate_tool_arguments/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0153 →](../../batch_02_prompting_context_structured_output/0153_writing_good_tool_descriptions/README.md)
