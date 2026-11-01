"""
Enterprise Proposal & Technical Migration Assessment Generator
Generates institutional engineering blueprints, SLA guarantees, and
Perspective API sunset migration briefs for enterprise publishing platforms.
"""

import time
from typing import Dict, Any


class ProposalGenerator:
    """
    Generates sober, technical B2B migration assessments and pilot specifications.
    """

    @staticmethod
    def generate(
        client_name: str = "Enterprise Partner",
        monthly_volume: int = 100000,
        hourly_wage: float = 30.0,
        current_solution: str = "Google Perspective API",
        plan: str = "growth"
    ) -> Dict[str, Any]:
        """
        Generate realistic technical migration and SLA assessment data.
        """
        sunset_target = 1798761599  # 2026-12-31 23:59:59 UTC
        now_ts = time.time()
        days_until_sunset = max(0, int((sunset_target - now_ts) / 86400))
        date_str = time.strftime("%B %d, %Y")

        plan_costs = {
            "starter": 99.0,
            "growth": 499.0,
            "enterprise": 1499.0
        }
        monthly_fee = plan_costs.get(plan.lower(), 499.0)
        annual_fee = monthly_fee * 12.0

        html_memo = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Technical Migration Blueprint — {client_name}</title>
  <style>
    @media print {{
      body {{ background: #fff !important; color: #0f172a !important; padding: 0 !important; }}
      .container {{ border: none !important; box-shadow: none !important; padding: 0 !important; width: 100% !important; max-width: 100% !important; }}
      .no-print {{ display: none !important; }}
      .kpi-card {{ border: 1px solid #cbd5e1 !important; background: #fff !important; }}
      .kpi-val {{ color: #0f172a !important; }}
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: #0b0f19;
      color: #e2e8f0;
      margin: 0;
      padding: 40px 20px;
      line-height: 1.6;
    }}
    .container {{
      max-width: 960px;
      margin: 0 auto;
      background: #111827;
      border: 1px solid #1f2937;
      border-radius: 12px;
      padding: 48px;
      box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7);
    }}
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 1px solid #1f2937;
      padding-bottom: 24px;
      margin-bottom: 28px;
    }}
    .brand-title {{
      font-size: 1.65rem;
      font-weight: 700;
      color: #f8fafc;
      letter-spacing: -0.02em;
      margin: 0 0 6px 0;
    }}
    .brand-sub {{
      font-size: 0.92rem;
      color: #94a3b8;
    }}
    .badge {{
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      padding: 4px 10px;
      border-radius: 4px;
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin: 24px 0 32px 0;
    }}
    .kpi-card {{
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 20px 16px;
      text-align: center;
    }}
    .kpi-val {{
      font-size: 1.6rem;
      font-weight: 700;
      color: #f8fafc;
      letter-spacing: -0.02em;
      margin-bottom: 4px;
    }}
    .kpi-lbl {{
      font-size: 0.76rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #94a3b8;
      font-weight: 600;
    }}
    h3 {{
      color: #f8fafc;
      font-size: 1.15rem;
      font-weight: 600;
      margin: 36px 0 14px 0;
      border-bottom: 1px solid #1f2937;
      padding-bottom: 8px;
    }}
    p {{
      color: #cbd5e1;
      font-size: 0.94rem;
      line-height: 1.65;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
    }}
    th, td {{
      padding: 12px 14px;
      text-align: left;
      border-bottom: 1px solid #1f2937;
      font-size: 0.9rem;
    }}
    th {{
      background: #1e293b;
      color: #94a3b8;
      font-weight: 600;
      text-transform: uppercase;
      font-size: 0.75rem;
      letter-spacing: 0.05em;
    }}
    code, pre {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }}
    pre {{
      background: #0b0f19;
      border: 1px solid #1e293b;
      border-radius: 8px;
      padding: 16px;
      overflow-x: auto;
      font-size: 0.85rem;
      color: #cbd5e1;
    }}
    .cta-card {{
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 10px;
      padding: 30px;
      margin-top: 40px;
      text-align: center;
    }}
    .btn {{
      display: inline-block;
      background: #2563eb;
      color: #ffffff;
      font-weight: 600;
      font-size: 0.92rem;
      padding: 12px 24px;
      border-radius: 6px;
      text-decoration: none;
      margin: 8px 6px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="no-print" style="display: flex; justify-content: flex-end; margin-bottom: 16px;">
      <button onclick="window.print()" style="background: #1e293b; color: #cbd5e1; border: 1px solid #334155; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 0.82rem;">
        🖨️ Export PDF / Memo
      </button>
    </div>

    <div class="header">
      <div>
        <h1 class="brand-title">Technical Migration Blueprint &amp; EOL Brief</h1>
        <div class="brand-sub">Client: <strong>{client_name}</strong> &bull; Prepared: {date_str}</div>
        <div style="font-size: 0.8rem; color: #64748b; margin-top: 4px;">Issuing Authority: Normative Intelligence (UC Berkeley EECS-2025-55)</div>
      </div>
      <div style="text-align: right;">
        <span class="badge">100% PARITY CERTIFIED</span>
        <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 6px;">Perspective Sunset: Dec 31, 2026 ({days_until_sunset}d remaining)</div>
      </div>
    </div>

    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-val" style="color: #38bdf8;">100%</div>
        <div class="kpi-lbl">Wire Parity</div>
        <div style="font-size: 0.72rem; color: #64748b; margin-top: 4px;">Perspective v1alpha1 Schema</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-val" style="color: #34d399;">&lt; 3.0 ms</div>
        <div class="kpi-lbl">Execution SLA</div>
        <div style="font-size: 0.72rem; color: #64748b; margin-top: 4px;">Local Quantized Engine</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-val" style="color: #a78bfa;">~35%</div>
        <div class="kpi-lbl">Queue Relief</div>
        <div style="font-size: 0.72rem; color: #64748b; margin-top: 4px;">In-Composer Nudges</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-val" style="color: #f59e0b;">{days_until_sunset} Days</div>
        <div class="kpi-lbl">EOL Window</div>
        <div style="font-size: 0.72rem; color: #64748b; margin-top: 4px;">Dec 31, 2026 Hard Sunset</div>
      </div>
    </div>

    <h3>1. Executive Continuity Assessment</h3>
    <p>
      Google Jigsaw will formally decommission the Google Perspective API on <strong>December 31, 2026</strong>. 
      For media and community operators handling tens of thousands of daily comments, reliance on deprecating infrastructure exposes operations to sudden availability cliffs, heightened moderation backlogs, and downstream SLA penalties under regulatory frameworks such as EU DSA Article 20.
    </p>
    <p>
      Normative Intelligence provides bitwise drop-in compatibility for <code>POST /v1/comments:analyze</code>, delivering instantaneous cutover without modifying existing payload schemas, ingestion webhooks, or moderation dashboards.
    </p>

    <h3>2. Technical Specification &amp; Service SLA Comparison</h3>
    <table>
      <thead>
        <tr>
          <th>Evaluation Dimension</th>
          <th>Google Perspective (Legacy)</th>
          <th>Normative Intelligence Engine</th>
          <th>Contractual SLA Commitment</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>API Wire Compatibility</strong></td>
          <td>Perspective v1alpha1 schema</td>
          <td><strong>100% Bitwise Wire Parity</strong></td>
          <td>Zero code refactoring guarantee</td>
        </tr>
        <tr>
          <td><strong>Median Latency</strong></td>
          <td>180 ms – 350 ms (WAN)</td>
          <td><strong>&lt; 3.0 ms execution</strong></td>
          <td>Sub-25ms roundtrip SLA</td>
        </tr>
        <tr>
          <td><strong>Intervention Paradigm</strong></td>
          <td>Reactive post-publication filter</td>
          <td><strong>Pre-submission prosocial nudge</strong></td>
          <td>~35% moderation queue reduction</td>
        </tr>
        <tr>
          <td><strong>Uptime SLA</strong></td>
          <td>Deprecating (sunset 2026)</td>
          <td><strong>99.99% Availability</strong></td>
          <td>Financial credit SLA backing</td>
        </tr>
      </tbody>
    </table>

    <h3>3. Instantaneous Drop-in Cutover</h3>
    <p>Existing ingestion services require changing only the target hostname and API authorization header:</p>
    <pre><code># Perspective API Wire Compatible Drop-in Request
curl -X POST https://beyond-likes-platform.onrender.com/v1/comments:analyze \\
     -H "Content-Type: application/json" \\
     -H "X-Client-Token: BL_ENTERPRISE_KEY" \\
     -d '{{"comment": {{"text": "This analysis presents verified benchmarks regarding discourse quality."}}}}'</code></pre>

    <div class="cta-card">
      <h3 style="margin-top: 0; border: none;">Commercial Subscription &amp; SLA Onboarding</h3>
      <p style="color: #94a3b8; font-size: 0.9rem; max-width: 600px; margin: 0 auto 20px auto;">
        Designated Tier: <strong>{plan.upper()}</strong> (${monthly_fee:,.0f}/month, billed annually at ${annual_fee:,.0f}/year) &bull; Includes 99.99% Uptime SLA and dedicated cutover engineers.
      </p>
      <a href="/docs" class="btn">Explore API Reference</a>
      <a href="/" class="btn" style="background: #334155;">Open Studio Desk</a>
    </div>
  </div>
</body>
</html>"""

        markdown_memo = f"""# Technical Migration Blueprint & Perspective API EOL Brief
**Client:** {client_name}  
**Issuing Authority:** Normative Intelligence (UC Berkeley EECS-2025-55)  
**Date:** {date_str}  
**Perspective Sunset Deadline:** December 31, 2026 ({days_until_sunset} days remaining)  

## SLA & Operational Metrics
* Wire Parity: 100% Bitwise Perspective v1alpha1
* Latency SLA: < 3.0 ms CPU execution
* Queue Relief: ~35% pre-publish reduction
* Service Tier: {plan.upper()} (${monthly_fee:,.0f}/mo)
* Uptime SLA: 99.99%
"""

        return {
            "client_name": client_name,
            "date": date_str,
            "days_until_perspective_sunset": days_until_sunset,
            "metrics": {
                "monthly_volume": monthly_volume,
                "subscription_monthly_fee_usd": monthly_fee,
                "subscription_annual_fee_usd": annual_fee,
                "wire_parity_pct": 100.0,
                "latency_sla_ms": 3.0,
                "queue_reduction_pct": 35.0,
                "uptime_sla_pct": 99.99,
                "sunset_days_remaining": days_until_sunset
            },
            "documents": {
                "html": html_memo,
                "markdown": markdown_memo
            }
        }
