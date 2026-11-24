from src.ui.demo import (
    DEMO_RECEIPTS,
    demo_analytics,
    demo_category_totals,
    demo_chat,
    demo_monthly_totals,
)


def test_demo_analytics_are_derived_from_sample_receipts():
    analytics = demo_analytics()

    assert f"Transactions: {len(DEMO_RECEIPTS)}." in analytics["summary"]
    assert "StreamFlix" in analytics["subscriptions"]
    assert len(demo_category_totals()) > 1
    assert len(demo_monthly_totals()) == 3


def test_demo_chat_discloses_synthetic_data_and_no_model_inference():
    result = demo_chat("What are my recurring subscriptions?")

    assert "StreamFlix" in result["response"]
    assert "synthetic data" in result["response"]
    assert "no AI model is called" in result["response"]
    assert result["execution_trace"][0]["tool_selected"] == "SAMPLE_ANALYTICS"
