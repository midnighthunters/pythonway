"""
Test verification suite for Project 043: VectorDB + LangChain Dynamic Semantic Few-Shot Selector
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import VectorExampleSelector, FEW_SHOT_EXAMPLES, build_dynamic_few_shot_chain


def test_example_selector_categories():
    selector = VectorExampleSelector(FEW_SHOT_EXAMPLES)

    # 1. Beverage Query
    bev_res = selector.select_examples("I need a large iced latte with oat milk and syrup", top_k=2)
    assert len(bev_res) == 2
    assert bev_res[0]["example"]["category"] == "pos_customization"
    assert bev_res[0]["score"] > 0.0

    # 2. Hardware Query
    diag_res = selector.select_examples("Espresso machine pressure gauge error E-02 flashing", top_k=2)
    assert len(diag_res) == 2
    assert diag_res[0]["example"]["category"] == "equipment_diagnostics"

    # 3. Origin/Cupping Query
    cup_res = selector.select_examples("What are the tasting notes and origin of Ethiopian coffee?", top_k=2)
    assert len(cup_res) == 2
    assert cup_res[0]["example"]["category"] == "cupping_notes"


def test_end_to_end_few_shot_pipeline():
    selector = VectorExampleSelector(FEW_SHOT_EXAMPLES)
    pipeline = build_dynamic_few_shot_chain(selector)

    # Run a beverage customization query
    result = pipeline("Medium cold brew with vanilla syrup and sweet foam")
    assert "selected_examples" in result
    assert len(result["selected_examples"]) == 2
    assert result["selected_examples"][0]["example"]["category"] == "pos_customization"

    output = result["llm_output"]
    assert isinstance(output, str)
    assert len(output) > 10
    # LLM should adhere to POS-TICKET format demonstrated in selected examples
    assert "[pos-ticket]" in output.lower() or "size:" in output.lower()


if __name__ == "__main__":
    test_example_selector_categories()
    test_end_to_end_few_shot_pipeline()
    print("Project 043: All verification tests PASSED successfully!")
