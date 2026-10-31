#!/usr/bin/env python3
"""
Beyond Likes CLI Tool (Enterprise Suite)
Terminal interface to test, benchmark, simulate traffic, and audit the Discourse Intelligence Engine.
"""
import sys
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from core_engine.evaluator import NormativeEvaluator
from core_engine.rephraser import RephraseAdvisor
from core_engine.perspective_adapter import PerspectiveAdapter
from storage.db import get_system_stats, store_result, get_cached_result
from benchmarks.run_benchmark import run_benchmarks
from benchmarks.adversarial_test import run_adversarial_suite

def print_help():
    print("""
Beyond Likes CLI - Enterprise Discourse Intelligence Engine
===========================================================
Usage:
  python3 cli.py score "<comment>" [--backend heuristic|hybrid|neural]
  python3 cli.py rephrase "<comment>"          # Get constructive rephrase tips
  python3 cli.py perspective "<comment>"       # Test Perspective API drop-in response
  python3 cli.py benchmark                     # Run 5 standard R&D benchmarks
  python3 cli.py adversarial                   # Run 9 adversarial evasion defense tests
  python3 cli.py migrate                       # Run Perspective-to-BeyondLikes audit
  python3 cli.py simulate [--count N]          # Run multi-platform traffic load simulator
  python3 cli.py report [--format md|html|json]# Generate executive audit report
  python3 cli.py stats                         # Show database and audit statistics
  python3 cli.py serve                         # Start live API & playground server
""")

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    cmd = sys.argv[1].lower()
    evaluator = NormativeEvaluator()

    if cmd == "score":
        if len(sys.argv) < 3:
            print("Error: Missing comment text.\nExample: python3 cli.py score 'Your comment here'")
            sys.exit(1)
        
        backend = "heuristic"
        args = sys.argv[2:]
        if "--backend" in args:
            b_idx = args.index("--backend")
            if b_idx + 1 < len(args):
                backend = args[b_idx + 1]
                args = args[:b_idx] + args[b_idx + 2:]
        text = " ".join(args).strip("\"'")

        res = evaluator.evaluate(text, backend=backend)
        rephrase = RephraseAdvisor.generate_suggestions(res, text)
        res["guidance"] = rephrase
        store_result(text, res, client_key="cli_user", latency_ms=res["metrics"]["latency_ms"])

        print("\n" + "="*60)
        print("DISCOURSE EVALUATION RESULT")
        print("="*60)
        print(f"Comment: \"{text}\"")
        print(f"Status:   {res['status']}")
        print(f"Score:    {res['composite_score']}/100")
        print(f"Backend:  {res.get('backend', backend)}")
        print("\nDimensions:")
        for dim, val in res["dimensions"].items():
            bar = "█" * int(val / 5) + "░" * (20 - int(val / 5))
            print(f"  {dim.capitalize():<18}: {val:>5.1f}%  [{bar}]")
        print(f"\nLatency:  {res['metrics']['latency_ms']} ms")
        if "action_routing" in res:
            routing = res["action_routing"]
            print(f"Action:   {routing['primary_action']} ({routing['priority']} priority)")
            print(f"Routing:  {routing['action_summary']}")
        if res.get("guidance", {}).get("needs_revision"):
            print("\n💡 Suggested Constructive Rewrite:")
            print(f"  \"{res['guidance']['suggested_revision']}\"")
            print(f"\nProsocial Nudge: {res['guidance']['prosocial_nudge']}")
        print("="*60 + "\n")

    elif cmd == "rephrase":
        if len(sys.argv) < 3:
            print("Error: Missing comment text.")
            sys.exit(1)
        text = " ".join(sys.argv[2:]).strip("\"'")
        res = evaluator.evaluate(text)
        rephrase = RephraseAdvisor.generate_suggestions(res, text)
        print("\n" + "="*60)
        print(f"Original: \"{text}\"")
        print(f"Suggested: \"{rephrase['suggested_revision']}\"")
        print(f"Unified Diff:\n{rephrase['diff_text']}")
        print(f"Tips:")
        for tip in rephrase["guidance_tips"]:
            print(f"  • {tip}")
        print("="*60 + "\n")

    elif cmd == "perspective":
        if len(sys.argv) < 3:
            print("Error: Missing comment text.")
            sys.exit(1)
        text = " ".join(sys.argv[2:]).strip("\"'")
        adapter = PerspectiveAdapter(evaluator)
        payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}, "INSULT": {}}}
        resp = adapter.handle_request(payload)
        print("\nGoogle Perspective API Output Format:")
        print(json.dumps(resp, indent=2))

    elif cmd == "benchmark":
        success = run_benchmarks()
        sys.exit(0 if success else 1)

    elif cmd == "adversarial":
        success = run_adversarial_suite()
        sys.exit(0 if success else 1)

    elif cmd == "migrate":
        from tools.perspective_migrator import run_migration_audit
        run_migration_audit()

    elif cmd == "simulate":
        from tools.traffic_simulator import run_traffic_simulation
        count = 20
        if "--count" in sys.argv:
            idx = sys.argv.index("--count")
            if idx + 1 < len(sys.argv):
                count = int(sys.argv[idx + 1])
        run_traffic_simulation("http://localhost:8888", count=count, concurrency=4, policy="newsroom", backend="heuristic")

    elif cmd == "report":
        from api.reports import generate_report_data, generate_markdown_report, generate_html_report
        fmt = "md"
        if "--format" in sys.argv:
            idx = sys.argv.index("--format")
            if idx + 1 < len(sys.argv):
                fmt = sys.argv[idx + 1]
        data = generate_report_data()
        if fmt == "html":
            print(generate_html_report(data))
        elif fmt == "json":
            print(json.dumps(data, indent=2))
        else:
            print(generate_markdown_report(data))

    elif cmd == "stats":
        stats = get_system_stats()
        print("\n" + "="*50)
        print("BEYOND LIKES AUDIT & DATABASE STATS")
        print("="*50)
        print(json.dumps(stats, indent=2))
        print("="*50 + "\n")

    elif cmd == "serve":
        from api.server import run_server
        run_server()

    else:
        print(f"Unknown command '{cmd}'.")
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
