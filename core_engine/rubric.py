"""
Advanced Discourse Modeling Taxonomy & Policy Profiles
Clean-room implementation grounded in UC Berkeley EECS-2025-55 & computational linguistics.
"""

TAXONOMY = {
    "epistemic_substance": {
        "title": "Epistemic Substance & Grounding",
        "description": "Evaluates factual grounding, empirical claims, citations, quantitative references, and structured logical deduction.",
        "dimensions": [
            "empirical_evidence",      # Mentions data, statistics, studies, concrete dates/locations
            "reasoning_structure",     # Uses logical premises leading to a stated conclusion
            "falsifiability",          # Articulates a clear, testable claim rather than a vague aesthetic preference
            "intellectual_humility"    # Acknowledges nuance or boundary conditions
        ]
    },
    "discourse_ethics": {
        "title": "Discourse Ethics & Civility",
        "description": "Measures conversational respect, absence of ad hominem, bad-faith rhetoric, harassment, and conversational empathy.",
        "dimensions": [
            "target_directedness",     # Attacks arguments vs attacking individual identity/character
            "emotional_temperature",   # High-temperature hostility vs measured critique
            "rhetorical_fairness",     # Absence of whataboutism, bad-faith strawmanning, and mocking
            "community_inclusivity"    # Freedom from slurs, intimidation, and exclusionary jargon
        ]
    },
    "constructive_utility": {
        "title": "Constructive Utility & Synthesis",
        "description": "Measures whether the contribution advances the state of the conversation, synthesizes disparate ideas, or proposes solutions.",
        "dimensions": [
            "novelty_increment",       # Adds new angles not already settled in the discussion
            "actionable_alternative",  # Proposes a viable fix, counter-model, or next step
            "synthetic_integration",   # Connects two opposing arguments into a coherent third model
            "clarifying_inquiry"       # Asks sharp, probing questions that unblock stagnant debate
        ]
    },
    "dialectical_relevance": {
        "title": "Dialectical Relevance & Signal-to-Noise",
        "description": "Evaluates anchor integrity to the root topic, resistance to derailment, and conciseness.",
        "dimensions": [
            "topical_cohesion",        # Stays tightly bounded to the core subject matter
            "signal_density",          # High information ratio per word; low repetitive filler
            "anti_derailment",         # Resists introducing partisan or off-topic wedge themes
            "contextual_coherence"     # Direct logical relationship to parent claim
        ]
    }
}

# Configurable Community Policy Profiles
POLICY_PROFILES = {
    "newsroom": {
        "name": "Journalistic Newsroom & Editorial",
        "description": "Balanced high-civility profile with emphasis on constructive counter-arguments and reduction of partisan hostility.",
        "weights": {
            "constructiveness": 0.35,
            "civility": 0.30,
            "persuasiveness": 0.20,
            "relevance": 0.15
        },
        "thresholds": {"auto_approve": 72, "review": 48, "reject": 28}
    },
    "academic": {
        "name": "Academic & Scientific Peer Exchange",
        "description": "Rigorous epistemic evaluation. Heavily weights empirical data, citations, and logical rigor over simple politeness.",
        "weights": {
            "constructiveness": 0.45,
            "civility": 0.20,
            "persuasiveness": 0.25,
            "relevance": 0.10
        },
        "thresholds": {"auto_approve": 78, "review": 52, "reject": 30}
    },
    "tech_community": {
        "name": "Developer & Open Source Forum",
        "description": "Prioritizes actionable technical solutions, reproducible details, and low noise over formal language.",
        "weights": {
            "constructiveness": 0.40,
            "civility": 0.20,
            "persuasiveness": 0.20,
            "relevance": 0.20
        },
        "thresholds": {"auto_approve": 70, "review": 45, "reject": 25}
    },
    "casual_social": {
        "name": "General Community & Social Hub",
        "description": "Relaxed tone standards, but strict filtering against targeted harassment, slurs, and spam.",
        "weights": {
            "constructiveness": 0.25,
            "civility": 0.40,
            "persuasiveness": 0.15,
            "relevance": 0.20
        },
        "thresholds": {"auto_approve": 65, "review": 40, "reject": 20}
    }
}

def get_all_policies() -> dict:
    """Returns combined built-in and dynamic custom policies from database."""
    policies = dict(POLICY_PROFILES)
    try:
        from storage.db import get_custom_policies
        custom = get_custom_policies()
        policies.update(custom)
    except Exception:
        pass
    return policies
