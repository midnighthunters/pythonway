# Q0685 · Implementing a dynamic Skill Registry and loader

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Agent skills | Medium |

## Question

Implement a complete Python Skill Registry that supports registering skills, listing active skills, and invoking skills with exception handling.

## Answer

```python
from typing import Any, Callable, Dict, List, Optional


class EnterpriseSkillRegistry:
    def __init__(self):
        self._skills: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, description: str, handler: Callable[[Dict[str, Any]], Any]):
        self._skills[name] = {"name": name, "description": description, "handler": handler}

    def list_skills(self) -> List[Dict[str, str]]:
        return [{"name": s["name"], "description": s["description"]} for s in self._skills.values()]

    def invoke_skill(self, name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if name not in self._skills:
            return {"status": "error", "message": f"Skill '{name}' not found."}
        try:
            res = self._skills[name]["handler"](params)
            return {"status": "success", "data": res}
        except Exception as e:
            return {"status": "error", "message": f"Skill execution failed: {e}"}


registry = EnterpriseSkillRegistry()
registry.register("pricing", "Bond pricing skill", lambda p: p["face_value"] * 0.98)

assert len(registry.list_skills()) == 1
ok = registry.invoke_skill("pricing", {"face_value": 1000})
assert ok["status"] == "success"
assert ok["data"] == 980.0

bad = registry.invoke_skill("unknown", {})
assert bad["status"] == "error"
```

## Likely follow-ups

- How can the registry reload skills dynamically without restarting the server?
- How should tenant isolation be applied when loading skills for different business units?

---

[← Q0684](../../batch_07_mcp_a2a_skills_assistants/0684_auditing_skill_inputs_and_generated_artifacts/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0686 →](../../batch_07_mcp_a2a_skills_assistants/0686_architecture_of_an_enterprise_personal_ai_assistant/README.md)
