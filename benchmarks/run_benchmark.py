"""
R&D Evaluation Benchmark Runner
Tests accuracy, discrimination, and latency against curated comment archetypes.
"""
import os
import sys
import json
import time

# Add parent directory to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from core_engine.evaluator import NormativeEvaluator
from core_engine.rephraser import RephraseAdvisor

def run_benchmarks():
    dataset_path = os.path.join(BASE_DIR, "benchmarks", "test_dataset.json")
    with open(dataset_path, "r") as f:
        tests = json.load(f)

    evaluator = NormativeEvaluator()
    passed = 0
    total = len(tests)
    latencies = []

    print("\n" + "="*75)
    print("BEYOND LIKES DISCOURSE ENGINE - R&D BENCHMARK SUITE")
    print("="*75)

    for case in tests:
        cid = case["id"]
        ctype = case["type"]
        text = case["text"]
        
        t0 = time.perf_counter()
        res = evaluator.evaluate(text)
        t_ms = (time.perf_counter() - t0) * 1000.0
        latencies.append(t_ms)

        rephrase = RephraseAdvisor.generate_suggestions(res, text)

        # Check conditions
        ok = True
        status = res["status"]
        if "expected_status" in case and status != case["expected_status"]:
            ok = False

        if ok:
            passed += 1
            mark = "✅ PASS"
        else:
            mark = "❌ FAIL"

        print(f"\n[{cid}] {ctype.upper()}: {mark}")
        print(f"  Comment: \"{text[:60]}...\"")
        print(f"  Composite: {res['composite_score']}/100 | Status: {status} | Latency: {t_ms:.2f}ms")
        print(f"  Dimensions: Const={res['dimensions']['constructiveness']} | Civ={res['dimensions']['civility']} | Pers={res['dimensions']['persuasiveness']}")
        if rephrase["needs_revision"]:
            print(f"  💡 Suggestion: \"{rephrase['suggested_revision'][:70]}...\"")

    avg_lat = sum(latencies) / len(latencies) if latencies else 0.0
    print("\n" + "="*75)
    print(f"BENCHMARK SUMMARY: {passed}/{total} Passed ({passed/total*100:.1f}%) | Avg Latency: {avg_lat:.2f}ms")
    print("="*75 + "\n")

    return passed == total

if __name__ == "__main__":
    success = run_benchmarks()
    sys.exit(0 if success else 1)
