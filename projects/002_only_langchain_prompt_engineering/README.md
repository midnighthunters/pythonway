# Project 002: Dynamic Prompt Templates & Few-Shot In-Context Learning

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 1.5 / 10 (Beginner)  
> **Primary Pillars**: `LangChain`  
> **Auxiliary Disciplines**: None (Core Focus)  

---

## 🎯 Learning Objective
Master advanced prompt engineering techniques in LangChain: dynamic variable interpolation, partial prompt pre-binding, structured few-shot prompt construction, and conversation history injection via `MessagesPlaceholder`.

---

## 🧠 Key Concepts Covered
- **`ChatPromptTemplate`**: Composing parameterized system and human prompts without fragile string concatenations.
- **Partial Formatting (`.partial()`)**: Binding static context (e.g. system configurations, tenant names) to prompts at instantiation time.
- **`FewShotChatMessagePromptTemplate`**: Supplying formatted input/output pairs to guide the model towards specific taxonomy structures.
- **`MessagesPlaceholder`**: Inserting dynamic lists of `BaseMessage` objects (chat history) directly into the prompt sequence.

---

## 🏗️ Architecture & Control Flow
```text
           Few-Shot Example Dataset
                     │
                     ▼
       ┌───────────────────────────┐
       │ FewShotChatMessagePrompt  │
       └─────────────┬─────────────┘
                     │
                     ▼
  User Input ──► ChatPromptTemplate (with MessagesPlaceholder)
                     │
                     ▼
                ChatGroq (LLM)
                     │
                     ▼
               StrOutputParser
```

---

## 📂 Project Structure
```text
002_only_langchain_prompt_engineering/
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

1. **When should you use `.partial()` on a prompt template instead of passing all variables during `.invoke()`?**
   * *Answer*: Use `.partial()` when some parameters are constant throughout a component's lifecycle (e.g. current date, company identity, API endpoint) or when you want to pass a dynamic function that calculates a timestamp at execution time without requiring the caller to supply it.

2. **Why is `FewShotChatMessagePromptTemplate` preferred over pasting raw text examples into a single system string?**
   * *Answer*: It separates examples into native `HumanMessage` and `AIMessage` pairs. This teaches the model the conversation rhythm directly in its expected API schema, producing vastly higher format adherence than unstructured text examples.

3. **What happens if you pass an empty list `[]` to a `MessagesPlaceholder(variable_name="chat_history")`?**
   * *Answer*: LangChain gracefully handles an empty list by omitting any additional messages from that slot without raising a KeyError or formatting error, making it ideal for the first turn of a conversation.

---

## 🏆 Stretch Challenge
**Task**: Extend `main.py` by implementing a `dynamic_few_shot_prompt` that accepts an arbitrary list of examples and formats them into a SQL Query Generator chain (Natural Language Input $\rightarrow$ Syntactically Valid SQL Output).
