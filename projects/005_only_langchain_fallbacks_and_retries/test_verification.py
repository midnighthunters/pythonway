import sys

# Ensure UTF-8 output encoding for Windows command line
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from langchain_core.runnables import RunnableLambda
from config import get_llm, ACTIVE_MODEL


def test_model_fallback():
    failing_model = get_llm(model="non-existent-broken-model")
    working_model = get_llm(model=ACTIVE_MODEL)

    resilient_model = failing_model.with_fallbacks([working_model])
    res = resilient_model.invoke("Say 'FALLBACK_OK' in 1 word.")
    assert "FALLBACK_OK" in res.content.upper() or len(res.content) > 0, "Expected fallback execution"
    print("✅ test_model_fallback PASSED!")


def test_retry_runnable():
    counter = {"calls": 0}

    def flaky(x):
        counter["calls"] += 1
        if counter["calls"] < 2:
            raise ValueError("Transient error")
        return "SUCCESS"

    retrying_runnable = RunnableLambda(flaky).with_retry(stop_after_attempt=3)
    res = retrying_runnable.invoke({})
    assert res == "SUCCESS", f"Expected SUCCESS, got {res}"
    assert counter["calls"] == 2, f"Expected 2 attempts, got {counter['calls']}"
    print("✅ test_retry_runnable PASSED!")


if __name__ == "__main__":
    test_model_fallback()
    test_retry_runnable()
    print("🎉 ALL PROJECT 005 AUTOMATED TESTS PASSED!")
