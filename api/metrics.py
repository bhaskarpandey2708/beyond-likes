"""
Prometheus & OpenMetrics Telemetry Engine for Beyond Likes
Tracks real-time system metrics, latency percentiles, tenant throughput,
discourse civility distributions, and cache efficiency for enterprise observability.
"""

import time
import threading
from typing import Dict, List, Tuple
from collections import defaultdict

class MetricsRegistry:
    def __init__(self):
        self._lock = threading.Lock()
        
        # Counters: {(endpoint, method, status): count}
        self.requests_total: Dict[Tuple[str, str, int], int] = defaultdict(int)
        
        # Latency buckets (in seconds): [0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5]
        self.latency_buckets = [0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5]
        # Latency counts: {(endpoint, tier): [bucket_counts...]}
        self.latency_histogram: Dict[Tuple[str, str], List[int]] = defaultdict(lambda: [0] * len(self.latency_buckets))
        self.latency_sum: Dict[Tuple[str, str], float] = defaultdict(float)
        self.latency_count: Dict[Tuple[str, str], int] = defaultdict(int)

        # Cache counters
        self.cache_hits: int = 0
        self.cache_misses: int = 0

        # Safety & Prosocial counters
        self.false_positives_salvaged: int = 0
        self.stealth_interceptions: int = 0
        self.appeals_reversed: int = 0
        self.comments_evaluated_total: int = 0

        # Composite score buckets: [20, 40, 60, 80, 100]
        self.score_buckets = [20.0, 40.0, 60.0, 80.0, 100.0]
        self.score_histogram: List[int] = [0] * len(self.score_buckets)
        self.score_sum: float = 0.0
        self.score_count: int = 0

        self.start_time = time.time()

    def record_request(self, endpoint: str, method: str, status_code: int, duration_sec: float, tier: str = "heuristic"):
        with self._lock:
            # Increment request counter
            clean_endpoint = endpoint.split("?")[0]
            self.requests_total[(clean_endpoint, method, status_code)] += 1

            # Update latency histogram
            key = (clean_endpoint, tier)
            self.latency_count[key] += 1
            self.latency_sum[key] += duration_sec
            for i, b in enumerate(self.latency_buckets):
                if duration_sec <= b:
                    self.latency_histogram[key][i] += 1

    def record_cache_hit(self):
        with self._lock:
            self.cache_hits += 1

    def record_cache_miss(self):
        with self._lock:
            self.cache_misses += 1

    def record_evaluation(self, composite_score: float, status: str, salvaged: bool = False, stealth: bool = False):
        with self._lock:
            self.comments_evaluated_total += 1
            self.score_count += 1
            self.score_sum += composite_score
            for i, b in enumerate(self.score_buckets):
                if composite_score <= b:
                    self.score_histogram[i] += 1

            if salvaged:
                self.false_positives_salvaged += 1
            if stealth:
                self.stealth_interceptions += 1

    def record_appeal_reversal(self):
        with self._lock:
            self.appeals_reversed += 1

    def export_openmetrics(self) -> str:
        """
        Serializes current telemetry into Prometheus / OpenMetrics text exposition format (RFC 0001).
        """
        with self._lock:
            lines = [
                "# HELP beyond_likes_uptime_seconds Total seconds since engine booted.",
                "# TYPE beyond_likes_uptime_seconds gauge",
                f"beyond_likes_uptime_seconds {round(time.time() - self.start_time, 2)}",
                "",
                "# HELP beyond_likes_requests_total Total HTTP requests handled.",
                "# TYPE beyond_likes_requests_total counter"
            ]

            for (endpoint, method, code), count in sorted(self.requests_total.items()):
                lines.append(f'beyond_likes_requests_total{{endpoint="{endpoint}",method="{method}",status="{code}"}} {count}')

            lines.extend([
                "",
                "# HELP beyond_likes_request_duration_seconds Latency histogram per endpoint and tier.",
                "# TYPE beyond_likes_request_duration_seconds histogram"
            ])

            for (endpoint, tier), bucket_counts in sorted(self.latency_histogram.items()):
                cumulative = 0
                for i, b in enumerate(self.latency_buckets):
                    cumulative += bucket_counts[i]
                    lines.append(f'beyond_likes_request_duration_seconds_bucket{{endpoint="{endpoint}",tier="{tier}",le="{b}"}} {cumulative}')
                # +Inf bucket
                total_cnt = self.latency_count[(endpoint, tier)]
                lines.append(f'beyond_likes_request_duration_seconds_bucket{{endpoint="{endpoint}",tier="{tier}",le="+Inf"}} {total_cnt}')
                lines.append(f'beyond_likes_request_duration_seconds_sum{{endpoint="{endpoint}",tier="{tier}"}} {round(self.latency_sum[(endpoint, tier)], 6)}')
                lines.append(f'beyond_likes_request_duration_seconds_count{{endpoint="{endpoint}",tier="{tier}"}} {total_cnt}')

            lines.extend([
                "",
                "# HELP beyond_likes_cache_hits_total Total responses served directly from SQLite cache.",
                "# TYPE beyond_likes_cache_hits_total counter",
                f"beyond_likes_cache_hits_total {self.cache_hits}",
                "",
                "# HELP beyond_likes_cache_misses_total Total cache misses requiring pipeline evaluation.",
                "# TYPE beyond_likes_cache_misses_total counter",
                f"beyond_likes_cache_misses_total {self.cache_misses}",
                "",
                "# HELP beyond_likes_comments_evaluated_total Cumulative comments evaluated across all modes.",
                "# TYPE beyond_likes_comments_evaluated_total counter",
                f"beyond_likes_comments_evaluated_total {self.comments_evaluated_total}",
                "",
                "# HELP beyond_likes_false_positives_salvaged_total Legitimate comments rescued from false toxicity blocks.",
                "# TYPE beyond_likes_false_positives_salvaged_total counter",
                f"beyond_likes_false_positives_salvaged_total {self.false_positives_salvaged}",
                "",
                "# HELP beyond_likes_stealth_interceptions_total Covert bad-faith attacks intercepted despite low legacy toxicity.",
                "# TYPE beyond_likes_stealth_interceptions_total counter",
                f"beyond_likes_stealth_interceptions_total {self.stealth_interceptions}",
                "",
                "# HELP beyond_likes_appeals_reversed_total Moderation appeals successfully reversed through constructive revision.",
                "# TYPE beyond_likes_appeals_reversed_total counter",
                f"beyond_likes_appeals_reversed_total {self.appeals_reversed}",
                "",
                "# HELP beyond_likes_composite_score Distribution of 0-100 discourse quality scores.",
                "# TYPE beyond_likes_composite_score histogram"
            ])

            cumulative_scores = 0
            for i, b in enumerate(self.score_buckets):
                cumulative_scores += self.score_histogram[i]
                lines.append(f'beyond_likes_composite_score_bucket{{le="{b}"}} {cumulative_scores}')
            lines.append(f'beyond_likes_composite_score_bucket{{le="+Inf"}} {self.score_count}')
            lines.append(f'beyond_likes_composite_score_sum {round(self.score_sum, 2)}')
            lines.append(f'beyond_likes_composite_score_count {self.score_count}')
            lines.append("")

            return "\n".join(lines) + "\n"

# Global telemetry registry singleton
telemetry = MetricsRegistry()
