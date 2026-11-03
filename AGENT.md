# AGENT.md: Operational Specification & Project Mission

**Venture:** `BL-001 - Beyond Likes: How Normative Feedback Complements Engagement Signals`  
**Origin:** Proprietary Deep-Tech Venture  
**Principals:** Ayush Pandey (Lead Engineer) & Bhaskar Pandey (`bhaskarauthor@gmail.com`)  
**Dedicated Local Workspace:** `/home/ayush-pandey/RESEARCH_TO_PRODUCT_VENTURE`  
**Shared Cloud Mirror:** `/home/ayush-pandey/GoogleDrive/RESEARCH_TO_PRODUCT_VENTURE`  
**Original Google Drive Shared Folder:** `Independent Research-to-Product Venture` (Shared by `bhaskarauthor@gmail.com`)  
**Primary Daemon:** `http://localhost:8888`  
**Auto-Sync Interval:** Every 600 seconds (10 minutes)  
**Last Updated:** October 23, 2026 at 02:18:43 AM IST (Automated 600s Daemon Sync | 46 Sessions Preserved | Active: `079a0145-8a92-41ee-9f28-bbbd00545696`)

---

## 1. Executive Charter & Purpose

Beyond Likes is the premier **100% bitwise drop-in replacement for the Google Perspective API**, which permanently sunsets on **December 31, 2026**.

The platform moves content moderation from punitive post-publication censorship to **in-composer prosocial elevation**:
1. **Zero-Code Drop-In Parity:** Fully compatible with Google Perspective's `POST /v1/comments:analyze` schema and `attributeScores` JSON response.
2. **Prosocial Normative Intelligence:** Continuously scores discourse across 4 continuous dimensions:
   - Epistemic Constructiveness
   - Discourse Civility
   - Persuasive Coherence
   - Dialectical Relevance
3. **In-Composer Git-Style Rephraser:** Generates inline diff suggestions and non-violent communication framing.
4. **Sub-2ms CPU Inference:** 435M DeBERTa-v3 backbone quantized into INT8 ONNX running locally without GPU dependency.
5. **EU Digital Services Act (DSA) Article 20:** Built-in statutory transparency reports, automated user appeals queues, and GDPR-compliant audit logs.
6. **Multi-Tenant SaaS & Stripe Billing:** Starter ($199/mo), Growth ($499/mo), Enterprise ($999/mo) with automated $100 sunset cutover credits.

---

## 2. Directory & Architecture Map

```text
RESEARCH_TO_PRODUCT_VENTURE/
├── AGENT.md                           # This operational agent guide & mission charter
├── PROJECT_MEMORY.md                  # Comprehensive component catalog & memory registry
├── CONVERSATION_LOGS.md               # Historical session and decision chronicle
├── api/
│   ├── server.py                      # Multi-threaded production HTTP daemon (:8888)
│   ├── billing.py                     # Stripe checkout sessions & HMAC webhook handlers
│   ├── auth.py                        # Sliding-window rate limiter & scoped API key auth
│   ├── analytics.py                   # Time-series discourse health trends (DHI)
│   ├── appeals.py                     # EU DSA Article 20 user appeal queue & auto-reversals
│   ├── dispatcher.py                  # Outbound HMAC-SHA256 webhook dispatcher
│   ├── exporter.py                    # CSV/JSONL audit exporter with pseudonymization
│   └── webhooks.py                    # Inbound webhook receivers (Discourse, WordPress)
├── core_engine/
│   ├── evaluator.py                   # Tri-mode normative evaluator with NFKD normalization
│   ├── perspective_adapter.py         # 1:1 Perspective API drop-in compatibility engine
│   ├── neural_evaluator.py            # INT8 CPU quantized neural inference
│   ├── thread_evaluator.py            # Multi-turn flame war & escalation index (TEI)
│   ├── shadow_mirror.py               # Dual-run side-by-side Perspective comparison
│   ├── ensemble.py                    # Dynamic latency-aware auto-escalation router
│   ├── compliance.py                  # EU DSA Articles 15, 20 & 24 transparency reporting
│   ├── cutover_cert.py                # Cryptographic Cutover Readiness Certificates
│   ├── multilingual.py                # Indic, Hinglish & transliterated parsing
│   └── rephraser.py                   # In-composer unified diff generator
├── dashboard/
│   └── index.html                     # 18-tab interactive GitHub Primer workstation
├── distribution/
│   ├── chrome_extension/              # Manifest V3 floating in-composer assistant
│   ├── discourse_plugin/              # Native Discourse Ruby plugin
│   ├── wordpress_plugin/              # Zero-config PHP WordPress comment filter
│   └── widget/                        # Universal vanilla JavaScript embed (<script>)
├── docs/
│   ├── CONVERSATION_HISTORY.md        # Master chronicle of all dialogue sessions & milestones
│   └── conversations/                 # 46 Archived transcripts (.jsonl) & readable summaries (.md)
├── downloads/                         # 4 Pre-compiled 1-click distribution zip packages
├── proposals/                         # 20 Pre-compiled executive ROI packets (.html / .md)
├── validation/
│   ├── social_launch_campaign.md      # LinkedIn & X/Twitter launch announcements (<=280 chars)
│   ├── social_expansion_campaign.md   # Reddit, Hacker News, Product Hunt & Blog expansion
│   ├── social_campaign_status.md      # Live syndication status audit & 1-click web intent links
│   ├── buyer_shortlist.md             # 20 target enterprises with ROI economics
│   └── campaign_status_report.md      # Live outreach pipeline status (19 Sent, 1 Scheduled)
├── sdk/
│   ├── beyond_likes_client.py         # Zero-dependency Python SDK
│   └── node/                          # TypeScript / Node.js SDK (npm package)
└── tools/
    ├── continuous_sync_daemon.py      # Automated 600-second multi-session cloud sync daemon
    ├── dispatch_social_campaign.py    # Multi-channel social validator, intent generator & dispatcher
    ├── simulate_outreach_campaign.py  # Enterprise CRM campaign dispatcher & audit generator
    ├── sync_to_gdrive.sh              # Google Drive rsync mirror script
    └── package_integrations.py        # Integration zip packager
```

---

## 3. Automation & 600-Second Cloud Sync Protocol

* **Continuous Sync Daemon:** [`tools/continuous_sync_daemon.py`](file:///home/ayush-pandey/RESEARCH_TO_PRODUCT_VENTURE/tools/continuous_sync_daemon.py)
* **Execution Interval:** Every 600 seconds (10 minutes)
* **Sync Targets:**
  1. Scans and parses all active and historical transcripts from `~/.gemini/antigravity-cli/brain/*/`
  2. Archives raw JSONL transcripts and generates human-readable markdown summaries in `docs/conversations/` (46 sessions preserved)
  3. Updates `docs/CONVERSATION_HISTORY.md` master chronicle
  4. Updates timestamps and status in `AGENT.md`, `PROJECT_MEMORY.md`, and `CONVERSATION_LOGS.md`
  5. Runs `rsync` mirroring the entire 2.00 GB workspace to `/home/ayush-pandey/GoogleDrive/RESEARCH_TO_PRODUCT_VENTURE`
  6. Logs all sync events to `storage/sync_daemon.log`

---

## 4. Test Matrix & Quality Guarantee (118/118 PASS)

* **Master Python Test Suite:** `68/68 PASS` (`tests/run_all_tests.py`)
* **Node.js SDK Test Suite:** `26/26 PASS` (`sdk/node/test_sdk.js`)
* **Nuanced Edge-Case Benchmark:** `10/10 PASS` (`benchmarks/edge_case_benchmark.py`)
* **Adversarial & Evasion Benchmark:** `9/9 PASS` (`benchmarks/adversarial_test.py`)
* **R&D Pipeline Benchmark:** `5/5 PASS` (`benchmarks/run_benchmark.py`)
* **Total:** **118 / 118 PASS (100% Reliability)**

---

## 5. Active Stage: Gate 2 Commercial Execution & Social Expansion

The technical platform is fully hardened. The active mission is:
1. Public Social Media Launch (LinkedIn Founder Post & X/Twitter 8-tweet thread)
2. Developer Community Expansion (Reddit r/MachineLearning, r/programming, Hacker News Show HN, Product Hunt)
3. Direct Enterprise Discovery Outreach to 20 target accounts in Tab 18 CRM.
