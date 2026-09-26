# Project 003: Structured Output & Strict Pydantic Schema Enforcement

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 2.0 / 10 (Beginner)  
> **Primary Pillars**: `LangChain`  
> **Auxiliary Disciplines**: `Guardrails`  

---

## 🎯 Learning Objective
Master programmatic schema enforcement in LangChain: extracting typed, validated Pydantic models using native model schema capabilities (`with_structured_output`), leveraging `JsonOutputParser`, and applying schema guardrails.

---

## 🧠 Key Concepts Covered
- **Pydantic v2 Models**: Specifying typed models with explicit field descriptions and validation constraints.
- **Schema Guardrails**: Using `@field_validator` to enforce business invariants (e.g. bounding confidence scores to $[0.0, 1.0]$).
- **`with_structured_output()`**: Leveraging underlying model function/tool calling to guarantee response formatting.
- **`JsonOutputParser`**: Generating explicit JSON schema prompt instructions for models lacking native tool support.

---

## 🏗️ Architecture & Control Flow
```text
Unstructured System Text
           │
           ▼
┌─────────────────────────────────┐
│     ChatPromptTemplate          │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│ llm.with_structured_output()    │  passes JSON schema via tool definitions
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│    Pydantic Schema Guardrail    │  validates types, enums & ranges
└──────────────┬──────────────────┘
               │
               ▼
    Validated IncidentReport Object
```

---

## 📂 Project Structure
```text
003_only_langchain_structured_output/
├── README.md              # Project specifications, self-quiz & stretch challenge
├── requirements.txt       # Dependencies for this project
├── config.py              # Groq model and environment configuration
├── main.py                # Pedagogical runnable demonstration
└── test_verification.py   # Automated assertion tests
```

---

## 🚀 Execution & Verification Guide

### 1. Run Main Demonstration
```bash
python main.py
```

### 2. Run Automated Verification Tests
```bash
python test_verification.py
```

---

## 📝 Self-Assessment Interview Quiz (Test Your Understanding)

1. **Why is `with_structured_output(PydanticModel)` more reliable than asking the model in prompt text to "reply in JSON"?**
   * *Answer*: Prompt-only JSON requests frequently suffer from preamble text (e.g. "Here is your JSON:"), markdown code fences (` ```json `), or invalid trailing commas. `with_structured_output` leverages model-level tool/function calling schemas, constraining the token sampling grammar directly to valid JSON.

2. **How does Pydantic v2 act as a safety and data guardrail?**
   * *Answer*: Pydantic validates data types, enforces string lengths (`Field(max_length=...)`), validates numeric ranges (`Field(ge=0, le=1)`), and executes custom `@field_validator` functions before objects are instantiated, immediately rejecting corrupted model outputs.

3. **When would you choose `JsonOutputParser` over `with_structured_output`?**
   * *Answer*: When working with local or smaller open-weights LLMs that do not have robust native function-calling capabilities, or when building chains that need to inspect raw JSON formatting instructions explicitly.

---

## 🏆 Stretch Challenge
**Task**: Add a nested Pydantic model `ActionItem(assignee: str, priority: int, action: str)` inside `IncidentReport` as `mitigation_steps: List[ActionItem]`, and extract a list of concrete remediation actions from the alert text.
