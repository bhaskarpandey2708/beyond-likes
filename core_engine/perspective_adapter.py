"""
Perspective API Drop-in Compatibility Adapter
Allows legacy clients integrating Google's Perspective API to seamlessly switch to Beyond Likes.
"""
import math
from typing import Dict, Any
from .evaluator import NormativeEvaluator

class PerspectiveAdapter:
    """
    Translates Google Perspective API v1alpha1 / v1 requests & responses.
    Uses logistic sigmoid curve to match Perspective's probability calibration.
    """

    def __init__(self, evaluator: NormativeEvaluator):
        self.evaluator = evaluator

    def _civility_to_toxicity(self, civility: float) -> float:
        # Standard logistic curve: midpoint at 50 civility
        prob = 1.0 / (1.0 + math.exp((civility - 50.0) / 12.0))
        return round(max(0.01, min(0.99, prob)), 3)

    def handle_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Accepts a Google Perspective API request format:
        {
          "comment": {"text": "some comment"},
          "requestedAttributes": {"TOXICITY": {}, "INSULT": {}},
          "languages": ["en"]
        }
        """
        comment_obj = payload.get("comment", {})
        text = comment_obj.get("text", "")
        requested = payload.get("requestedAttributes", {})
        if not requested:
            requested = {"TOXICITY": {}}

        languages = payload.get("languages", ["en"])

        # Run Beyond Likes evaluation
        res = self.evaluator.evaluate(text)
        dims = res.get("dimensions", {})
        civility = dims.get("civility", 100.0)

        # Invert Civility using calibrated sigmoid curve
        toxicity_prob = self._civility_to_toxicity(civility)
        insult_prob = round(max(0.01, min(0.99, toxicity_prob * 0.95)), 3)
        threat_prob = 0.02 if toxicity_prob < 0.7 else round(toxicity_prob * 0.6, 3)

        attr_scores = {}
        for attr in requested.keys():
            attr_upper = attr.upper()
            if attr_upper == "TOXICITY":
                val = toxicity_prob
            elif attr_upper == "SEVERE_TOXICITY":
                val = round(toxicity_prob * 0.7, 3)
            elif attr_upper in ("INSULT", "PROFANITY"):
                val = insult_prob
            elif attr_upper == "THREAT":
                val = threat_prob
            elif attr_upper == "IDENTITY_ATTACK":
                val = round(toxicity_prob * 0.4, 3)
            else:
                val = toxicity_prob

            attr_scores[attr_upper] = {
                "summaryScore": {
                    "value": val,
                    "type": "PROBABILITY"
                }
            }

        return {
            "attributeScores": attr_scores,
            "languages": languages,
            "detectedLanguages": languages,
            "clientToken": payload.get("clientToken", ""),
            "_beyond_likes_metadata": {
                "composite_quality_score": res["composite_score"],
                "constructiveness": dims["constructiveness"],
                "status": res["status"],
                "migration_notice": "Served by Beyond Likes Engine (Perspective Drop-in Mode)"
            }
        }
