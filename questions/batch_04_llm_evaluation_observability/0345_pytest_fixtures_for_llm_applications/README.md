# Q0345 · Pytest fixtures for LLM applications

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Testing | Medium |

## Question

Show how you'd organise pytest fixtures for an LLM service: a fake LLM, a fake retriever, frozen time, and an evaluation-marked test that calls the real model only when explicitly enabled.

## Answer

```python
# no-run
# conftest.py
import os

import pytest


@pytest.fixture
def fake_llm():
    from tests.fakes import FakeLLM  # scripted, strict fake from the previous question
    return FakeLLM([(r"classify", '{"label": "it"}')])


@pytest.fixture
def fake_retriever():
    docs = {"pol-7": "London hotels are capped at 180 GBP."}
    return lambda query, user: [{"id": k, "text": v} for k, v in docs.items() if "hotel" in query.lower()]


@pytest.fixture
def frozen_now(monkeypatch):
    import datetime as dt
    fixed = dt.datetime(2026, 9, 26, 12, 0, tzinfo=dt.timezone.utc)
    monkeypatch.setattr("app.clock.now", lambda: fixed)
    return fixed


def pytest_collection_modifyitems(config, items):
    if os.getenv("RUN_LLM_EVALS") != "1":
        skip = pytest.mark.skip(reason="set RUN_LLM_EVALS=1 to call real models")
        for item in items:
            if "llm_eval" in item.keywords:
                item.add_marker(skip)


# test_chat.py
def test_routes_it_tickets(fake_llm, fake_retriever):
    from app.chat import answer
    assert answer("VPN broken", llm=fake_llm, retriever=fake_retriever)["route"] == "it"


@pytest.mark.llm_eval
def test_real_model_abstains_on_unknown_policy(real_client):
    assert real_client.ask("What is the Mars office travel policy?")["status"] == "not_found"
```

Design for this with dependency injection: pass the LLM client, retriever and clock into functions, instead of importing global clients. Unit tests stay fast and deterministic on every commit. Real-model tests run in a separate, opt-in job with budgets, and their results feed the evaluation dashboard rather than being flaky blockers.

## Likely follow-ups

- Why does dependency injection make LLM code dramatically easier to test?

---

[← Q0344](../../batch_04_llm_evaluation_observability/0344_property_based_fuzzing_of_output_parsers/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0346 →](../../batch_04_llm_evaluation_observability/0346_contract_tests_for_provider_adapters/README.md)
