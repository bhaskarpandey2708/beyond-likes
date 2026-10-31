"""
Token Economics & Margin Simulator for Beyond Likes SaaS
Calculates compute inference cost per 10k evaluations against SaaS subscription pricing.
"""
import json

# Pricing per million tokens (Oct 2026 industry benchmarks)
MODEL_PRICING = {
    "gemini-flash": {"input_per_m": 0.075, "output_per_m": 0.30},
    "gpt-4o-mini": {"input_per_m": 0.15, "output_per_m": 0.60},
    "claude-3-haiku": {"input_per_m": 0.25, "output_per_m": 1.25},
    "local-heuristic": {"input_per_m": 0.00, "output_per_m": 0.00} # $0 marginal API cost
}

PLANS = {
    "starter": {"name": "Starter / Indie", "price_per_month": 49.0, "included_evals": 25000},
    "pro": {"name": "Professional Newsroom", "price_per_month": 199.0, "included_evals": 150000},
    "enterprise": {"name": "Enterprise Platform", "price_per_month": 599.0, "included_evals": 600000}
}

def simulate_economics(avg_comment_tokens=75, avg_response_tokens=65, model="gemini-flash"):
    """
    Computes unit economics, gross margins, and cost per 1,000 requests.
    """
    rates = MODEL_PRICING.get(model, MODEL_PRICING["gemini-flash"])
    
    # Cost per single evaluation
    input_cost = (avg_comment_tokens / 1_000_000.0) * rates["input_per_m"]
    output_cost = (avg_response_tokens / 1_000_000.0) * rates["output_per_m"]
    total_cost_per_eval = input_cost + output_cost
    cost_per_1k = total_cost_per_eval * 1000.0
    cost_per_10k = total_cost_per_eval * 10000.0

    report = {
        "model": model,
        "assumptions": {
            "avg_comment_tokens": avg_comment_tokens,
            "avg_response_tokens": avg_response_tokens,
            "input_cost_per_m": f"${rates['input_per_m']}",
            "output_cost_per_m": f"${rates['output_per_m']}"
        },
        "unit_costs": {
            "per_single_eval_usd": round(total_cost_per_eval, 6),
            "per_1k_evals_usd": round(cost_per_1k, 4),
            "per_10k_evals_usd": round(cost_per_10k, 4)
        },
        "plan_margins": {}
    }

    for plan_key, plan in PLANS.items():
        evals = plan["included_evals"]
        revenue = plan["price_per_month"]
        cogs = evals * total_cost_per_eval
        gross_profit = revenue - cogs
        margin_pct = (gross_profit / revenue) * 100.0

        report["plan_margins"][plan_key] = {
            "plan_name": plan["name"],
            "monthly_price": f"${revenue:.2f}",
            "included_evals": f"{evals:,}",
            "monthly_cogs": f"${cogs:.2f}",
            "gross_profit": f"${gross_profit:.2f}",
            "gross_margin_pct": f"{margin_pct:.1f}%",
            "viable": margin_pct >= 75.0
        }

    return report

if __name__ == "__main__":
    import sys
    model_choice = sys.argv[1] if len(sys.argv) > 1 else "gemini-flash"
    result = simulate_economics(model=model_choice)
    print(json.dumps(result, indent=2))
