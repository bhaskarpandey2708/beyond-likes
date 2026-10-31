"""
Platform Webhook Handlers for Beyond Likes
Parses native webhook events from Discourse, WordPress, and Custom Platform Bots.
"""
from typing import Dict, Any, Tuple
from core_engine.evaluator import NormativeEvaluator
from core_engine.rephraser import RephraseAdvisor
from storage.db import store_result
from api.events import broadcaster

evaluator = NormativeEvaluator()

def process_discourse_webhook(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handles Discourse 'post_created' or 'post_edited' event payloads.
    Discourse schema:
    {
      "post": {
        "id": 1234,
        "raw": "Comment text...",
        "username": "user",
        "topic_id": 5678
      }
    }
    """
    post = payload.get("post", {})
    text = post.get("raw", "")
    post_id = post.get("id")
    username = post.get("username", "anonymous")

    if not text:
        return {"action": "ignore", "reason": "Empty post body"}

    res = evaluator.evaluate(text, policy="tech_community")
    guidance = RephraseAdvisor.generate_suggestions(res, text)
    res["guidance"] = guidance
    store_result(text, res, client_key=f"discourse:{username}", latency_ms=res["metrics"]["latency_ms"])

    broadcaster.broadcast("webhook_comment", {
        "timestamp": "now",
        "platform": "Discourse",
        "author": username,
        "text": text[:160],
        "composite_score": res["composite_score"],
        "status": res["status"],
        "dimensions": res["dimensions"],
        "flags": res["flags"],
        "suggested_revision": guidance.get("suggested_revision", "")
    })

    composite = res["composite_score"]
    status = res["status"]

    if status == "APPROVED_PROMOTED":
        action = "pin_or_promote"
    elif status == "FLAGGED_UNCIVIL" or status == "FLAGGED_SPAM":
        action = "quarantine_and_nudge"
    elif status == "NEEDS_IMPROVEMENT":
        action = "enqueue_for_review"
    else:
        action = "publish_standard"

    return {
        "platform": "discourse",
        "post_id": post_id,
        "username": username,
        "action": action,
        "discourse_score": composite,
        "dimensions": res["dimensions"],
        "needs_nudge": guidance["needs_revision"],
        "suggested_revision": guidance["suggested_revision"],
        "prosocial_nudge": guidance["prosocial_nudge"]
    }

def process_wordpress_webhook(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handles WordPress comment submission payloads:
    {
      "comment_ID": 101,
      "comment_content": "Text...",
      "comment_author": "name",
      "comment_author_email": "email"
    }
    """
    text = payload.get("comment_content", "")
    comment_id = payload.get("comment_ID")
    author = payload.get("comment_author", "guest")

    if not text:
        return {"comment_status": "spam", "reason": "Empty content"}

    res = evaluator.evaluate(text, policy="newsroom")
    guidance = RephraseAdvisor.generate_suggestions(res, text)
    res["guidance"] = guidance
    store_result(text, res, client_key=f"wordpress:{author}", latency_ms=res["metrics"]["latency_ms"])

    broadcaster.broadcast("webhook_comment", {
        "timestamp": "now",
        "platform": "WordPress",
        "author": author,
        "text": text[:160],
        "composite_score": res["composite_score"],
        "status": res["status"],
        "dimensions": res["dimensions"],
        "flags": res["flags"],
        "suggested_revision": guidance.get("suggested_revision", "")
    })

    # Map to standard WordPress approval states (1 = approve, 0 = hold/moderation, 'spam' = spam)
    if res["status"] == "FLAGGED_SPAM":
        wp_status = "spam"
    elif res["status"] == "FLAGGED_UNCIVIL":
        wp_status = "0" # Hold in moderation queue
    elif res["status"] == "APPROVED_PROMOTED" or res["status"] == "STANDARD_PUBLISH":
        wp_status = "1" # Auto-approve
    else:
        wp_status = "0" # Hold for review

    return {
        "platform": "wordpress",
        "comment_ID": comment_id,
        "recommended_wp_status": wp_status,
        "composite_score": res["composite_score"],
        "status_label": res["status"],
        "guidance": guidance
    }
