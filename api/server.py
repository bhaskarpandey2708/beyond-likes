"""
Production-Grade Zero-Dependency REST API & Interactive Dashboard Server
Normative Intelligence Platform (Port 8888)
"""
import os
import sys
import json
import time
import queue
import urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from config.settings import HOST, PORT, API_KEYS
from core_engine.rubric import POLICY_PROFILES, get_all_policies
from core_engine.evaluator import NormativeEvaluator
from core_engine.rephraser import RephraseAdvisor
from core_engine.perspective_adapter import PerspectiveAdapter
from core_engine.shadow_mirror import ShadowMirrorEngine
from core_engine.ensemble import EnsembleRouter
from core_engine.compliance import ComplianceReporter
from api.exporter import AuditExporter
from api.appeals import AppealsEngine
from economics.token_calculator import simulate_economics
from storage.db import (
    store_result, get_cached_result, get_recent_evaluations, get_system_stats,
    save_custom_policy, get_custom_policies, delete_custom_policy,
    get_shadow_stats, get_recent_shadow_logs,
    save_webhook_subscription, get_webhook_subscriptions, delete_webhook_subscription,
    get_recent_webhook_deliveries, get_appeals,
    create_tenant, get_tenants, get_tenant_by_id, create_tenant_api_key, get_tenant_keys, delete_tenant_api_key,
    get_replay_runs, get_outreach_pipeline, update_outreach_client
)
from api.auth import verify_api_key, record_api_call
from api.replay import CorpusReplayEngine
from api.metrics import telemetry
from core_engine.cutover_cert import CutoverCertificationEngine
from api.webhooks import process_discourse_webhook, process_wordpress_webhook
from api.reports import generate_report_data, generate_markdown_report, generate_html_report
from api.analytics import get_timeseries_analytics
from api.events import broadcaster
from api.dispatcher import dispatcher
from core_engine.thread_evaluator import ThreadEvaluator
from api.billing import billing_engine
from core_engine.proposal_generator import ProposalGenerator

evaluator = NormativeEvaluator()
perspective_adapter = PerspectiveAdapter(evaluator)
thread_evaluator = ThreadEvaluator(evaluator)
shadow_mirror_engine = ShadowMirrorEngine(evaluator)
ensemble_router = EnsembleRouter(evaluator)

# Simulated live incoming comments pool for Mission Control
LIVE_STREAM_POOL = [
    {"source": "Ars Technica", "author": "dev_alex", "text": "According to IEEE 2026 data, utility solar prices declined 18% in western states."},
    {"source": "The Verge", "author": "pixel_fan", "text": "You are a complete clown and anyone buying this phone is a brainless idiot."},
    {"source": "Dev.to", "author": "sarah_codes", "text": "While I appreciate the post, using raw regex for HTML parsing creates security vulnerabilities."},
    {"source": "Linus Tech Tips", "author": "rig_builder", "text": "lol this gpu is pure garbage."},
    {"source": "Hacker News", "author": "pg_fan", "text": "The paper demonstrates that dual feedback raises constructive engagement by 0.176 over peer popularity alone."},
    {"source": "Reddit r/tech", "author": "crypto_king", "text": "Make $500 a day click here https://scamtoken.io/pump discount code MOON"},
    {"source": "Substack", "author": "economic_analyst", "text": "Why aren't you mentioning the mining labor in Chile? What about that?"}
]

class NormativeIntelligenceAPIHandler(BaseHTTPRequestHandler):

    def _send_json(self, status_code: int, data: dict):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, x-api-key")
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, status_code: int, text: str, content_type: str = "text/plain; charset=utf-8"):
        body = text.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, x-api-key")
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, file_path: str, content_type: str, attachment_name: str = None):
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self.send_header("Access-Control-Allow-Origin", "*")
            if attachment_name:
                self.send_header("Content-Disposition", f'attachment; filename="{attachment_name}"')
            self.end_headers()
            self.wfile.write(content)
        else:
            self._send_json(404, {"error": f"File not found: {os.path.basename(file_path)}"})

    def _read_body_json(self) -> dict:
        content_len = int(self.headers.get("Content-Length", 0))
        if content_len == 0:
            return {}
        try:
            raw = self.rfile.read(content_len).decode("utf-8", errors="replace")
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
            elif isinstance(parsed, list):
                return {"_list": parsed, "items": parsed, "comments": parsed}
            return {}
        except Exception:
            return {}

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, x-api-key")
        self.end_headers()

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # 1. Root & Commercial Showcase
        if path in ["/", "/index.html", "/landing", "/landing/index.html", "/showcase"]:
            self._send_file(os.path.join(BASE_DIR, "landing", "index.html"), "text/html; charset=utf-8")
            return

        # 1a. Enterprise Studio Desk Workstation
        elif path in ["/studio", "/studio/", "/dashboard", "/dashboard/", "/desk", "/app", "/dashboard/index.html"]:
            self._send_file(os.path.join(BASE_DIR, "dashboard", "index.html"), "text/html; charset=utf-8")
            return

        # 1b. Serve In-Composer Widget Demo Page
        elif path == "/widget/demo":
            self._send_file(os.path.join(BASE_DIR, "distribution", "widget", "demo.html"), "text/html; charset=utf-8")
            return

        # 1c. Serve Embeddable Widget JavaScript
        elif path == "/widget/beyond-likes.js":
            self._send_file(os.path.join(BASE_DIR, "distribution", "widget", "beyond-likes.js"), "application/javascript; charset=utf-8")
            return

        # 1d. Serve Interactive API Docs
        elif path in ["/docs", "/docs/", "/docs/index.html"]:
            self._send_file(os.path.join(BASE_DIR, "docs", "index.html"), "text/html; charset=utf-8")
            return

        # 1e. Serve OpenAPI Specification (YAML and JSON)
        elif path in ["/docs/openapi.yaml", "/docs/openapi.yml"]:
            self._send_file(os.path.join(BASE_DIR, "docs", "openapi.yaml"), "text/yaml; charset=utf-8")
            return

        elif path == "/docs/openapi.json":
            self._send_file(os.path.join(BASE_DIR, "docs", "openapi.json"), "application/json; charset=utf-8")
            return

        # 1f. Serve Interactive Startup Pitch Deck
        elif path in ["/deck", "/deck/", "/pitch", "/pitch/", "/pitch-deck", "/slides"]:
            self._send_file(os.path.join(BASE_DIR, "brand", "pitch-deck.html"), "text/html; charset=utf-8")
            return

        # 1g. Serve Native PowerPoint Pitch Deck Download
        elif path in ["/deck/download", "/pitch/download", "/brand/Normative_Intelligence_Pitch_Deck.pptx", "/brand/deck.pptx"]:
            self._send_file(os.path.join(BASE_DIR, "brand", "Normative_Intelligence_Pitch_Deck.pptx"),
                            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            "Normative_Intelligence_Pitch_Deck.pptx")
            return

        # 1h. Serve Brand Identity & Visual Asset Kit
        elif path in ["/brand", "/brand/", "/brand-kit", "/brand/index.html"]:
            self._send_file(os.path.join(BASE_DIR, "brand", "index.html"), "text/html; charset=utf-8")
            return

        # 1i. Serve Vector Logos
        elif path == "/brand/logo.svg":
            self._send_file(os.path.join(BASE_DIR, "brand", "logo.svg"), "image/svg+xml; charset=utf-8")
            return

        elif path == "/brand/logo-horizontal.svg":
            self._send_file(os.path.join(BASE_DIR, "brand", "logo-horizontal.svg"), "image/svg+xml; charset=utf-8")
            return

        # 1j. Serve Empirical Benchmark Report & Technical Whitepaper
        elif path in ["/benchmarks", "/benchmarks/", "/whitepaper", "/whitepaper/", "/whitepaper.html"]:
            self._send_file(os.path.join(BASE_DIR, "benchmarks", "whitepaper.html"), "text/html; charset=utf-8")
            return

        # 1k. Serve Raw Empirical Benchmark Results (JSON)
        elif path in ["/v1/benchmarks/results", "/benchmarks/results.json"]:
            self._send_file(os.path.join(BASE_DIR, "benchmarks", "benchmark_results.json"), "application/json; charset=utf-8")
            return

        # 1l. Serve Demo Walkthrough Video & Poster
        elif path in ["/brand/Normative_Intelligence_Demo_Walkthrough.mp4", "/demo-video", "/video", "/walkthrough"]:
            self._send_file(os.path.join(BASE_DIR, "brand", "Normative_Intelligence_Demo_Walkthrough.mp4"), "video/mp4")
            return

        elif path in ["/brand/demo_video_poster.jpg", "/demo-poster"]:
            self._send_file(os.path.join(BASE_DIR, "brand", "demo_video_poster.jpg"), "image/jpeg")
            return

        # 2. Health check
        elif path == "/v1/health":
            self._send_json(200, {
                "status": "HEALTHY",
                "service": "Normative Intelligence Platform",
                "version": "2.8.0-enterprise-edge",
                "timestamp": time.time(),
                "endpoints": [
                    "GET /landing",
                    "GET /v1/metrics",
                    "GET /v1/cutover/certificate",
                    "GET /v1/billing/plans",
                    "POST /v1/billing/checkout",
                    "POST /v1/billing/webhook",
                    "GET /v1/billing/status",
                    "POST /v1/billing/simulate-upgrade",
                    "POST /v1/score",
                    "POST /v1/rephrase",
                    "POST /v1/batch-score",
                    "POST /v1/thread:analyze",
                    "POST /v1/ensemble:analyze",
                    "POST /v1/comments:analyze (Perspective Drop-in)",
                    "POST /v1/shadow-mirror",
                    "GET /v1/shadow-mirror/stats",
                    "GET /v1/shadow-mirror/logs",
                    "POST /v1/shadow-mirror/replay",
                    "GET /v1/shadow-mirror/replay/runs",
                    "GET /v1/shadow-mirror/replay/sample-corpus",
                    "GET /v1/tenants",
                    "POST /v1/tenants",
                    "GET /v1/tenants/keys",
                    "POST /v1/tenants/keys",
                    "DELETE /v1/tenants/keys",
                    "POST /v1/proposals/generate",
                    "GET /v1/proposals/view",
                    "GET /v1/proposals/packet",
                    "GET /v1/proposals/packets",
                    "GET /v1/outreach/pipeline",
                    "POST /v1/outreach/status",
                    "GET /v1/social/campaign",
                    "POST /v1/social/status",
                    "GET /v1/downloads",
                    "GET /v1/compliance/dsa-report",
                    "GET /v1/audit/export",
                    "POST /v1/appeals:submit",
                    "GET /v1/appeals",
                    "POST /v1/appeals:resolve",
                    "POST /v1/webhooks/discourse",
                    "POST /v1/webhooks/wordpress",
                    "POST /v1/webhooks/subscriptions",
                    "GET /v1/webhooks/subscriptions",
                    "DELETE /v1/webhooks/subscriptions",
                    "GET /v1/webhooks/deliveries",
                    "POST /v1/webhooks/test",
                    "GET /v1/live-feed-sample",
                    "GET /v1/roi-calculator",
                    "GET /v1/policies",
                    "GET /v1/audit-logs",
                    "GET /v1/stats",
                    "GET /v1/economics",
                    "GET /v1/reports",
                    "GET /v1/analytics/trends",
                    "GET /v1/stream",
                    "GET /docs",
                    "GET /docs/openapi.yaml",
                    "GET /widget/demo",
                    "GET /widget/beyond-likes.js"
                ]
            })

        # 2b. Shadow Mirror Cutover Stats
        elif path == "/v1/shadow-mirror/stats":
            self._send_json(200, get_shadow_stats())

        # 2c. Shadow Mirror Discrepancy Logs
        elif path == "/v1/shadow-mirror/logs":
            limit = int(query.get("limit", [50])[0])
            self._send_json(200, {"logs": get_recent_shadow_logs(limit=limit)})

        # 2c-1. Shadow Mirror Replay Benchmark Runs
        elif path == "/v1/shadow-mirror/replay/runs":
            limit = int(query.get("limit", [20])[0])
            runs = CorpusReplayEngine.get_past_runs(limit=limit)
            self._send_json(200, {"runs": runs, "total": len(runs)})

        # 2c-2. Shadow Mirror Sample Benchmark Corpus
        elif path == "/v1/shadow-mirror/replay/sample-corpus":
            gold = CorpusReplayEngine.generate_gold_corpus()
            self._send_json(200, {"corpus": gold, "total": len(gold)})

        # 2c-3. Enterprise Workspace Tenants
        elif path == "/v1/tenants":
            tenants = get_tenants()
            self._send_json(200, {"tenants": tenants, "total": len(tenants)})

        # 2c-4. Tenant Scoped API Keys
        elif path == "/v1/tenants/keys":
            tid = query.get("tenant_id", [""])[0]
            if not tid:
                self._send_json(400, {"error": "Missing 'tenant_id' query parameter."})
                return
            keys = get_tenant_keys(tid)
            self._send_json(200, {"tenant_id": tid, "keys": keys, "total": len(keys)})

        # 2d. Outbound Webhook Subscriptions List
        elif path == "/v1/webhooks/subscriptions":
            self._send_json(200, {"subscriptions": get_webhook_subscriptions(active_only=False)})

        # 2e. Outbound Webhook Delivery History Logs
        elif path == "/v1/webhooks/deliveries":
            limit = int(query.get("limit", [50])[0])
            self._send_json(200, {"deliveries": get_recent_webhook_deliveries(limit=limit)})

        # 2e-1. OpenMetrics / Prometheus Telemetry Scrape Endpoint
        elif path == "/v1/metrics":
            prom_text = telemetry.export_openmetrics()
            self._send_text(200, prom_text, content_type="text/plain; version=0.0.4; charset=utf-8")
            return

        # 2e-2. Google Perspective Cutover Readiness Certificate
        elif path == "/v1/cutover/certificate":
            org = query.get("org", ["Enterprise Publishing Partner"])[0]
            fmt = query.get("format", ["json"])[0].lower()
            cert_data = CutoverCertificationEngine.generate_certificate(organization_name=org)
            if fmt == "html":
                html_out = CutoverCertificationEngine.generate_html_certificate(cert_data)
                self._send_text(200, html_out, content_type="text/html; charset=utf-8")
                return
            else:
                self._send_json(200, cert_data)
                return

        # 2e-3. Commercial Billing Plans Catalog
        elif path == "/v1/billing/plans":
            self._send_json(200, billing_engine.get_plans())

        # 2e-4. Tenant Billing & Subscription Status
        elif path == "/v1/billing/status":
            tid = query.get("tenant_id", [""])[0]
            if not tid:
                self._send_json(400, {"error": "Missing 'tenant_id' query parameter."})
                return
            res = billing_engine.get_billing_status(tid)
            status_code = 404 if "error" in res else 200
            self._send_json(status_code, res)

        # 2f. EU Digital Services Act (DSA) Compliance Report
        elif path == "/v1/compliance/dsa-report":
            fmt = query.get("format", ["json"])[0].lower()
            dsa_data = ComplianceReporter.generate_dsa_data()
            if fmt == "markdown" or fmt == "md":
                md_bytes = ComplianceReporter.generate_markdown_report(dsa_data).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/markdown; charset=utf-8")
                self.send_header("Content-Length", str(len(md_bytes)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(md_bytes)
                return
            elif fmt == "html":
                html_bytes = ComplianceReporter.generate_html_report(dsa_data).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(html_bytes)))
                self.end_headers()
                self.wfile.write(html_bytes)
                return
            else:
                self._send_json(200, dsa_data)

        # 2g. Raw Audit & Compliance Export (CSV or JSONL)
        elif path == "/v1/audit/export":
            fmt = query.get("format", ["csv"])[0].lower()
            record_type = query.get("type", ["evaluations"])[0].lower()
            limit = int(query.get("limit", [1000])[0])
            anonymize = query.get("anonymize", ["false"])[0].lower() in ["true", "1", "yes"]

            if record_type == "appeals":
                csv_data = AuditExporter.export_appeals_csv(limit=limit).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/csv; charset=utf-8")
                self.send_header("Content-Disposition", 'attachment; filename="beyond_likes_dsa_appeals.csv"')
                self.send_header("Content-Length", str(len(csv_data)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(csv_data)
                return
            else:
                if fmt == "jsonl":
                    jsonl_data = AuditExporter.export_evaluations_jsonl(limit=limit, anonymize=anonymize).encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
                    self.send_header("Content-Disposition", 'attachment; filename="beyond_likes_audit_evaluations.jsonl"')
                    self.send_header("Content-Length", str(len(jsonl_data)))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(jsonl_data)
                    return
                else:
                    csv_data = AuditExporter.export_evaluations_csv(limit=limit, anonymize=anonymize).encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_header("Content-Disposition", 'attachment; filename="beyond_likes_audit_evaluations.csv"')
                    self.send_header("Content-Length", str(len(csv_data)))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(csv_data)
                    return

        # 2h. List DSA Article 20 Moderation Appeals
        elif path == "/v1/appeals":
            status_filter = query.get("status", [None])[0]
            limit = int(query.get("limit", [50])[0])
            appeals = get_appeals(status_filter=status_filter, limit=limit)
            self._send_json(200, {"appeals": appeals, "total": len(appeals)})

        # 3. Available Policies (Built-in + Custom DB profiles)
        elif path == "/v1/policies":
            self._send_json(200, get_all_policies())

        # 4. Live Simulated Stream for Mission Control UI
        elif path == "/v1/live-feed-sample":
            import random
            sample_count = int(query.get("count", [3])[0])
            chosen = random.sample(LIVE_STREAM_POOL, min(sample_count, len(LIVE_STREAM_POOL)))
            evaluated_feed = []
            for item in chosen:
                res = evaluator.evaluate(item["text"])
                guidance = RephraseAdvisor.generate_suggestions(res, item["text"])
                evaluated_feed.append({
                    "timestamp": time.strftime("%H:%M:%S"),
                    "platform": item["source"],
                    "author": item["author"],
                    "text": item["text"],
                    "composite_score": res["composite_score"],
                    "status": res["status"],
                    "dimensions": res["dimensions"],
                    "flags": res["flags"],
                    "suggested_revision": guidance["suggested_revision"]
                })
            self._send_json(200, {"feed": evaluated_feed})

        # 5. ROI & Moderator Hours Saved Calculator
        elif path == "/v1/roi-calculator":
            monthly_comments = int(query.get("comments_per_month", [50000])[0])
            mod_wage_usd = float(query.get("hourly_wage", [30.0])[0])

            # Industry benchmarks: avg moderator reviews 45 comments/hr
            manual_hours_needed = monthly_comments / 45.0
            manual_cost_usd = manual_hours_needed * mod_wage_usd

            # Normative Intelligence auto-processes 70% of comments cleanly
            hours_saved = manual_hours_needed * 0.65
            dollars_saved = hours_saved * mod_wage_usd

            self._send_json(200, {
                "monthly_volume": monthly_comments,
                "moderator_hourly_wage": f"${mod_wage_usd:.2f}",
                "manual_review_hours_est": round(manual_hours_needed, 1),
                "manual_cost_usd": f"${manual_cost_usd:,.2f}",
                "hours_saved_monthly": round(hours_saved, 1),
                "dollars_saved_monthly": f"${dollars_saved:,.2f}",
                "roi_multiple": round(dollars_saved / 199.0, 1) # Against $199 Pro SaaS plan
            })

        # 5b. View Rendered HTML Proposal
        elif path == "/v1/proposals/view":
            client_name = query.get("client_name", ["Enterprise Partner"])[0]
            monthly_vol = int(query.get("comments_per_month", [100000])[0])
            wage = float(query.get("hourly_wage", [30.0])[0])
            plan = query.get("plan", ["growth"])[0]
            prop = ProposalGenerator.generate(client_name=client_name, monthly_volume=monthly_vol, hourly_wage=wage, plan=plan)
            html_content = prop.get("documents", {}).get("html", "<h1>Technical Migration Assessment</h1>")
            html_bytes = html_content.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html_bytes)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(html_bytes)
            return

        # 5c. View Comprehensive Commercial Proposal Packet (HTML or JSON)
        elif path == "/v1/proposals/packet":
            client_slug = query.get("client", query.get("slug", ["the-verge"]))[0]
            fmt = query.get("format", ["html"])[0].lower()
            accept_header = self.headers.get("Accept", "").lower()
            if "application/json" in accept_header and "text/html" not in accept_header:
                fmt = "json" 

            proposals_dir = os.path.join(BASE_DIR, "proposals")
            html_file = os.path.join(proposals_dir, f"{client_slug}_executive_packet.html")

            if not os.path.exists(html_file):
                from tools.generate_client_proposal_packet import build_client_packet
                build_client_packet(client_slug)

            if fmt == "json":
                from tools.generate_client_proposal_packet import build_client_packet
                res = build_client_packet(client_slug)
                self._send_json(200, res)
                return

            with open(html_file, "r", encoding="utf-8") as f:
                content = f.read().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
            return

        # 5d. List Target Client Proposal Packets Catalog
        elif path == "/v1/proposals/packets":
            from tools.generate_client_proposal_packet import get_all_profiles
            profs = get_all_profiles()
            items = []
            for k, v in profs.items():
                items.append({
                    "slug": k,
                    "name": v["client_name"],
                    "category": v["category"],
                    "monthly_volume": v["monthly_volume"],
                    "plan": v["plan"],
                    "packet_url": f"/v1/proposals/packet?client={k}",
                    "packet_json": f"/v1/proposals/packet?client={k}&format=json"
                })
            self._send_json(200, {"total": len(items), "packets": items})

        # 5e. GTM Outreach Pipeline CRM
        elif path == "/v1/outreach/pipeline":
            status_filter = query.get("status", [None])[0]
            pipeline = get_outreach_pipeline(status_filter=status_filter)
            self._send_json(200, pipeline)

        # 5e2. Social Media & Syndication Campaign
        elif path == "/v1/social/campaign":
            from tools.dispatch_social_campaign import get_all_channels
            channels = get_all_channels()
            self._send_json(200, {"channels": channels, "total": len(channels)})

        # 5f. Integration Packages Catalog & Download
        elif path == "/v1/downloads":
            from tools.package_integrations import build_all_packages
            pkgs = build_all_packages()
            self._send_json(200, {"packages": pkgs})

        elif path.startswith("/v1/downloads/"):
            pkg_id = path.replace("/v1/downloads/", "").strip()
            from tools.package_integrations import PACKAGES, DOWNLOADS_DIR, build_all_packages
            if pkg_id in PACKAGES:
                meta = PACKAGES[pkg_id]
                zip_path = os.path.join(DOWNLOADS_DIR, meta["filename"])
                if not os.path.exists(zip_path):
                    build_all_packages()
                if os.path.exists(zip_path):
                    with open(zip_path, "rb") as f:
                        data = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/zip")
                    self.send_header("Content-Disposition", f'attachment; filename="{meta["filename"]}"')
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
                    return
            self._send_json(404, {"error": f"Package '{pkg_id}' not found."})
            return

        # 6. Audit Logs
        elif path == "/v1/audit-logs":
            logs = get_recent_evaluations(limit=50)
            self._send_json(200, {"logs": logs})

        # 7. Database Stats
        elif path == "/v1/stats":
            stats = get_system_stats()
            self._send_json(200, stats)

        # 8. Economics simulator
        elif path == "/v1/economics":
            econ = simulate_economics()
            self._send_json(200, econ)

        # 9. Executive Discourse Audit Reports
        elif path == "/v1/reports":
            fmt = query.get("format", ["json"])[0].lower()
            hourly_wage = float(query.get("hourly_wage", [35.0])[0])
            report_data = generate_report_data(hourly_wage=hourly_wage)
            
            if fmt == "markdown" or fmt == "md":
                md_text = generate_markdown_report(report_data).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/markdown; charset=utf-8")
                self.send_header("Content-Length", str(len(md_text)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(md_text)
                return
            elif fmt == "html":
                html_text = generate_html_report(report_data).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(html_text)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(html_text)
                return
            else:
                self._send_json(200, report_data)

        # 9b. Time-Series Discourse Health Analytics
        elif path == "/v1/analytics/trends":
            hours = int(query.get("hours", [24])[0])
            bucket_mins = int(query.get("bucket", [60])[0])
            trend_data = get_timeseries_analytics(window_hours=hours, bucket_minutes=bucket_mins)
            self._send_json(200, trend_data)

        # 10. Real-time Server-Sent Events (SSE) Stream
        elif path == "/v1/stream":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            client_queue = broadcaster.subscribe()
            try:
                init_msg = f"event: connected\ndata: {json.dumps({'message': 'Connected to Normative Intelligence live stream'})}\n\n"
                self.wfile.write(init_msg.encode("utf-8"))
                self.wfile.flush()

                while True:
                    try:
                        evt = client_queue.get(timeout=10)
                        payload = f"event: {evt['event']}\ndata: {json.dumps(evt['data'])}\n\n"
                        self.wfile.write(payload.encode("utf-8"))
                        self.wfile.flush()
                    except queue.Empty:
                        heartbeat = f": keepalive {time.time()}\n\n"
                        self.wfile.write(heartbeat.encode("utf-8"))
                        self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass
            finally:
                broadcaster.unsubscribe(client_queue)
            return

        else:
            self._send_json(404, {"error": f"Path '{path}' not found"})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self._read_body_json()

        # Check API key authentication
        api_key = self.headers.get("x-api-key") or self.headers.get("Authorization")
        if api_key and api_key.startswith("Bearer "):
            api_key = api_key[7:]

        valid, err_msg, client_meta = verify_api_key(api_key)
        if not valid:
            self._send_json(401, {"error": err_msg})
            return

        record_api_call(client_meta, path)

        client_id = client_meta["client_name"] if client_meta else "anonymous"

        # 1. Primary Scoring Endpoint
        if path == "/v1/score":
            text = body.get("text", "")
            context = body.get("context", "")
            policy = body.get("policy", "newsroom")
            backend = body.get("backend", "heuristic")

            if not text:
                self._send_json(400, {"error": "Missing 'text' parameter in request body."})
                return
            
            cached = get_cached_result(text)
            if cached and cached.get("policy_applied") == policy and cached.get("backend") == backend:
                telemetry.record_cache_hit()
                self._send_json(200, cached)
                return

            telemetry.record_cache_miss()
            result = evaluator.evaluate(text, context=context, policy=policy, backend=backend)
            rephrase = RephraseAdvisor.generate_suggestions(result, text)
            result["guidance"] = rephrase

            telemetry.record_evaluation(
                composite_score=result["composite_score"],
                status=result["status"],
                salvaged=(result["status"] in ["APPROVED_PROMOTED", "STANDARD_PUBLISH"] and result["composite_score"] >= 65.0),
                stealth=("FLAGGED" in result["status"] or result["composite_score"] < 40.0)
            )

            store_result(text, result, client_key=client_id, latency_ms=result["metrics"]["latency_ms"])
            
            broadcaster.broadcast("comment_evaluated", {
                "timestamp": time.strftime("%H:%M:%S"),
                "platform": "API Direct",
                "author": client_id,
                "text": text[:160],
                "composite_score": result["composite_score"],
                "status": result["status"],
                "dimensions": result["dimensions"],
                "flags": result["flags"],
                "suggested_revision": rephrase.get("suggested_revision", "")
            })

            # Outbound Webhook notification for severe civility breaches
            if "FLAGGED" in result["status"] or result["composite_score"] < 35.0:
                dispatcher.dispatch("comment_quarantined", {
                    "text_snippet": text[:160],
                    "status": result["status"],
                    "composite_score": result["composite_score"],
                    "dimensions": result["dimensions"],
                    "client_id": client_id,
                    "policy": policy
                })

            self._send_json(200, result)

        # 2. In-Composer Rephraser Endpoint
        elif path == "/v1/rephrase":
            text = body.get("text", "")
            policy = body.get("policy", "newsroom")
            if not text:
                self._send_json(400, {"error": "Missing 'text' parameter."})
                return
            eval_res = evaluator.evaluate(text, policy=policy)
            suggestions = RephraseAdvisor.generate_suggestions(eval_res, text)
            self._send_json(200, suggestions)

        # 3. Batch Scoring Endpoint
        elif path == "/v1/batch-score":
            comments = body.get("comments", [])
            policy = body.get("policy", "newsroom")
            backend = body.get("backend", "heuristic")
            if not isinstance(comments, list) or not comments:
                self._send_json(400, {"error": "Expected non-empty list of 'comments'."})
                return

            batch_results = []
            scores = []
            status_counts = {}

            for c in comments:
                if isinstance(c, dict):
                    c_text = c.get("text", "")
                    c_id = c.get("id")
                elif isinstance(c, str):
                    c_text = c
                    c_id = None
                else:
                    c_text = str(c)
                    c_id = None

                try:
                    res = evaluator.evaluate(c_text, policy=policy, backend=backend)
                    rephrase = RephraseAdvisor.generate_suggestions(res, c_text)
                    res["guidance"] = rephrase
                    if c_id:
                        res["id"] = c_id
                    batch_results.append(res)
                    scores.append(res.get("composite_score", 50.0))
                    st = res.get("status", "NEEDS_IMPROVEMENT")
                    status_counts[st] = status_counts.get(st, 0) + 1
                except Exception as eval_err:
                    batch_results.append({
                        "id": c_id,
                        "text": str(c_text)[:120],
                        "error": str(eval_err),
                        "composite_score": 50.0,
                        "status": "EVALUATION_ERROR"
                    })

            avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0
            health_index = round(sum(1 for s in batch_results if s.get("composite_score", 0) >= 60.0) / len(batch_results) * 100, 1) if batch_results else 0.0

            self._send_json(200, {
                "total_analyzed": len(batch_results),
                "community_health_index": health_index,
                "average_score": avg_score,
                "status_distribution": status_counts,
                "policy_used": policy,
                "items": batch_results
            })

        # 4. Discourse Webhook
        elif path == "/v1/webhooks/discourse":
            resp = process_discourse_webhook(body)
            self._send_json(200, resp)

        # 5. WordPress Webhook
        elif path == "/v1/webhooks/wordpress":
            resp = process_wordpress_webhook(body)
            self._send_json(200, resp)

        # 6. Perspective API Drop-in
        elif path == "/v1/comments:analyze" or path == "/v1alpha1/comments:analyze":
            resp = perspective_adapter.handle_request(body)
            self._send_json(200, resp)

        # 7. Dynamic Custom Policy Creation
        elif path == "/v1/policies":
            policy_id = body.get("id")
            name = body.get("name")
            desc = body.get("description", "Custom community policy profile.")
            weights = body.get("weights")
            thresholds = body.get("thresholds")

            if not policy_id or not name or not weights or not thresholds:
                self._send_json(400, {"error": "Missing required fields: id, name, weights, thresholds"})
                return

            if not isinstance(weights, dict) or not isinstance(thresholds, dict):
                self._send_json(400, {"error": "Weights and thresholds must be JSON objects."})
                return

            w_sum = sum(weights.values())
            if abs(w_sum - 1.0) > 0.05:
                self._send_json(400, {"error": f"Sum of weights must equal 1.0 (got {w_sum:.2f})"})
                return

            save_custom_policy(policy_id, name, desc, weights, thresholds)
            self._send_json(200, {
                "status": "SAVED",
                "policy_id": policy_id,
                "message": f"Custom policy '{name}' successfully registered and live."
            })

        # 8. Multi-Turn Conversational Thread Analysis
        elif path == "/v1/thread:analyze":
            comments = body.get("comments", [])
            topic = body.get("topic", "")
            policy = body.get("policy", "newsroom")
            backend = body.get("backend", "heuristic")

            if not isinstance(comments, list) or not comments:
                self._send_json(400, {"error": "Expected non-empty list of 'comments' for thread evaluation."})
                return

            res = thread_evaluator.analyze_thread(comments, topic=topic, policy=policy, backend=backend)

            if res.get("thread_escalation_index", 0) >= 65:
                broadcaster.broadcast("flame_war_alert", {
                    "topic": topic,
                    "tei": res["thread_escalation_index"],
                    "action": res["action_routing"]["action"],
                    "timestamp": time.strftime("%H:%M:%S")
                })
                dispatcher.dispatch("flame_war_detected", {
                    "topic": topic,
                    "tei": res["thread_escalation_index"],
                    "action": res["action_routing"]["action"],
                    "turn_count": len(comments)
                })

            self._send_json(200, res)

        # 9. Executive Proposal & TCO Generator
        elif path == "/v1/proposals/generate":
            client_name = body.get("client_name", "Enterprise Partner")
            monthly_volume = int(body.get("monthly_volume", 100000))
            hourly_wage = float(body.get("hourly_wage", 30.0))
            current_solution = body.get("current_solution", "Google Perspective API + Manual Review")
            plan = body.get("plan", "growth")

            proposal = ProposalGenerator.generate(
                client_name=client_name,
                monthly_volume=monthly_volume,
                hourly_wage=hourly_wage,
                current_solution=current_solution,
                plan=plan
            )
            self._send_json(200, proposal)

        # 9b. Update GTM Outreach Client Status
        elif path == "/v1/outreach/status":
            slug = body.get("slug")
            if not slug:
                self._send_json(400, {"error": "Missing required field 'slug'."})
                return
            status = body.get("status")
            notes = body.get("notes")
            contact_name = body.get("contact_name")
            contact_email = body.get("contact_email")
            last_contact_date = body.get("last_contact_date")

            updated = update_outreach_client(
                slug=slug,
                status=status,
                notes=notes,
                contact_name=contact_name,
                contact_email=contact_email,
                last_contact_date=last_contact_date
            )
            if not updated:
                self._send_json(404, {"error": f"Client target '{slug}' not found."})
                return
            self._send_json(200, {"success": True, "target": updated})

        # 9c. Update Social Campaign Channel Status
        elif path == "/v1/social/status":
            from tools.dispatch_social_campaign import update_channel_status, generate_status_report
            channel = body.get("channel")
            status = body.get("status")
            published_url = body.get("published_url")
            notes = body.get("notes")
            if not channel or not status:
                self._send_json(400, {"error": "Missing required fields 'channel' and 'status'."})
                return
            update_channel_status(channel, status, published_url, notes)
            generate_status_report()
            self._send_json(200, {"success": True, "channel": channel, "status": status})

        # 10. Perspective Shadow Mirror Dual-Run
        elif path == "/v1/shadow-mirror":
            text = body.get("text", "")
            comments = body.get("comments", [])
            policy = body.get("policy", "newsroom")
            backend = body.get("backend", "heuristic")

            if not text and not comments:
                self._send_json(400, {"error": "Expected 'text' string or 'comments' array."})
                return

            if text:
                result = shadow_mirror_engine.evaluate_shadow(text, policy=policy, backend=backend)
                category = result["comparison"]["discrepancy_category"]
                
                broadcaster.broadcast("shadow_evaluation", {
                    "timestamp": time.strftime("%H:%M:%S"),
                    "snippet": result["text_snippet"],
                    "perspective_toxic": result["perspective"]["toxicity_score"],
                    "beyond_composite": result["beyond_likes"]["composite_score"],
                    "category": category,
                    "verdict_agreement": result["comparison"]["verdict_agreement"]
                })

                if category == "FALSE_POSITIVE_SALVAGED":
                    dispatcher.dispatch("false_positive_salvaged", result)
                elif category == "STEALTH_EVASION_INTERCEPTED":
                    dispatcher.dispatch("stealth_evasion_intercepted", result)

                self._send_json(200, result)
            else:
                batch_out = []
                for c in comments:
                    batch_out.append(shadow_mirror_engine.evaluate_shadow(c, policy=policy, backend=backend))
                stats = get_shadow_stats()
                self._send_json(200, {
                    "total_evaluated": len(batch_out),
                    "stats": stats,
                    "items": batch_out
                })

        # 11. Register Outbound Webhook Subscription
        elif path == "/v1/webhooks/subscriptions":
            url = body.get("url")
            events = body.get("events", ["*"])
            secret = body.get("secret", "")
            sub_id = body.get("id")

            if not url or not url.startswith(("http://", "https://")):
                self._send_json(400, {"error": "A valid 'url' starting with http:// or https:// is required."})
                return

            sub_id_created = save_webhook_subscription(url=url, events=events, secret=secret, sub_id=sub_id)
            self._send_json(200, {
                "status": "REGISTERED",
                "subscription_id": sub_id_created,
                "url": url,
                "events": events
            })

        # 12. Test Dispatch Outbound Webhook
        elif path == "/v1/webhooks/test":
            sub_id = body.get("subscription_id")
            event_type = body.get("event", "ping")
            if not sub_id:
                self._send_json(400, {"error": "Missing 'subscription_id' in body."})
                return
            res = dispatcher.test_dispatch(subscription_id=sub_id, sample_event=event_type)
            self._send_json(200 if res.get("success") else 502, res)

        # 13. Dynamic Multi-Tier Ensemble Router
        elif path in ["/v1/ensemble:analyze", "/v1/ensemble/analyze"]:
            text = body.get("text", "")
            context = body.get("context")
            policy = body.get("policy", "newsroom")
            force_tier = body.get("force_tier")
            if not text:
                self._send_json(400, {"error": "Missing 'text' parameter in request body."})
                return

            res = ensemble_router.route_and_evaluate(text=text, context=context, policy=policy, force_tier=force_tier)
            self._send_json(200, res)

        # 14. Submit DSA Article 20 Appeal
        elif path in ["/v1/appeals:submit", "/v1/appeals/submit"]:
            reason = body.get("reason") or body.get("justification") or body.get("explanation")
            if reason and "reason" not in body:
                body["reason"] = reason
            if not body.get("user_id") and body.get("author_id"):
                body["user_id"] = body.get("author_id")
            if not body.get("reason") and not body.get("revised_text"):
                self._send_json(400, {"error": "Appeal requires at least a 'reason' or a 'revised_text'."})
                return
            res = AppealsEngine.submit_appeal(body)
            self._send_json(200, res)

        # 15. Resolve DSA Article 20 Appeal (Moderator Action)
        elif path in ["/v1/appeals:resolve", "/v1/appeals/resolve"]:
            appeal_id = body.get("appeal_id")
            decision = body.get("decision")
            notes = body.get("moderator_notes", "")
            if not appeal_id or not decision:
                self._send_json(400, {"error": "Missing required fields: 'appeal_id' and 'decision'."})
                return
            res = AppealsEngine.resolve_appeal_action(appeal_id=int(appeal_id), decision=decision, moderator_notes=notes)
            status_code = 200 if res.get("success") else 400
            self._send_json(status_code, res)

        # 16. Enterprise Workspace Tenants Provisioning
        elif path == "/v1/tenants":
            name = str(body.get("name", "")).strip()
            if not name:
                self._send_json(400, {"error": "Missing 'name' parameter for new tenant."})
                return
            tier = body.get("tier", "growth")
            quota = body.get("monthly_quota")
            tid = body.get("tenant_id")
            tenant = create_tenant(name=name, tier=tier, monthly_quota=quota, tenant_id=tid)
            self._send_json(201, tenant)

        # 17. Tenant Scoped API Key Generation
        elif path == "/v1/tenants/keys":
            tid = body.get("tenant_id")
            key_name = body.get("key_name", "Production Key")
            scopes = body.get("scopes", ["*"])
            if not tid:
                self._send_json(400, {"error": "Missing 'tenant_id' parameter in request body."})
                return
            key_res = create_tenant_api_key(tenant_id=tid, key_name=key_name, scopes=scopes)
            self._send_json(201, key_res)

        # 18. Historical Corpus Shadow Replay Benchmarker
        elif path == "/v1/shadow-mirror/replay":
            corpus = body.get("corpus") or body.get("items")
            if not corpus:
                corpus = CorpusReplayEngine.generate_gold_corpus()
            name = body.get("name", "Corpus Replay Benchmark")
            tid = body.get("tenant_id") or (client_meta.get("tenant_id") if client_meta else None)
            res = CorpusReplayEngine.run_replay(corpus=corpus, name=name, tenant_id=tid)
            self._send_json(200, res)

        # 19. Commercial Stripe Checkout Session
        elif path in ["/v1/billing/checkout", "/v1/billing/checkout-session"]:
            tid = body.get("tenant_id") or (client_meta.get("tenant_id") if client_meta else None)
            plan_id = body.get("plan_id", "growth")
            cycle = body.get("billing_cycle", "monthly")
            email = body.get("customer_email")
            s_url = body.get("success_url")
            c_url = body.get("cancel_url")
            if not tid:
                self._send_json(400, {"error": "Missing 'tenant_id' parameter in request body."})
                return
            res = billing_engine.create_checkout_session(
                tenant_id=tid,
                plan_id=plan_id,
                billing_cycle=cycle,
                customer_email=email,
                success_url=s_url,
                cancel_url=c_url
            )
            status_code = 400 if "error" in res else 200
            self._send_json(status_code, res)

        # 20. Inbound Stripe Webhook Ingestion
        elif path == "/v1/billing/webhook":
            sig = self.headers.get("Stripe-Signature", "")
            res = billing_engine.verify_and_process_webhook(payload_data=body, signature_header=sig)
            status_code = 200 if res.get("success") else 400
            self._send_json(status_code, res)

        # 21. Simulated 1-Click Sandbox Tier Upgrade
        elif path == "/v1/billing/simulate-upgrade":
            tid = body.get("tenant_id") or (client_meta.get("tenant_id") if client_meta else None)
            plan_id = body.get("plan_id", "growth")
            email = body.get("email", "billing@partner.org")
            if not tid:
                self._send_json(400, {"error": "Missing 'tenant_id' parameter in request body."})
                return
            res = billing_engine.simulate_instant_upgrade(tenant_id=tid, target_plan=plan_id, email=email)
            status_code = 200 if res.get("success") else 400
            self._send_json(status_code, res)

        else:
            self._send_json(404, {"error": f"Endpoint '{path}' not found"})

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path.startswith("/v1/webhooks/subscriptions"):
            sub_id = query.get("id", [""])[0]
            if not sub_id and "/" in path.strip("/"):
                parts = path.strip("/").split("/")
                if len(parts) >= 4: # /v1/webhooks/subscriptions/<id>
                    sub_id = parts[3]
            if not sub_id:
                self._send_json(400, {"error": "Missing webhook subscription 'id' in query or URL path."})
                return
            deleted = delete_webhook_subscription(sub_id)
            if deleted:
                self._send_json(200, {"status": "DELETED", "subscription_id": sub_id})
            else:
                self._send_json(404, {"error": f"Webhook subscription '{sub_id}' not found."})

        elif path.startswith("/v1/tenants/keys"):
            key_val = query.get("key", [""])[0]
            if not key_val and "/" in path.strip("/"):
                parts = path.strip("/").split("/")
                if len(parts) >= 4:
                    key_val = parts[3]
            if not key_val:
                self._send_json(400, {"error": "Missing API key in query '?key=' or URL path."})
                return
            deleted = delete_tenant_api_key(key_val)
            if deleted:
                self._send_json(200, {"status": "REVOKED", "key": key_val})
            else:
                self._send_json(404, {"error": f"API key '{key_val}' not found."})

        elif path.startswith("/v1/policies"):
            policy_id = query.get("id", [""])[0]
            if not policy_id and "/" in path.strip("/"):
                parts = path.strip("/").split("/")
                if len(parts) >= 3:
                    policy_id = parts[2]
            if not policy_id:
                self._send_json(400, {"error": "Missing policy 'id' in query or URL path."})
                return
            if policy_id in POLICY_PROFILES:
                self._send_json(403, {"error": f"Cannot delete default system policy '{policy_id}'."})
                return
            deleted = delete_custom_policy(policy_id)
            if deleted:
                self._send_json(200, {"status": "DELETED", "policy_id": policy_id})
            else:
                self._send_json(404, {"error": f"Policy '{policy_id}' not found."})
        else:
            self._send_json(404, {"error": f"Path '{path}' not found"})

    def log_message(self, format, *args):
        sys.stderr.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] NormativeIntelligenceAPI {args[0]} {args[1]}\n")

def run_server():
    server_address = (HOST, PORT)
    httpd = ThreadingHTTPServer(server_address, NormativeIntelligenceAPIHandler)
    print("\n" + "="*70)
    print(f"🚀 Normative Intelligence Platform (Port {PORT})")
    print(f"📡 Dashboard & UI/UX Studio: http://localhost:{PORT}/")
    print(f"🔌 Single Score API:         POST http://localhost:{PORT}/v1/score")
    print(f"🔌 Batch Corpus Analysis:    POST http://localhost:{PORT}/v1/batch-score")
    print(f"🔌 Discourse Webhook:        POST http://localhost:{PORT}/v1/webhooks/discourse")
    print(f"🔌 WordPress Webhook:        POST http://localhost:{PORT}/v1/webhooks/wordpress")
    print(f"🔌 Perspective Drop-in:      POST http://localhost:{PORT}/v1/comments:analyze")
    print(f"📊 Live Stream Feed:         GET  http://localhost:{PORT}/v1/live-feed-sample")
    print(f"💰 ROI Calculator:           GET  http://localhost:{PORT}/v1/roi-calculator")
    print("="*70 + "\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server gracefully...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
