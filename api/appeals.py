"""
DSA Article 20 Appeals & Reversal Workflow Engine for Beyond Likes
Handles user self-correction appeals, automated re-scoring of constructive revisions,
and human moderator decision routing.
"""

from typing import Dict, Any, Optional
from core_engine.evaluator import NormativeEvaluator
from storage.db import create_appeal, get_appeals, resolve_appeal, get_connection
from api.dispatcher import dispatcher
from api.events import broadcaster

evaluator = NormativeEvaluator()


class AppealsEngine:
    """
    Manages statutory user appeal lifecycles under EU DSA Article 20.
    """

    @staticmethod
    def submit_appeal(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a user appeal. If user provides a constructive revised text,
        evaluates improvement and performs automated reversal if quality standards are met.
        """
        user_id = data.get("user_id", "anonymous_user")
        original_text = data.get("original_text", "")
        appeal_reason = data.get("reason", "Disagreement with moderation decision.")
        eval_id = data.get("evaluation_id")
        revised_text = data.get("revised_text", "").strip()

        original_status = data.get("original_status", "NEEDS_IMPROVEMENT")
        original_score = float(data.get("original_score", 30.0))

        # Try to locate original evaluation in database if evaluation_id provided
        if eval_id and (not original_text or original_score == 30.0):
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT text_snippet, composite_score, status FROM evaluations WHERE id = ?", (eval_id,))
                row = cursor.fetchone()
                if row:
                    original_text = original_text or row["text_snippet"]
                    original_score = float(row["composite_score"])
                    original_status = row["status"]

        revised_score = None
        revised_status = None
        decision = "PENDING"
        moderator_notes = ""

        # Automated Re-Scoring of Revised Text
        if revised_text:
            eval_res = evaluator.evaluate(revised_text)
            revised_score = eval_res["composite_score"]
            revised_status = eval_res["status"]

            # If user demonstrated constructive self-correction (civility >= 65 and score >= 60)
            if eval_res["dimensions"]["civility"] >= 65.0 and revised_score >= 60.0:
                decision = "REVERSED_CONSTRUCTIVE"
                moderator_notes = (
                    f"Automated Reversal under DSA Article 20: User provided constructive revision "
                    f"improving score from {original_score} to {revised_score} pts."
                )

        appeal_id = create_appeal(
            user_id=user_id,
            original_text=original_text or "Unspecified snippet",
            original_status=original_status,
            original_score=original_score,
            appeal_reason=appeal_reason,
            evaluation_id=eval_id,
            revised_text=revised_text if revised_text else None,
            revised_score=revised_score,
            revised_status=revised_status,
            decision=decision,
            moderator_notes=moderator_notes
        )

        # Notify via SSE and Outbound Webhooks
        event_name = "appeal_auto_reversed" if decision == "REVERSED_CONSTRUCTIVE" else "appeal_submitted"
        event_payload = {
            "appeal_id": appeal_id,
            "user_id": user_id,
            "decision": decision,
            "original_score": original_score,
            "revised_score": revised_score,
            "reason": appeal_reason
        }
        broadcaster.broadcast(event_name, event_payload)
        dispatcher.dispatch(event_name, event_payload)

        return {
            "appeal_id": appeal_id,
            "user_id": user_id,
            "decision": decision,
            "status": "AUTO_REVERSED" if decision == "REVERSED_CONSTRUCTIVE" else "PENDING_MODERATOR_REVIEW",
            "original_score": original_score,
            "revised_score": revised_score,
            "moderator_notes": moderator_notes or "Enqueued for human moderator review within 24h SLA."
        }

    @staticmethod
    def resolve_appeal_action(appeal_id: int, decision: str, moderator_notes: str = "") -> Dict[str, Any]:
        """Processes manual moderator determination on an appeal."""
        allowed_decisions = ["ACCEPTED_MODERATOR", "REJECTED", "REVERSED_CONSTRUCTIVE"]
        if decision not in allowed_decisions:
            return {"success": False, "error": f"Invalid decision. Must be one of {allowed_decisions}"}

        ok = resolve_appeal(appeal_id=appeal_id, decision=decision, moderator_notes=moderator_notes)
        if not ok:
            return {"success": False, "error": f"Appeal ID {appeal_id} not found."}

        event_payload = {
            "appeal_id": appeal_id,
            "decision": decision,
            "moderator_notes": moderator_notes
        }
        broadcaster.broadcast("appeal_resolved", event_payload)
        dispatcher.dispatch("appeal_resolved", event_payload)

        return {
            "success": True,
            "appeal_id": appeal_id,
            "decision": decision,
            "moderator_notes": moderator_notes
        }
