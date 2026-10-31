"""
Adversarial & Evasion Robustness Benchmark Suite
Tests Beyond Likes against zero-width unicode injection, leetspeak obfuscation,
spaced-out profanity, sarcastic deflections, and payload stress.
"""
import os
import sys
import time
from typing import Dict, Any, List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from core_engine.evaluator import NormativeEvaluator

ADVERSARIAL_CASES = [
    {
        "id": "ADV-01",
        "category": "Zero-Width Space Injection",
        "text": "You are a f\u200bu\u200bc\u200bk\u200bi\u200bn\u200bg moron and a complete c\u200bl\u200bo\u200bw\u200bn.",
        "expected_flag": "FLAGGED_UNCIVIL",
        "max_civility": 40.0,
        "description": "Unicode U+200B zero-width spaces placed between characters to defeat regex."
    },
    {
        "id": "ADV-02",
        "category": "Soft Hyphen Injection",
        "text": "Shut up you b\u00adi\u00adt\u00adc\u00adh and g\u00adt\u00adf\u00ado.",
        "expected_flag": "FLAGGED_UNCIVIL",
        "max_civility": 40.0,
        "description": "Unicode U+00AD invisible soft hyphen inserted into vulgarity."
    },
    {
        "id": "ADV-03",
        "category": "Leetspeak / Number Substitution",
        "text": "You are an 1d10t and a sh1t a$$h0le.",
        "expected_flag": "FLAGGED_UNCIVIL",
        "max_civility": 40.0,
        "description": "Numeric and symbol replacements (1->i, 0->o, $$->ss)."
    },
    {
        "id": "ADV-04",
        "category": "Spaced-Out Profanity Evasion",
        "text": "Go k y s right now and get the f u c k out.",
        "expected_flag": "FLAGGED_UNCIVIL",
        "max_civility": 40.0,
        "description": "Whitespace separated characters designed to bypass single token lookups."
    },
    {
        "id": "ADV-05",
        "category": "Unicode Homoglyph / Accent Substitution",
        "text": "You are a stúpid ídïöt with no brain.",
        "expected_flag": "FLAGGED_UNCIVIL",
        "max_civility": 40.0,
        "description": "Latin accented characters used in place of standard ASCII vowels."
    },
    {
        "id": "ADV-06",
        "category": "Sarcastic Whataboutism Deflection",
        "text": "Why aren't you talking about the massive corruption in the CEO's office? What about that? Convenient omission.",
        "expected_flag": "NEEDS_IMPROVEMENT",
        "max_civility": 85.0, # Not explicit harassment, but penalized for rhetorical deflection
        "description": "Classic rhetorical evasion deflecting accountability without constructive evidence."
    },
    {
        "id": "ADV-07",
        "category": "Legitimate Technical Terminology (False Positive Resistance)",
        "text": "The memory allocation failure killed the master process thread, which terminated gracefully.",
        "expected_flag": "STANDARD_PUBLISH",
        "min_civility": 80.0,
        "description": "Words like 'killed', 'terminated' used in computer science context must NOT trigger hostility."
    },
    {
        "id": "ADV-08",
        "category": "Deep Epistemic Synthesis (Prosocial Target)",
        "text": "According to the 2026 IEEE survey, latency dropped by 24.3% when utilizing edge inference. Furthermore, synthesizing this with caching achieves sub-5ms SLA.",
        "expected_flag": "APPROVED_PROMOTED",
        "min_civility": 85.0,
        "description": "Model constructive contribution with empirical citation and synthesis."
    },
    {
        "id": "ADV-09",
        "category": "High-Volume Payload Stress",
        "text": "Standard discourse analysis. " * 500, # 1,500 words
        "expected_flag": "STANDARD_PUBLISH",
        "min_civility": 80.0,
        "description": "Stress payload to verify no regex ReDoS or memory blowup occurs."
    }
]

def run_adversarial_suite():
    print("=" * 75)
    print("🛡️ BEYOND LIKES: ADVERSARIAL & EVASION ROBUSTNESS TEST SUITE")
    print("=" * 75)
    
    evaluator = NormativeEvaluator()
    passed = 0
    total = len(ADVERSARIAL_CASES)
    start_all = time.perf_counter()
    
    for case in ADVERSARIAL_CASES:
        t0 = time.perf_counter()
        res = evaluator.evaluate(case["text"])
        lat = (time.perf_counter() - t0) * 1000
        
        status = res["status"]
        civ = res["dimensions"]["civility"]
        
        # Verify conditions
        is_pass = True
        reason = []
        
        if "max_civility" in case and civ > case["max_civility"]:
            is_pass = False
            reason.append(f"Civility {civ} exceeded max threshold {case['max_civility']}")
        if "min_civility" in case and civ < case["min_civility"]:
            is_pass = False
            reason.append(f"Civility {civ} below min threshold {case['min_civility']}")
            
        if case["expected_flag"] == "FLAGGED_UNCIVIL" and status != "FLAGGED_UNCIVIL":
            is_pass = False
            reason.append(f"Expected status FLAGGED_UNCIVIL, got {status}")
            
        if is_pass:
            passed += 1
            mark = "✅ PASS"
            detail = f"Status: {status} | Civ: {civ} | Latency: {lat:.2f}ms"
        else:
            mark = "❌ FAIL"
            detail = f"Status: {status} | Civ: {civ} | {' & '.join(reason)}"
            
        print(f"[{mark}] {case['id']} - {case['category']}:")
        print(f"       Details: {detail}")
        
    duration = (time.perf_counter() - start_all) * 1000
    print("=" * 75)
    print(f"SUMMARY: {passed}/{total} tests passed ({passed/total*100:.1f}%) in {duration:.2f}ms")
    print("=" * 75)
    return passed == total

if __name__ == "__main__":
    success = run_adversarial_suite()
    sys.exit(0 if success else 1)
