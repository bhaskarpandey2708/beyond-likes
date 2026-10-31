"""
Beyond Likes Edge-Case & Nuanced Discourse Benchmark Suite
Validates zero low-quality degradation across high-difficulty linguistic edge cases.
Specifically evaluates known failure modes of Google Perspective API:
1. Sensitive Identity False Positives (LGBTQ+, Racial Equality)
2. Rigorous Scientific / Academic Disagreement
3. Clinical / Oncology Medical Terminology
4. Multilingual / Hinglish Counter-Speech
5. Covert Toxic Sealioning & Pseudo-Polite Trolling
6. EU DSA Regulatory Disclosures
7. Obfuscated Adversarial Vulgarity
"""
import os
import sys
import time
from typing import Dict, Any, List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from core_engine.evaluator import NormativeEvaluator
from core_engine.rephraser import RephraseAdvisor

EDGE_CASE_BATTERY = [
    {
        "id": "EDGE-01",
        "category": "Sensitive Identity (LGBTQ+ Non-Discrimination)",
        "text": "I am an openly gay high school educator advocating for comprehensive anti-bullying protections for queer youth.",
        "perspective_legacy_flaw": "Flags 0.74 toxicity due to identity token co-occurrence ('gay', 'queer').",
        "expected_status": ["STANDARD_PUBLISH", "APPROVED_PROMOTED"],
        "min_civility": 85.0,
        "min_constructiveness": 60.0,
        "must_not_flag": ["is_toxic", "is_spam"]
    },
    {
        "id": "EDGE-02",
        "category": "Racial Equality Advocacy & Legislative Reform",
        "text": "Black lives matter, and systemic disparities in mandatory minimum sentencing require empirical reform through judicial oversight.",
        "perspective_legacy_flaw": "Flags 0.68 identity attack on racial justice discourse.",
        "expected_status": ["STANDARD_PUBLISH", "APPROVED_PROMOTED"],
        "min_civility": 85.0,
        "min_constructiveness": 50.0,
        "must_not_flag": ["is_toxic"]
    },
    {
        "id": "EDGE-03",
        "category": "Clinical Oncology & Medical Pathology",
        "text": "Pathology confirmed invasive ductal carcinoma with axillary lymph node metastases requiring adjuvant chemotherapy and surgical resection.",
        "perspective_legacy_flaw": "Flags anatomical/pathological clinical terms as vulgar or graphic.",
        "expected_status": ["STANDARD_PUBLISH", "APPROVED_PROMOTED"],
        "min_civility": 85.0,
        "min_relevance": 70.0,
        "must_not_flag": ["is_toxic"]
    },
    {
        "id": "EDGE-04",
        "category": "Sharp Academic / Peer-Review Disagreement",
        "text": "I strongly disagree with the authors' methodology. The sample size is underpowered, and without double-blind controls, the statistical significance claims are unfounded.",
        "perspective_legacy_flaw": "Classifies rigorous epistemic critique as insulting or toxic attack.",
        "expected_status": ["STANDARD_PUBLISH", "APPROVED_PROMOTED"],
        "min_civility": 80.0,
        "min_constructiveness": 70.0,
        "must_not_flag": ["is_toxic"]
    },
    {
        "id": "EDGE-05",
        "category": "Hinglish Code-Mixed Constructive Pushback",
        "text": "Bhai ye bilkul galat interpretation hai. Pehle official documentation aur peer-reviewed benchmark dekho phir claim karo.",
        "perspective_legacy_flaw": "Fails to parse romanized Indic dialects, degrading to random baseline.",
        "expected_status": ["STANDARD_PUBLISH", "APPROVED_PROMOTED"],
        "min_civility": 80.0,
        "min_constructiveness": 45.0,
        "must_not_flag": ["is_toxic"]
    },
    {
        "id": "EDGE-06",
        "category": "Pseudo-Polite Passive-Aggressive Sealioning",
        "text": "With all due respect and utmost polite deference, can anyone with an elementary school IQ explain why your garbage argument isn't laughable?",
        "perspective_legacy_flaw": "Foolish reliance on superficial pleasantries ('respect', 'deference') suppresses toxicity score.",
        "expected_status": ["FLAGGED_UNCIVIL", "NEEDS_IMPROVEMENT"],
        "max_civility": 45.0,
        "must_flag": "is_toxic"
    },
    {
        "id": "EDGE-07",
        "category": "Sarcastic Deflection & Whataboutism",
        "text": "Oh sure, let's just pretend the budget deficit is magic fairy dust. What about the billions sent overseas? Utterly laughable logic.",
        "perspective_legacy_flaw": "Treats deflection as valid civic contribution.",
        "expected_status": ["NEEDS_IMPROVEMENT"],
        "max_constructiveness": 50.0,
        "max_persuasiveness": 50.0
    },
    {
        "id": "EDGE-08",
        "category": "EU Digital Services Act (DSA) Legal Disclosure",
        "text": "In accordance with Article 16 of EU Regulation 2022/2065, this notification identifies illegal hate speech violating national criminal codes.",
        "perspective_legacy_flaw": "Flags statutory quote of penal terminology as hate speech violation.",
        "expected_status": ["STANDARD_PUBLISH", "APPROVED_PROMOTED"],
        "min_civility": 85.0,
        "min_constructiveness": 60.0,
        "must_not_flag": ["is_toxic"]
    },
    {
        "id": "EDGE-09",
        "category": "Zero-Width Obfuscated Harassment",
        "text": "Shut up you f\u200bu\u200bc\u200bk\u200bi\u200bn\u200bg worthless idiot.",
        "perspective_legacy_flaw": "Zero-width unicode spaces completely bypass standard substring filters.",
        "expected_status": ["FLAGGED_UNCIVIL"],
        "max_civility": 35.0,
        "must_flag": "is_toxic"
    },
    {
        "id": "EDGE-10",
        "category": "Leetspeak / Symbol Evasion Trolling",
        "text": "You are a total 1d10t and a d1sgust1ng piece of tr4sh.",
        "perspective_legacy_flaw": "Bypasses keyword lists via character substitution.",
        "expected_status": ["FLAGGED_UNCIVIL"],
        "max_civility": 35.0,
        "must_flag": "is_toxic"
    }
]

def run_edge_case_battery() -> bool:
    print("=" * 80)
    print("🔬 BEYOND LIKES: NUANCED DISCOURSE & EDGE-CASE QUALITY BENCHMARK")
    print("Eliminates Perspective API False Positives & Stealth Toxic Evasion")
    print("=" * 80)

    evaluator = NormativeEvaluator()
    passed = 0
    total = len(EDGE_CASE_BATTERY)
    latencies = []
    start_total = time.perf_counter()

    for case in EDGE_CASE_BATTERY:
        cid = case["id"]
        cat = case["category"]
        text = case["text"]

        t0 = time.perf_counter()
        res = evaluator.evaluate(text)
        lat = (time.perf_counter() - t0) * 1000.0
        latencies.append(lat)

        status = res["status"]
        civ = res["dimensions"]["civility"]
        const = res["dimensions"]["constructiveness"]
        pers = res["dimensions"]["persuasiveness"]
        rel = res["dimensions"]["relevance"]
        flags = res.get("flags", {})

        is_pass = True
        reasons = []

        # Validate status expectation
        if "expected_status" in case and status not in case["expected_status"]:
            is_pass = False
            reasons.append(f"Status '{status}' not in expected {case['expected_status']}")

        # Validate minimum thresholds
        if "min_civility" in case and civ < case["min_civility"]:
            is_pass = False
            reasons.append(f"Civility {civ} < min {case['min_civility']}")
        if "min_constructiveness" in case and const < case["min_constructiveness"]:
            is_pass = False
            reasons.append(f"Constructiveness {const} < min {case['min_constructiveness']}")
        if "min_relevance" in case and rel < case["min_relevance"]:
            is_pass = False
            reasons.append(f"Relevance {rel} < min {case['min_relevance']}")

        # Validate maximum thresholds
        if "max_civility" in case and civ > case["max_civility"]:
            is_pass = False
            reasons.append(f"Civility {civ} > max {case['max_civility']}")
        if "max_constructiveness" in case and const > case["max_constructiveness"]:
            is_pass = False
            reasons.append(f"Constructiveness {const} > max {case['max_constructiveness']}")
        if "max_persuasiveness" in case and pers > case["max_persuasiveness"]:
            is_pass = False
            reasons.append(f"Persuasiveness {pers} > max {case['max_persuasiveness']}")

        # Validate safety flag assertions
        if "must_not_flag" in case:
            for flag_name in case["must_not_flag"]:
                if flags.get(flag_name, False):
                    is_pass = False
                    reasons.append(f"Unexpected flag '{flag_name}' was True (False-Positive!)")

        if "must_flag" in case:
            if not flags.get(case["must_flag"], False):
                is_pass = False
                reasons.append(f"Expected flag '{case['must_flag']}' was False (False-Negative!)")

        if is_pass:
            passed += 1
            mark = "✅ PASS"
            detail = f"Status: {status} | Civ: {civ} | Const: {const} | Latency: {lat:.2f}ms"
        else:
            mark = "❌ FAIL"
            detail = f"Status: {status} | {' & '.join(reasons)}"

        print(f"\n[{mark}] {cid} : {cat}")
        print(f"       Legacy Perspective Flaw: {case['perspective_legacy_flaw']}")
        print(f"       Result: {detail}")

    total_time = (time.perf_counter() - start_total) * 1000.0
    avg_latency = sum(latencies) / len(latencies) if latencies else 0.0

    print("\n" + "=" * 80)
    print(f"🎯 EDGE-CASE BENCHMARK SUMMARY: {passed}/{total} Passed ({passed/total*100:.1f}%)")
    print(f"⚡ Total Runtime: {total_time:.2f}ms | Average Latency: {avg_latency:.2f}ms per query")
    print("=" * 80 + "\n")

    return passed == total

if __name__ == "__main__":
    success = run_edge_case_battery()
    sys.exit(0 if success else 1)
