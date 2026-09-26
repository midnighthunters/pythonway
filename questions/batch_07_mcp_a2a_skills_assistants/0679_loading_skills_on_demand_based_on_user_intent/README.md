# Q0679 · Loading skills on demand based on user intent

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Agent skills | Medium |

## Question

Write Python code that matches a user query against a skill catalog using keyword and regex matching to select and activate the target skill.

## Answer

```python
import re
from typing import Any, Dict, List, Optional


class IntentSkillMatcher:
    def __init__(self):
        self._rules: List[Dict[str, Any]] = []

    def add_skill_rule(self, skill_name: str, patterns: List[str]):
        compiled = [re.compile(p, re.IGNORECASE) for p in patterns]
        self._rules.append({"name": skill_name, "patterns": compiled})

    def match_skill(self, user_query: str) -> Optional[str]:
        for rule in self._rules:
            for pat in rule["patterns"]:
                if pat.search(user_query):
                    return rule["name"]
        return None


matcher = IntentSkillMatcher()
matcher.add_skill_rule("fx_hedge", [r"\bhedge\b", r"\bfx exposure\b", r"\bcurrency risk\b"])
matcher.add_skill_rule("trade_break", [r"\bbreak\b", r"\bunmatched trade\b", r"\breconciliation\b"])

assert matcher.match_skill("We need to hedge our EUR exposure.") == "fx_hedge"
assert matcher.match_skill("Found an unmatched trade in LDN books.") == "trade_break"
assert matcher.match_skill("What is the weather today?") is None
```

## Likely follow-ups

- When should semantic vector embedding search be used instead of regex matching?
- How does the system handle queries that bridge across two distinct skills?

---

[← Q0678](../../batch_07_mcp_a2a_skills_assistants/0678_progressive_disclosure_pattern_for_agent_skills/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0680 →](../../batch_07_mcp_a2a_skills_assistants/0680_validating_skill_configuration_and_metadata_with_pydantic/README.md)
