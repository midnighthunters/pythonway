import sys

# Ensure UTF-8 output encoding for Windows command line
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)


def test_runnable_parallel():
    branch_a = RunnableLambda(lambda x: x["val"] * 2)
    branch_b = RunnableLambda(lambda x: x["val"] + 10)

    parallel = RunnableParallel(
        doubled=branch_a,
        plus_ten=branch_b,
        original=RunnablePassthrough(),
    )

    res = parallel.invoke({"val": 5})
    assert res["doubled"] == 10, f"Expected doubled=10, got {res['doubled']}"
    assert res["plus_ten"] == 15, f"Expected plus_ten=15, got {res['plus_ten']}"
    assert res["original"] == {"val": 5}, f"Expected original input preserved"
    print("✅ test_runnable_parallel PASSED!")


def test_passthrough_assign():
    chain = RunnablePassthrough.assign(
        squared=lambda x: x["num"] ** 2,
        greeting=lambda x: f"Hello {x['name']}",
    )
    res = chain.invoke({"num": 4, "name": "Antigravity"})
    assert res["squared"] == 16, f"Expected squared=16, got {res['squared']}"
    assert res["greeting"] == "Hello Antigravity", f"Expected greeting formatted"
    assert res["num"] == 4, "Expected original num preserved"
    print("✅ test_passthrough_assign PASSED!")


if __name__ == "__main__":
    test_runnable_parallel()
    test_passthrough_assign()
    print("🎉 ALL PROJECT 004 AUTOMATED TESTS PASSED!")
