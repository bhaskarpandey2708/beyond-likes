"""
Enterprise Moderation Action & Routing Rules Engine
Translates normative multidimensional discourse scores into automated,
policy-driven execution actions for community platforms and CMSs.
"""
from typing import Dict, Any, List

DEFAULT_RULES = [
    {
        "id": "RULE_AUTO_PIN",
        "name": "Auto-Pin Epistemic Contributions",
        "condition": lambda r: r["dimensions"]["constructiveness"] >= 75.0 and r["dimensions"]["civility"] >= 75.0,
        "action": "PIN_AND_FEATURE",
        "priority": "HIGH",
        "reason": "Top-decile epistemic grounding and synthesis.",
        "badge": "Top Perspective"
    },
    {
        "id": "RULE_QUARANTINE_UNCIVIL",
        "name": "Automated Hostility Quarantine",
        "condition": lambda r: r["dimensions"]["civility"] < 40.0 or r["flags"].get("is_toxic", False),
        "action": "QUARANTINE_AND_NUDGE",
        "priority": "CRITICAL",
        "reason": "Hostile attack, harassment, or severe vulgarity.",
        "badge": "Quarantined"
    },
    {
        "id": "RULE_BLOCK_SPAM",
        "name": "Commercial Spam Interception",
        "condition": lambda r: r["flags"].get("is_spam", False),
        "action": "BLOCK_PERMANENTLY",
        "priority": "CRITICAL",
        "reason": "Commercial link or unauthorized promotional text.",
        "badge": "Spam Blocked"
    },
    {
        "id": "RULE_WHATABOUTISM_NUDGE",
        "name": "Rhetorical Deflection In-Composer Nudge",
        "condition": lambda r: r["substance_breakdown"].get("fallacy_count", 0) >= 2 and r["substance_breakdown"].get("epistemic_evidence_count", 0) == 0,
        "action": "ATTACH_PROSOCIAL_NUDGE",
        "priority": "MEDIUM",
        "reason": "Rhetorical deflection without constructive evidence.",
        "badge": "Needs Evidence"
    },
    {
        "id": "RULE_LOW_EFFORT_PROMPT",
        "name": "Low-Effort Substantiation Prompt",
        "condition": lambda r: r["metrics"]["word_count"] < 6 and r["dimensions"]["constructiveness"] < 30.0,
        "action": "PROMPT_FOR_DETAIL",
        "priority": "LOW",
        "reason": "Low informational depth; invite user to elaborate.",
        "badge": "Low Substance"
    }
]

def evaluate_action_rules(eval_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates an evaluation result against active action rules
    and returns recommended moderation execution routing.
    """
    triggered_rules = []

    for rule in DEFAULT_RULES:
        try:
            if rule["condition"](eval_result):
                triggered_rules.append({
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "action": rule["action"],
                    "priority": rule["priority"],
                    "reason": rule["reason"],
                    "badge": rule["badge"]
                })
        except Exception:
            continue

    if not triggered_rules:
        primary_action = "STANDARD_PUBLISH"
        priority = "LOW"
        badge = "Standard"
        summary = "Passed community standards without special routing."
    else:
        # Sort by priority: CRITICAL > HIGH > MEDIUM > LOW
        prio_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        triggered_rules.sort(key=lambda x: prio_order.get(x["priority"], 99))
        primary = triggered_rules[0]
        primary_action = primary["action"]
        priority = primary["priority"]
        badge = primary["badge"]
        summary = primary["reason"]

    return {
        "primary_action": primary_action,
        "priority": priority,
        "recommended_badge": badge,
        "action_summary": summary,
        "all_triggered_rules": triggered_rules
    }
