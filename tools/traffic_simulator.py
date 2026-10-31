#!/usr/bin/env python3
"""
Beyond Likes Live Multi-Platform Traffic & Load Simulator
Simulates realistic streams of comments from Discourse, WordPress, Reddit, and forums.
Measures latency percentiles (p50, p95, p99), throughput (RPS), and triage distributions.
"""
import os
import sys
import time
import json
import random
import argparse
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any

DEFAULT_SERVER_URL = "http://localhost:8888"

SIMULATED_PERSONAS = [
    {
        "persona": "Empirical Researcher",
        "platform": "Ars Technica",
        "author": "dr_elena_watts",
        "text": "According to the 2026 IEEE comparative study, solid-state electrolytes improved round-trip efficiency by 14.8%. Furthermore, localized field trials showed a 32% reduction in thermal runaway risk over conventional NMC cells."
    },
    {
        "persona": "Hostile Troll",
        "platform": "The Verge",
        "author": "pixel_warrior",
        "text": "You are a complete clown and anyone who actually believes this paid marketing fluff is a brainless idiot with no technical literacy."
    },
    {
        "persona": "Adversarial Evasion Hacker",
        "platform": "Reddit r/tech",
        "author": "stealth_anon",
        "text": "Shut up you f\u200bu\u200bc\u200bk\u200bi\u200bn\u200bg 1d10t and a$$h0le, get the f u c k out."
    },
    {
        "persona": "Rhetorical Deflector (Whataboutist)",
        "platform": "Substack Notes",
        "author": "skeptic_pete",
        "text": "Why aren't you talking about the massive corruption in the supply chain oversight committee? What about that? Convenient omission by the mainstream press."
    },
    {
        "persona": "Commercial Spam Bot",
        "platform": "WordPress Blog",
        "author": "crypto_rewards_bot",
        "text": "Make $800 a day working 1 hour from home! Click here https://fastpump.crypto/register discount code MOON2026 dm me on telegram."
    },
    {
        "persona": "Civil Synthesizer",
        "platform": "Hacker News",
        "author": "systems_thinker",
        "text": "While I agree that the initial capital expenditure is high, on the other hand lifecycle battery amortization yields a lower Levelized Cost of Storage (LCOS). A viable middle ground is phased municipal deployment."
    },
    {
        "persona": "Low-Effort Platitude",
        "platform": "Discourse",
        "author": "drive_by_user",
        "text": "lol this will never work in real life."
    },
    {
        "persona": "Technical Code Reviewer",
        "platform": "Dev.to",
        "author": "alx_developer",
        "text": "In section 3, utilizing standard non-blocking asynchronous event loops prevents thread exhaustion under sustained 5,000 req/sec loads. We measured 4.2ms p99 response times."
    },
    {
        "persona": "Legitimate Skeptic",
        "platform": "Ars Technica",
        "author": "grid_architect",
        "text": "I respectfully disagree with the premise that transmission lines can handle this intermittent surge without synchronous condensers. In our regional grid tests, frequency instability occurred above 35% penetration."
    },
    {
        "persona": "Spaced Vulgarity Evasion",
        "platform": "Discourse",
        "author": "edgy_poster",
        "text": "Go k y s right now and shut up."
    }
]

def send_evaluation_request(server_url: str, comment: Dict[str, Any], policy: str, backend: str) -> Dict[str, Any]:
    """Posts a single evaluation request and measures latency."""
    url = f"{server_url}/v1/score"
    payload = json.dumps({
        "text": comment["text"],
        "policy": policy,
        "backend": backend
    }).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            elapsed_ms = (time.perf_counter() - t0) * 1000
            return {
                "success": True,
                "status_code": resp.status,
                "latency_ms": elapsed_ms,
                "result": data,
                "persona": comment["persona"]
            }
    except Exception as e:
        elapsed_ms = (time.perf_counter() - t0) * 1000
        return {
            "success": False,
            "error": str(e),
            "latency_ms": elapsed_ms,
            "persona": comment["persona"]
        }

def run_traffic_simulation(server_url: str, count: int, concurrency: int, policy: str, backend: str):
    print("=" * 75)
    print("🚀 BEYOND LIKES MULTI-PLATFORM DISCOURSE TRAFFIC SIMULATOR")
    print(f"Target Server: {server_url} | Total Comments: {count} | Concurrency: {concurrency}")
    print(f"Community Policy: {policy} | Inference Backend: {backend}")
    print("=" * 75)

    pool = []
    for _ in range(count):
        pool.append(random.choice(SIMULATED_PERSONAS))

    latencies = []
    status_counts = {}
    flagged_toxic = 0
    flagged_spam = 0
    approved_promoted = 0
    success_count = 0
    fail_count = 0

    start_total = time.perf_counter()

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [
            executor.submit(send_evaluation_request, server_url, item, policy, backend)
            for item in pool
        ]
        
        for idx, fut in enumerate(as_completed(futures), 1):
            res = fut.result()
            latencies.append(res["latency_ms"])
            if res["success"]:
                success_count += 1
                data = res["result"]
                st = data.get("status", "UNKNOWN")
                status_counts[st] = status_counts.get(st, 0) + 1
                
                if data.get("flags", {}).get("is_toxic"): flagged_toxic += 1
                if data.get("flags", {}).get("is_spam"): flagged_spam += 1
                if st == "APPROVED_PROMOTED": approved_promoted += 1
            else:
                fail_count += 1

            if idx % 10 == 0 or idx == count:
                print(f"  [Progress] Processed {idx}/{count} requests ({idx/count*100:.0f}%)...")

    duration = time.perf_counter() - start_total
    rps = count / duration if duration > 0 else 0

    latencies.sort()
    p50 = latencies[int(len(latencies) * 0.50)]
    p95 = latencies[int(len(latencies) * 0.95)]
    p99 = latencies[int(len(latencies) * 0.99)]
    avg_lat = sum(latencies) / len(latencies) if latencies else 0

    print("\n" + "=" * 75)
    print("📊 SIMULATION THROUGHPUT & LATENCY PERFORMANCE REPORT")
    print("=" * 75)
    print(f"  Total Evaluated:       {count} comments")
    print(f"  Successful Requests:   {success_count} ({success_count/count*100:.1f}%)")
    print(f"  Failed Requests:       {fail_count}")
    print(f"  Total Duration:        {duration:.2f} seconds")
    print(f"  Throughput:            {rps:.1f} requests/sec (RPS)")
    print(f"  Latency Average:       {avg_lat:.2f} ms")
    print(f"  Latency p50 (Median):  {p50:.2f} ms")
    print(f"  Latency p95:           {p95:.2f} ms")
    print(f"  Latency p99:           {p99:.2f} ms")
    print("-" * 75)
    print("⚖️ AUTOMATED TRIAGE DECISION BREAKDOWN:")
    for st, cnt in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  * {st:<22}: {cnt:>3} ({cnt/count*100:>5.1f}%)")
    print("-" * 75)
    print(f"  Hostile Attacks Intercepted: {flagged_toxic}")
    print(f"  Commercial Spam Intercepted: {flagged_spam}")
    print(f"  High-Substance Promoted:     {approved_promoted}")
    print("=" * 75)

def main():
    parser = argparse.ArgumentParser(description="Beyond Likes Discourse Traffic Simulator")
    parser.add_argument("--server", default=DEFAULT_SERVER_URL, help="Server base URL")
    parser.add_argument("--count", type=int, default=30, help="Number of comments to simulate")
    parser.add_argument("--concurrency", type=int, default=5, help="Concurrent request threads")
    parser.add_argument("--policy", default="newsroom", help="Policy profile to evaluate against")
    parser.add_argument("--backend", default="heuristic", choices=["heuristic", "hybrid", "neural"], help="Inference backend")
    
    args = parser.parse_args()
    run_traffic_simulation(args.server, args.count, args.concurrency, args.policy, args.backend)

if __name__ == "__main__":
    main()
