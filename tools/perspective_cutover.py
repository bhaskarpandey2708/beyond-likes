#!/usr/bin/env python3
"""
Enterprise Perspective Cutover CLI Utility
Automates cutover validation, schema conformance verification, and certificate generation
for engineering and compliance teams ahead of the December 31, 2026 Perspective sunset.
"""

import sys
import os
import argparse
import json
import time

# Ensure project root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core_engine.cutover_cert import CutoverCertificationEngine

def main():
    parser = argparse.ArgumentParser(
        description="Beyond Likes Google Perspective Cutover Readiness CLI"
    )
    parser.add_argument(
        "--org",
        default="Enterprise Publishing Partner",
        help="Organization or media partner name for certificate issuance"
    )
    parser.add_argument(
        "--format",
        choices=["json", "html", "summary"],
        default="summary",
        help="Output format (summary, json, html)"
    )
    parser.add_argument(
        "--output",
        help="Optional file path to save certificate output"
    )

    args = parser.parse_args()

    print("\n" + "="*70)
    print("🔍 BEYOND LIKES: GOOGLE PERSPECTIVE SUNSET CUTOVER AUDIT")
    print(f"Target Organization: {args.org}")
    print(f"Mandatory Sunset Deadline: December 31, 2026")
    print("="*70 + "\n")

    t0 = time.time()
    cert = CutoverCertificationEngine.generate_certificate(organization_name=args.org)
    duration = time.time() - t0

    if args.format == "summary":
        print(f"📋 Certificate ID:   {cert['certificate_id']}")
        print(f"📅 Issue Date:       {cert['issue_date']}")
        print(f"🛡️ Overall Status:    {cert['overall_status']}")
        print(f"⚡ Average Latency:  {cert['verification_summary']['average_latency_ms']} ms")
        print(f"⏱️ Audit Duration:   {duration:.2f}s\n")
        print("BATTERY CHECKS:")
        for c in cert["checks"]:
            symbol = "✅" if c["status"] == "PASS" else "❌"
            print(f"  {symbol} [{c['check_id']}] {c['name']} ({c['latency_ms']}ms)")
            print(f"     Details: {c['details']}")

        print("\n" + "="*70)
        print(f"SHA-256 FINGERPRINT: {cert['cryptographic_fingerprint_sha256']}")
        print("="*70 + "\n")

    elif args.format == "json":
        json_str = json.dumps(cert, indent=2)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(json_str)
            print(f"✅ Certificate saved to {args.output}")
        else:
            print(json_str)

    elif args.format == "html":
        html_str = CutoverCertificationEngine.generate_html_certificate(cert)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(html_str)
            print(f"✅ Printable HTML Certificate saved to {args.output}")
        else:
            print(html_str)

    # Return 0 on PASS, 1 on remediation required
    sys.exit(0 if cert["overall_status"] == "CERTIFIED_CUTOVER_READY" else 1)

if __name__ == "__main__":
    main()
