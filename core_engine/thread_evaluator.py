"""
Multi-Turn Conversational Thread Evaluator & Escalation Engine
Evaluates dynamic discourse trajectories across parent-child reply trees.
Computes Thread Escalation Index (TEI), de-escalator recognition, and automated thread interventions.
"""

import math
from typing import List, Dict, Any, Optional
from .evaluator import NormativeEvaluator


class ThreadEvaluator:
    """
    Evaluates multi-turn conversation threads to detect flame wars,
    epistemic drift, and de-escalation actions in real time.
    """

    def __init__(self, evaluator_instance: Optional[NormativeEvaluator] = None):
        self.evaluator = evaluator_instance or NormativeEvaluator()

    def analyze_thread(
        self,
        comments: List[Dict[str, Any]],
        topic: str = "",
        policy: str = "newsroom",
        backend: str = "heuristic"
    ) -> Dict[str, Any]:
        """
        Analyze an entire reply chain or conversational thread.
        Each comment dict must contain:
          - id: str or int
          - author: str
          - text: str
          - reply_to: optional ID of the parent comment
          - timestamp: optional float or str
        """
        if not comments:
            return {
                "error": "No comments provided in thread",
                "thread_status": "EMPTY",
                "thread_escalation_index": 0.0,
                "recommended_action": "NO_OP"
            }

        # Index comments by id
        comment_map = {}
        annotated_turns = []
        civility_series = []
        constructiveness_series = []
        authors_seen = set()

        de_escalators = set()
        instigators = set()
        constructive_leaders = set()

        total_score = 0.0
        escalation_events = 0
        de_escalation_events = 0
        flagged_count = 0

        pinnacle_comment = None
        max_composite = -1.0

        for idx, item in enumerate(comments):
            c_id = str(item.get("id", idx + 1))
            author = item.get("author", f"User_{idx + 1}")
            text = item.get("text", "")
            reply_to = str(item.get("reply_to")) if item.get("reply_to") is not None else None
            timestamp = item.get("timestamp")

            authors_seen.add(author)

            # Evaluate comment individually
            eval_res = self.evaluator.evaluate(text, policy=policy, backend=backend)
            composite = eval_res["composite_score"]
            dims = eval_res["dimensions"]
            flags = eval_res["flags"]
            status = eval_res["status"]

            total_score += composite
            civility_series.append(dims["civility"])
            constructiveness_series.append(dims["constructiveness"])

            if "FLAGGED" in status:
                flagged_count += 1

            # Check pinnacle comment
            if composite > max_composite and dims["civility"] >= 70:
                max_composite = composite
                pinnacle_comment = {
                    "id": c_id,
                    "author": author,
                    "text": text,
                    "composite_score": composite,
                    "constructiveness": dims["constructiveness"]
                }

            if composite >= 75 and dims["constructiveness"] >= 75:
                constructive_leaders.add(author)

            # Analyze relation to parent comment
            turn_role = "STANDARD_REPLY"
            civility_delta = 0.0

            if reply_to and reply_to in comment_map:
                parent = comment_map[reply_to]
                parent_civ = parent["dimensions"]["civility"]
                current_civ = dims["civility"]
                civility_delta = round(current_civ - parent_civ, 1)

                # De-escalation condition: parent was low civility, current is high civility
                if parent_civ < 50 and current_civ >= 70:
                    turn_role = "DE_ESCALATOR"
                    de_escalators.add(author)
                    de_escalation_events += 1

                # Escalation condition: parent was civil, current is significantly lower
                elif current_civ < 40 and parent_civ >= 60:
                    turn_role = "ESCALATOR"
                    instigators.add(author)
                    escalation_events += 1

                # Sustained flame war turn
                elif current_civ < 40 and parent_civ < 40:
                    turn_role = "FLAME_WAR_EXCHANGE"
                    escalation_events += 1

            elif idx == 0:
                turn_role = "THREAD_STARTER"

            annotated_turn = {
                "turn": idx + 1,
                "id": c_id,
                "author": author,
                "reply_to": reply_to,
                "text": text,
                "composite_score": composite,
                "dimensions": dims,
                "flags": flags,
                "status": status,
                "civility_delta": civility_delta,
                "turn_role": turn_role
            }

            comment_map[c_id] = annotated_turn
            annotated_turns.append(annotated_turn)

        n_comments = len(comments)
        avg_score = round(total_score / n_comments, 1)
        flag_ratio = flagged_count / n_comments

        # -------------------------------------------------------------
        # Thread Escalation Index (TEI) Calculation (0 to 100)
        # -------------------------------------------------------------
        # Base factor: proportion of flagged / uncivil comments
        base_tei = flag_ratio * 55.0

        # Escalation dynamic: ratio of escalating turns
        if n_comments > 1:
            escalation_penalty = (escalation_events / (n_comments - 1)) * 35.0
            de_escalation_discount = (de_escalation_events / (n_comments - 1)) * 25.0
        else:
            escalation_penalty = 0.0
            de_escalation_discount = 0.0

        # Civility slope across last 3 turns
        recent_slope_penalty = 0.0
        if len(civility_series) >= 3:
            slope = civility_series[-1] - civility_series[-3]
            if slope < -25:
                recent_slope_penalty = 15.0  # Rapid recent downturn
            elif slope > 25:
                recent_slope_penalty = -10.0 # Rapid recent recovery

        raw_tei = base_tei + escalation_penalty - de_escalation_discount + recent_slope_penalty
        tei = round(max(0.0, min(100.0, raw_tei)), 1)

        # -------------------------------------------------------------
        # Determine Thread Status & Recommended Action
        # -------------------------------------------------------------
        if tei <= 20.0 and avg_score >= 75.0:
            status = "EXEMPLARY_DELIBERATION"
            action = "PIN_BEST_PRACTICE"
            action_desc = "High-quality constructive exchange. Consider highlighting to community."
        elif tei <= 40.0:
            status = "HEALTHY_DEBATE"
            action = "ALLOW_CONTINUE"
            action_desc = "Discourse is within acceptable normative bounds. No intervention needed."
        elif tei <= 65.0:
            status = "TENSION_ELEVATED"
            action = "PROSOCIAL_BANNER_NUDGE"
            action_desc = "Moderate hostility detected. Display in-thread prosocial guidance reminder."
        elif tei <= 80.0:
            status = "ESCALATING_HOSTILITY"
            action = "ACTIVATE_SLOW_MODE"
            action_desc = "Hostility escalating across reply turns. Recommend a 10-minute reply cooldown."
        else:
            status = "ACTIVE_FLAME_WAR"
            action = "AUTO_LOCK_OR_QUARANTINE"
            action_desc = "Severe flame war detected. Quarantine or lock thread to halt toxic contagion."

        return {
            "topic": topic,
            "total_comments": n_comments,
            "unique_participants": len(authors_seen),
            "average_discourse_health": avg_score,
            "thread_escalation_index": tei,
            "thread_status": status,
            "action_routing": {
                "action": action,
                "description": action_desc,
                "urgency": "HIGH" if tei >= 70 else ("MEDIUM" if tei >= 45 else "LOW")
            },
            "pinnacle_comment": pinnacle_comment,
            "key_actors": {
                "constructive_leaders": list(constructive_leaders),
                "de_escalators": list(de_escalators),
                "instigators": list(instigators)
            },
            "metrics": {
                "escalation_events": escalation_events,
                "de_escalation_events": de_escalation_events,
                "flagged_comments": flagged_count,
                "civility_trajectory": civility_series
            },
            "annotated_turns": annotated_turns
        }
