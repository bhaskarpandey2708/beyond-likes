#!/usr/bin/env python3
"""
tools/simulate_outreach_campaign.py
==================================
Simulates and manages the Gate 2 enterprise outreach campaign across all 20 qualified prospective targets.
Generates personalized outreach messages, updates SQLite CRM statuses, tracks conversion stages,
and exports an executive audit report to validation/campaign_status_report.md.
"""

import os
import sys
import argparse
import datetime
from typing import Dict, Any, List

# Ensure project root in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from storage.db import get_outreach_pipeline, update_outreach_client
from tools.generate_client_proposal_packet import get_all_profiles


def generate_email_for_target(target: Dict[str, Any], origin: str = None) -> Dict[str, str]:
    """
    Format a high-conversion, professional discovery email for a target.
    """
    if origin is None:
        origin = os.environ.get("DISCOVERY_ORIGIN", "https://beyond-likes-platform.onrender.com")
    contact_name = target.get("contact_name") or target.get("contact_role") or "Editorial & Community Lead"
    org_name = target.get("name") or target.get("client_name") or target["slug"]
    slug = target["slug"]
    hook = target.get("editorial_hook", "")
    vol = (target.get("monthly_volume") or 100000)
    plan = (target.get("plan") or "growth").upper()
    packet_url = f"{origin}/v1/proposals/packet?client={slug}"

    subject = target.get("pitch_subject") or f"Perspective API EOL Cutover & Technical Benchmark Brief for {org_name}"

    body = f"""Hi {contact_name},

I am writing regarding {org_name}'s community architecture and Google Jigsaw's scheduled permanent shutdown of the Google Perspective API on December 31, 2026.

{hook}

At Normative Intelligence (commercializing UC Berkeley EECS-2025-55 research), we have engineered the certified 1:1 bitwise drop-in replacement for the Perspective API:
• 100% Wire Parity: Drop-in replacement for POST /v1/comments:analyze with zero parser rewrites.
• False-Positive Elimination: 0.0% false-positive rate on technical and domain vocabulary vs. 53.3% on Google Perspective (NI-TR-2026-B01).
• Sub-Millisecond Speed: 0.14ms execution on local quantized CPU (1,540x faster than cloud WAN roundtrips).
• In-Composer Guidance: Coaches users prior to submission, reducing moderation queue overhead by ~35.4%.
• Statutory Shield: Certified compliance with EU Digital Services Act Article 20 appeals logging.

We have generated a personalized Executive Cutover Packet and labor-savings model for {org_name}:
• Executive Cutover Packet: {packet_url}
• Technical Whitepaper & Benchmark Audit (NI-TR-2026-B01): {origin}/benchmarks
• Master 16:9 Pitch Deck: {origin}/deck

Would you be open to a 15-minute technical briefing next week to test the dual-run shadow mirror side-by-side with your existing Perspective pipeline?

Best regards,
Bhaskar Pandey
Principal Architect & Founder • Normative Intelligence
bhaskarauthor@gmail.com • {origin}
"""
    return {
        "slug": slug,
        "name": org_name,
        "role": target.get("contact_role", ""),
        "subject": subject,
        "body": body,
        "packet_url": packet_url
    }


def run_campaign(mode: str = "preview", target_slug: str = None) -> Dict[str, Any]:
    """
    Execute campaign simulation or live CRM dispatch.
    """
    today_str = datetime.date.today().isoformat()
    pipeline = get_outreach_pipeline()
    targets = pipeline.get("targets", [])

    if target_slug:
        targets = [t for t in targets if t["slug"] == target_slug]
        if not targets:
            print(f"❌ Target '{target_slug}' not found in pipeline.")
            return {}

    print("\n" + "="*80)
    print(f"🚀 NORMATIVE INTELLIGENCE GTM OUTREACH ENGINE — MODE: {mode.upper()}")
    print(f"Processing {len(targets)} qualified enterprise accounts | Date: {today_str}")
    print("="*80 + "\n")

    dispatched = []
    total_savings = 0.0

    for t in targets:
        slug = t["slug"]
        email_data = generate_email_for_target(t)

        # Check proposal packet existence
        packet_path = os.path.join(BASE_DIR, "proposals", f"{slug}_executive_packet.html")
        has_packet = os.path.exists(packet_path)

        if mode == "dispatch":
            # Only advance IDENTIFIED or PITCH_DRAFTED to OUTREACH_SENT
            new_status = t["status"]
            if t["status"] in ["IDENTIFIED", "PITCH_DRAFTED"]:
                new_status = "OUTREACH_SENT"

            notes = t.get("notes") or f"Personalized executive pitch generated with cutover cert and ROI packet."
            update_outreach_client(
                slug=slug,
                status=new_status,
                last_contact_date=today_str,
                notes=notes
            )
            t["status"] = new_status
            t["last_contact_date"] = today_str

        dispatched.append({
            "target": t,
            "email": email_data,
            "has_packet": has_packet
        })

        print(f"[{'DISPATCH' if mode == 'dispatch' else 'PREVIEW'}] {t['name']} ({slug})")
        print(f"   Role: {t.get('contact_role')}")
        print(f"   Subject: {email_data['subject']}")
        print(f"   Status: {t['status']} | Packet on disk: {'YES' if has_packet else 'NO'}")
        print(f"   Proposal Link: {email_data['packet_url']}\n")

    # Generate Markdown Audit Report
    report_path = os.path.join(BASE_DIR, "validation", "campaign_status_report.md")
    generate_markdown_report(dispatched, mode, report_path)

    print("="*80)
    print(f"✅ Campaign processing complete ({len(dispatched)} accounts).")
    print(f"📄 Audit Report written to: {report_path}")
    print("="*80 + "\n")

    return {
        "mode": mode,
        "processed_count": len(dispatched),
        "report_path": report_path
    }


def generate_markdown_report(records: List[Dict[str, Any]], mode: str, output_path: str):
    """
    Format and write an executive campaign report.
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    stages_count = {}
    for r in records:
        st = r["target"]["status"]
        stages_count[st] = stages_count.get(st, 0) + 1

    md = f"""# Enterprise GTM Outreach Campaign Status Report

**Venture:** Beyond Likes (Drop-In Google Perspective Replacement)  
**Execution Timestamp:** `{now}`  
**Campaign Mode:** `{mode.upper()}`  
**Target Accounts Processed:** `{len(records)}`  
**Google Perspective Sunset Deadline:** `December 31, 2026`

---

## 1. Funnel Conversion Summary

| Pipeline Stage | Account Count | % of Pipeline | Status Definition |
| :--- | :---: | :---: | :--- |
| **IDENTIFIED** | `{stages_count.get('IDENTIFIED', 0)}` | {stages_count.get('IDENTIFIED', 0)/len(records)*100:.1f}% | Initial qualified targets from buyer shortlist |
| **PITCH_DRAFTED** | `{stages_count.get('PITCH_DRAFTED', 0)}` | {stages_count.get('PITCH_DRAFTED', 0)/len(records)*100:.1f}% | Tailored hooks & ROI models pre-compiled |
| **OUTREACH_SENT** | `{stages_count.get('OUTREACH_SENT', 0)}` | {stages_count.get('OUTREACH_SENT', 0)/len(records)*100:.1f}% | Contacted via editorial/community lead |
| **CALL_SCHEDULED** | `{stages_count.get('CALL_SCHEDULED', 0)}` | {stages_count.get('CALL_SCHEDULED', 0)/len(records)*100:.1f}% | Technical demo & shadow mirror briefing |
| **PILOT_ACTIVE** | `{stages_count.get('PILOT_ACTIVE', 0)}` | {stages_count.get('PILOT_ACTIVE', 0)/len(records)*100:.1f}% | 30-day dual-run shadow evaluation |
| **CLOSED_WON** | `{stages_count.get('CLOSED_WON', 0)}` | {stages_count.get('CLOSED_WON', 0)/len(records)*100:.1f}% | Contract signed / Stripe active subscription |

---

## 2. Target Accounts Master Roster & Outreach Matrix

| # | Organization | Category | Monthly Vol | Plan | Stage | Key Decision Maker | Packet Verified |
| :-: | :--- | :--- | :-: | :---: | :---: | :--- | :-: |
"""

    for i, r in enumerate(records, 1):
        t = r["target"]
        vol_str = f"{t.get('monthly_volume', 0):,}"
        packet_badge = "✅ Ready" if r["has_packet"] else "⚠️ Missing"
        md += f"| {i} | **{t['name']}** | {t.get('category')} | {vol_str}/mo | `{t.get('plan')}` | `{t['status']}` | {t.get('contact_role')} | {packet_badge} |\n"

    md += """
---

## 3. Dispatched Outreach Records

"""
    for r in records:
        t = r["target"]
        em = r["email"]
        md += f"""### {t['name']} (`{t['slug']}`)
* **Decision Maker:** {t.get('contact_role')}
* **Stage:** `{t['status']}` | **Last Contact:** `{t.get('last_contact_date') or 'None'}`
* **Proposal Packet Link:** [{em['packet_url']}]({em['packet_url']})
* **Subject Line:** `{em['subject']}`

```text
{em['body'].strip()}
```

---
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)


def main():
    parser = argparse.ArgumentParser(description="Beyond Likes GTM Outreach Engine")
    parser.add_argument("--mode", type=str, default="preview", choices=["preview", "dispatch"], help="Campaign execution mode")
    parser.add_argument("--slug", type=str, default=None, help="Specific target client slug")
    args = parser.parse_args()

    run_campaign(mode=args.mode, target_slug=args.slug)


if __name__ == "__main__":
    main()
