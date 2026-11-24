"""Synthetic data and deterministic responses for the public portfolio demo."""

from collections import Counter, defaultdict


DEMO_RECEIPTS = [
    {"store": "Market Basket", "date": "2026-01-03", "total": 64.20, "category": "Groceries", "items": "Produce, rice, coffee"},
    {"store": "Bean House", "date": "2026-01-05", "total": 7.50, "category": "Dining", "items": "Latte"},
    {"store": "StreamFlix", "date": "2026-01-10", "total": 14.99, "category": "Subscriptions", "items": "Monthly plan"},
    {"store": "City Transit", "date": "2026-01-14", "total": 22.00, "category": "Transport", "items": "Transit card"},
    {"store": "Market Basket", "date": "2026-01-18", "total": 53.20, "category": "Groceries", "items": "Vegetables, bread"},
    {"store": "Bean House", "date": "2026-02-05", "total": 8.25, "category": "Dining", "items": "Coffee, sandwich"},
    {"store": "StreamFlix", "date": "2026-02-10", "total": 14.99, "category": "Subscriptions", "items": "Monthly plan"},
    {"store": "Market Basket", "date": "2026-02-18", "total": 71.40, "category": "Groceries", "items": "Groceries"},
    {"store": "Bean House", "date": "2026-03-05", "total": 6.80, "category": "Dining", "items": "Coffee"},
    {"store": "StreamFlix", "date": "2026-03-10", "total": 14.99, "category": "Subscriptions", "items": "Monthly plan"},
    {"store": "Market Basket", "date": "2026-03-18", "total": 58.90, "category": "Groceries", "items": "Groceries"},
    {"store": "Paws & Care", "date": "2026-03-22", "total": 189.00, "category": "Pet Care", "items": "Veterinary visit"},
]


def demo_category_totals() -> list[dict[str, float | str]]:
    """Return category totals from the bundled example receipts."""
    totals: defaultdict[str, float] = defaultdict(float)
    for receipt in DEMO_RECEIPTS:
        totals[receipt["category"]] += receipt["total"]
    return [
        {"category": category, "total": round(total, 2)}
        for category, total in sorted(totals.items(), key=lambda item: item[1], reverse=True)
    ]


def demo_monthly_totals() -> list[dict[str, float | str]]:
    """Return monthly totals from the bundled example receipts."""
    totals: defaultdict[str, float] = defaultdict(float)
    for receipt in DEMO_RECEIPTS:
        totals[receipt["date"][:7]] += receipt["total"]
    return [
        {"month": month, "total": round(total, 2)}
        for month, total in sorted(totals.items())
    ]


def demo_analytics() -> dict[str, str]:
    """Build readable analytics from synthetic demo data."""
    total = sum(receipt["total"] for receipt in DEMO_RECEIPTS)
    average = total / len(DEMO_RECEIPTS)
    categories = demo_category_totals()
    monthly = demo_monthly_totals()

    visits = Counter(receipt["store"] for receipt in DEMO_RECEIPTS)
    subscriptions = [
        store for store, count in visits.items()
        if count >= 3 and any(
            receipt["store"] == store and receipt["category"] == "Subscriptions"
            for receipt in DEMO_RECEIPTS
        )
    ]
    largest = max(DEMO_RECEIPTS, key=lambda receipt: receipt["total"])

    summary = (
        f"Overall Total Spend: ${total:,.2f}. Transactions: {len(DEMO_RECEIPTS)}. "
        f"Average Transaction: ${average:,.2f}."
    )
    anomalies = (
        f"Largest sample transaction: {largest['store']} — "
        f"${largest['total']:,.2f} ({largest['category']})."
    )
    subscription_text = (
        "Repeated monthly sample charge(s): " + ", ".join(subscriptions) + "."
        if subscriptions else "No repeated sample charges found."
    )
    trends = "Monthly sample totals: " + "; ".join(
        f"{entry['month']}: ${entry['total']:,.2f}" for entry in monthly
    ) + "."
    category_text = "Sample spending by category: " + "; ".join(
        f"{entry['category']}: ${entry['total']:,.2f}" for entry in categories
    ) + "."

    return {
        "summary": summary,
        "anomalies": anomalies,
        "subscriptions": subscription_text,
        "trends": trends,
        "categories": category_text,
        "report": "\n".join((summary, anomalies, subscription_text, trends, category_text)),
    }


def demo_chat(query: str) -> dict:
    """Return a deterministic answer based on the synthetic receipt sample."""
    lowered = query.lower()
    analytics = demo_analytics()

    if any(word in lowered for word in ("subscription", "recurring", "repeat")):
        answer = analytics["subscriptions"]
        tool = "SAMPLE_ANALYTICS"
    elif any(word in lowered for word in ("anomal", "unusual", "largest", "outlier")):
        answer = analytics["anomalies"]
        tool = "SAMPLE_ANALYTICS"
    elif any(word in lowered for word in ("trend", "month", "week", "over time")):
        answer = analytics["trends"]
        tool = "SAMPLE_ANALYTICS"
    elif any(word in lowered for word in ("categor", "breakdown", "where")):
        answer = analytics["categories"]
        tool = "SAMPLE_ANALYTICS"
    elif any(word in lowered for word in ("receipt", "item", "store", "purchase")):
        answer = (
            "The example data includes purchases at Market Basket, Bean House, "
            "StreamFlix, City Transit, and Paws & Care. Visit Financial Intel "
            "to browse the complete synthetic receipt table."
        )
        tool = "SAMPLE_RECEIPTS"
    else:
        answer = analytics["summary"]
        tool = "SAMPLE_ANALYTICS"

    answer += " These results use bundled synthetic data; no AI model is called."
    return {
        "response": answer,
        "execution_trace": [{
            "step_number": 1,
            "tool_selected": tool,
            "tool_input": query[:200],
            "tool_output": "Bundled synthetic portfolio-demo records",
            "reasoning": "Deterministic demo response; no live financial data or LLM inference.",
            "latency_ms": 0.0,
        }],
        "total_latency_ms": 0.0,
        "steps_taken": 1,
    }
