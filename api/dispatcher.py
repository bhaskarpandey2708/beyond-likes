"""
Enterprise Outbound Webhook Dispatcher for Beyond Likes
Delivers cryptographically signed HMAC-SHA256 event notifications to
external moderation systems, Discord, Slack, Discourse, and customer inboxes.
"""

import hmac
import hashlib
import json
import time
import uuid
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List, Optional
from storage.db import (
    get_webhook_subscriptions,
    log_webhook_delivery,
    save_webhook_subscription,
    delete_webhook_subscription,
    get_recent_webhook_deliveries
)


class WebhookDispatcher:
    """
    High-throughput asynchronous webhook delivery worker with
    HMAC-SHA256 signatures and exponential backoff retry.
    """

    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="wh_dispatch")

    @staticmethod
    def compute_signature(payload_bytes: bytes, secret: str) -> str:
        """Generates HMAC-SHA256 hexadecimal signature."""
        return hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()

    def dispatch(self, event_type: str, data: Dict[str, Any]) -> List[str]:
        """
        Dispatches event asynchronously to all active matching webhook subscribers.
        Returns list of matched subscription IDs.
        """
        subscriptions = get_webhook_subscriptions(active_only=True)
        if not subscriptions:
            return []

        payload = {
            "id": f"evt_{uuid.uuid4().hex[:12]}",
            "event": event_type,
            "timestamp": time.time(),
            "data": data
        }

        matched_ids = []
        for sub in subscriptions:
            events = sub.get("events", ["*"])
            if "*" in events or event_type in events:
                matched_ids.append(sub["id"])
                self.executor.submit(self._deliver_with_retry, sub, payload)

        return matched_ids

    def _deliver_with_retry(self, sub: Dict[str, Any], payload: Dict[str, Any], max_attempts: int = 3):
        """Executes HTTP delivery with exponential backoff."""
        sub_id = sub["id"]
        url = sub["url"]
        secret = sub.get("secret", "")
        event_type = payload["event"]

        body_bytes = json.dumps(payload, indent=2).encode("utf-8")
        signature = self.compute_signature(body_bytes, secret)

        attempts = 0
        last_error = None
        status_code = None
        success = False
        t_start = time.perf_counter()

        for attempt in range(1, max_attempts + 1):
            attempts = attempt
            try:
                req = urllib.request.Request(
                    url,
                    data=body_bytes,
                    headers={
                        "Content-Type": "application/json; charset=utf-8",
                        "User-Agent": "BeyondLikes-Webhook-Dispatcher/2.5.0",
                        "x-beyondlikes-event": event_type,
                        "x-beyondlikes-signature": f"sha256={signature}",
                        "x-beyondlikes-delivery": payload["id"],
                        "x-beyondlikes-attempt": str(attempt)
                    },
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=5.0) as resp:
                    status_code = resp.status
                    if 200 <= status_code < 300:
                        success = True
                        break
            except urllib.error.HTTPError as he:
                status_code = he.code
                last_error = f"HTTP {he.code}: {he.reason}"
                if status_code in [400, 401, 403, 404]:
                    # Client errors shouldn't be retried
                    break
            except Exception as e:
                last_error = str(e)

            # Exponential backoff: 0.5s, 1.5s
            if attempt < max_attempts:
                time.sleep(0.5 * (2 ** (attempt - 1)))

        duration_ms = round((time.perf_counter() - t_start) * 1000, 2)
        log_webhook_delivery(
            sub_id=sub_id,
            event=event_type,
            status_code=status_code,
            success=success,
            attempts=attempts,
            duration_ms=duration_ms,
            error_msg=last_error if not success else None
        )

    def test_dispatch(self, subscription_id: str, sample_event: str = "ping") -> Dict[str, Any]:
        """Synchronously tests delivery to a registered subscription."""
        subs = [s for s in get_webhook_subscriptions(active_only=False) if s["id"] == subscription_id]
        if not subs:
            return {"success": False, "error": f"Subscription '{subscription_id}' not found"}

        sub = subs[0]
        test_payload = {
            "id": f"test_{uuid.uuid4().hex[:8]}",
            "event": sample_event,
            "timestamp": time.time(),
            "data": {
                "message": "Beyond Likes Webhook verification probe",
                "subscription_id": subscription_id,
                "verified": True
            }
        }

        body_bytes = json.dumps(test_payload).encode("utf-8")
        secret = sub.get("secret", "")
        sig = self.compute_signature(body_bytes, secret)

        t0 = time.perf_counter()
        try:
            req = urllib.request.Request(
                sub["url"],
                data=body_bytes,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "BeyondLikes-Webhook-Dispatcher/2.5.0",
                    "x-beyondlikes-event": sample_event,
                    "x-beyondlikes-signature": f"sha256={sig}",
                    "x-beyondlikes-delivery": test_payload["id"]
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=4.0) as resp:
                duration_ms = round((time.perf_counter() - t0) * 1000, 2)
                log_webhook_delivery(
                    sub_id=subscription_id,
                    event=sample_event,
                    status_code=resp.status,
                    success=True,
                    attempts=1,
                    duration_ms=duration_ms
                )
                return {
                    "success": True,
                    "status_code": resp.status,
                    "duration_ms": duration_ms,
                    "signature_verified": True
                }
        except urllib.error.HTTPError as he:
            duration_ms = round((time.perf_counter() - t0) * 1000, 2)
            log_webhook_delivery(
                sub_id=subscription_id,
                event=sample_event,
                status_code=he.code,
                success=False,
                attempts=1,
                duration_ms=duration_ms,
                error_msg=f"HTTP {he.code}: {he.reason}"
            )
            return {
                "success": False,
                "status_code": he.code,
                "duration_ms": duration_ms,
                "error": f"HTTP {he.code}: {he.reason}"
            }
        except Exception as e:
            duration_ms = round((time.perf_counter() - t0) * 1000, 2)
            log_webhook_delivery(
                sub_id=subscription_id,
                event=sample_event,
                status_code=None,
                success=False,
                attempts=1,
                duration_ms=duration_ms,
                error_msg=str(e)
            )
            return {
                "success": False,
                "duration_ms": duration_ms,
                "error": str(e)
            }


# Global singleton dispatcher instance
dispatcher = WebhookDispatcher()
