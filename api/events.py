"""
Real-Time Event Broadcaster & Server-Sent Events (SSE) Layer
Enables real-time push notifications of evaluated discourse comments
to connected dashboards, moderation consoles, and downstream webhooks.
"""
import json
import time
import queue
import threading
from typing import Dict, Any, List

class EventBroadcaster:
    """Thread-safe publish-subscribe event broker for real-time SSE streaming."""

    def __init__(self):
        self._listeners: List[queue.Queue] = []
        self._lock = threading.Lock()

    def subscribe(self) -> queue.Queue:
        """Subscribes a new client and returns an event queue."""
        q = queue.Queue(maxsize=100)
        with self._lock:
            self._listeners.append(q)
        return q

    def unsubscribe(self, q: queue.Queue):
        """Removes a client event queue."""
        with self._lock:
            if q in self._listeners:
                self._listeners.remove(q)

    def broadcast(self, event_type: str, data: Dict[str, Any]):
        """Broadcasts a structured event payload to all active subscribers."""
        event_payload = {
            "event": event_type,
            "timestamp": time.time(),
            "data": data
        }
        with self._lock:
            dead_queues = []
            for q in self._listeners:
                try:
                    q.put_nowait(event_payload)
                except queue.Full:
                    dead_queues.append(q)
            for dq in dead_queues:
                if dq in self._listeners:
                    self._listeners.remove(dq)

# Global singleton broadcaster instance
broadcaster = EventBroadcaster()
