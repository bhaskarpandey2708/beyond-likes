#!/usr/bin/env python3
"""
Normative Intelligence — Inclusive System & Parity Verification Suite
Conducts comprehensive end-to-end testing across:
1. Static Surface Availability & Response Headers (/ , /studio, /deck, /benchmarks, /docs)
2. Strict Cache-Control Verification (no-cache headers on all routes)
3. 1:1 Perspective API Wire Drop-in Parity (/v1/comments:analyze)
4. 4D Normative Scoring Engine Integrity (/v1/score)
5. Pre-submission In-Composer Rephrase & Nudge API (/v1/rephrase)
6. Dual-Run Shadow Mirror Endpoint (/v1/shadow-mirror)
7. Production Asset Integrity (PPTX, SVG logos, OpenAPI specs)
"""

import sys
import os
import json
import time
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8888"
PASS_COUNT = 0
FAIL_COUNT = 0

def log_test(name, success, details=""):
    global PASS_COUNT, FAIL_COUNT
    if success:
        PASS_COUNT += 1
        print(f"  ✅ PASS: {name} {details}")
    else:
        FAIL_COUNT += 1
        print(f"  ❌ FAIL: {name} - {details}")

print("=" * 70)
print("🧪 NORMATIVE INTELLIGENCE — INCLUSIVE SYSTEM VERIFICATION SUITE")
print("=" * 70)

# ------------------------------------------------------------------------------
# TEST GROUP 1: Surface Routes & Cache-Control Headers
# ------------------------------------------------------------------------------
print("\n[GROUP 1] Surface Availability & Cache-Control Headers")
surfaces = [
    ("/", "Showcase Landing Home"),
    ("/studio", "Executive Studio Desk"),
    ("/deck", "Auto-Advancing 16:9 Pitch Deck"),
    ("/benchmarks", "Empirical Research Whitepaper"),
    ("/docs", "Developer API Studio"),
    ("/brand", "Brand Identity & Video Hub"),
    ("/v1/health", "System Health Check")
]

for path, label in surfaces:
    url = f"{BASE_URL}{path}"
    try:
        t0 = time.time()
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as res:
            t1 = time.time()
            latency = (t1 - t0) * 1000
            headers = dict(res.headers)
            cache_ctrl = headers.get("Cache-Control", "")
            has_no_cache = "no-cache" in cache_ctrl
            body_len = len(res.read())

            log_test(
                f"{label} ({path})",
                res.status == 200 and has_no_cache and body_len > 0,
                f"[{res.status} OK, {body_len} bytes, {latency:.1f}ms, Cache-Control: {cache_ctrl}]"
            )
    except Exception as e:
        log_test(f"{label} ({path})", False, str(e))

# ------------------------------------------------------------------------------
# TEST GROUP 2: 1:1 Perspective API Wire Parity
# ------------------------------------------------------------------------------
print("\n[GROUP 2] 1:1 Google Perspective Wire Parity (/v1/comments:analyze)")
perspective_payload = {
    "comment": {
        "text": "kill -9 $(pgrep nginx) to release the hung worker socket"
    },
    "requestedAttributes": {
        "TOXICITY": {}
    },
    "languages": ["en"]
}

try:
    url = f"{BASE_URL}/v1/comments:analyze"
    data_bytes = json.dumps(perspective_payload).encode("utf-8")
    req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=5) as res:
        latency = (time.time() - t0) * 1000
        body = json.loads(res.read().decode("utf-8"))
        
        has_attr_scores = "attributeScores" in body
        has_toxicity = "TOXICITY" in body.get("attributeScores", {})
        has_summary_score = "summaryScore" in body.get("attributeScores", {}).get("TOXICITY", {})
        score_val = body.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {}).get("value", 0)

        log_test(
            "Perspective JSON Schema Match",
            has_attr_scores and has_toxicity and has_summary_score,
            f"[attributeScores.TOXICITY value: {score_val}, latency: {latency:.1f}ms]"
        )
except Exception as e:
    log_test("Perspective Wire Parity", False, str(e))

# ------------------------------------------------------------------------------
# TEST GROUP 3: Core 4D Normative Scoring Engine
# ------------------------------------------------------------------------------
print("\n[GROUP 3] Core 4D Normative Scoring Engine (/v1/score)")
score_payload = {
    "text": "According to 2026 data, utility-scale battery storage prices declined 18%, reducing evening peak curtailment.",
    "policy": "newsroom",
    "backend": "heuristic"
}

try:
    url = f"{BASE_URL}/v1/score"
    data_bytes = json.dumps(score_payload).encode("utf-8")
    req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=5) as res:
        latency = (time.time() - t0) * 1000
        body = json.loads(res.read().decode("utf-8"))

        composite = body.get("composite_score", 0)
        dimensions = body.get("dimensions", {})
        has_dimensions = all(k in dimensions for k in ["constructiveness", "civility", "persuasiveness", "relevance"])

        log_test(
            "4D Normative Rubric Evaluation",
            res.status == 200 and composite > 50 and has_dimensions,
            f"[Composite: {composite:.1f}/100, Constructive: {dimensions.get('constructiveness', 0):.1f}%, Civility: {dimensions.get('civility', 0):.1f}%, Latency: {latency:.1f}ms]"
        )
except Exception as e:
    log_test("4D Normative Scoring", False, str(e))

# ------------------------------------------------------------------------------
# TEST GROUP 4: Pre-submission In-Composer Rephrase API
# ------------------------------------------------------------------------------
print("\n[GROUP 4] Pre-submission In-Composer Rephrase API (/v1/rephrase)")
rephrase_payload = {
    "text": "This author is an absolute clown and the article is garbage."
}

try:
    url = f"{BASE_URL}/v1/rephrase"
    data_bytes = json.dumps(rephrase_payload).encode("utf-8")
    req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=5) as res:
        latency = (time.time() - t0) * 1000
        body = json.loads(res.read().decode("utf-8"))

        rephrased = body.get("suggested_revision", "")
        has_rephrase = len(rephrased) > 10

        log_test(
            "Constructive Rephrase & Nudge Generation",
            res.status == 200 and has_rephrase,
            f"[Revision: '{rephrased[:45]}...', Latency: {latency:.1f}ms]"
        )
except Exception as e:
    log_test("In-Composer Rephrase API", False, str(e))

# ------------------------------------------------------------------------------
# TEST GROUP 5: Dual-Run Shadow Mirror
# ------------------------------------------------------------------------------
print("\n[GROUP 5] Dual-Run Shadow Mirror (/v1/shadow-mirror)")
shadow_payload = {
    "text": "I strongly contest your conclusion; Table 4 omits key ablation metrics from the 2024 trial."
}

try:
    url = f"{BASE_URL}/v1/shadow-mirror"
    data_bytes = json.dumps(shadow_payload).encode("utf-8")
    req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=5) as res:
        latency = (time.time() - t0) * 1000
        body = json.loads(res.read().decode("utf-8"))
        comparison = body.get("comparison", {})
        perspective = body.get("perspective", {})
        normative = body.get("beyond_likes", {})

        log_test(
            "Shadow Mirror Dual Evaluation",
            res.status == 200 and "discrepancy_category" in comparison,
            f"[Perspective Toxicity: {perspective.get('toxicity_score')}, Normative Score: {normative.get('composite_score')}, Parity: {comparison.get('discrepancy_category')}, Speed Advantage: {comparison.get('latency_advantage_factor')}]"
        )
except Exception as e:
    log_test("Dual-Run Shadow Mirror", False, str(e))

# ------------------------------------------------------------------------------
# TEST GROUP 6: Asset Integrity
# ------------------------------------------------------------------------------
print("\n[GROUP 6] Critical File & Presentation Asset Integrity")
assets = [
    ("landing/index.html", "Showcase Home HTML"),
    ("dashboard/index.html", "Guided Studio HTML"),
    ("brand/pitch-deck.html", "16:9 Fluid Slide Deck HTML"),
    ("benchmarks/whitepaper.html", "Empirical Whitepaper HTML"),
    ("docs/index.html", "API Reference HTML"),
    ("brand/Normative_Intelligence_Pitch_Deck.pptx", "PowerPoint Presentation Binary"),
    ("brand/Normative_Intelligence_Demo_Walkthrough.mp4", "Broadcast Demo Video 1080p MP4"),
    ("brand/demo_video_poster.jpg", "Demo Video Poster Thumbnail JPEG"),
    ("docs/openapi.json", "OpenAPI JSON Specification"),
    ("docs/openapi.yaml", "OpenAPI YAML Specification")
]

base_dir = "/tmp/beyond-likes-git"
for rel_path, label in assets:
    full_path = os.path.join(base_dir, rel_path)
    exists = os.path.exists(full_path)
    size = os.path.getsize(full_path) if exists else 0
    log_test(f"Asset: {label} ({rel_path})", exists and size > 500, f"[{size:,} bytes]")

print("\n" + "=" * 70)
print(f"📊 TEST SUMMARY: {PASS_COUNT} PASSED, {FAIL_COUNT} FAILED")
print("=" * 70)

if FAIL_COUNT > 0:
    sys.exit(1)
sys.exit(0)
