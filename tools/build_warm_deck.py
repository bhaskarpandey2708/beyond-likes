#!/usr/bin/env python3
"""
Normative Intelligence — Cinematic Fluid-Slide Pitch Deck Builder
Rebuilds brand/pitch-deck.html with:
- Genuine fluid slide glide transitions (translateX with cubic-bezier easing and blur)
- Generous, customizable pacing (default 6 seconds, adjustable)
- Clean play/pause and manual navigation
- Interactive hover tooltips
- NO download clutter
- Warm Terracotta & Linen Editorial design system
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "brand", "pitch-deck.html")

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Normative Intelligence — Enterprise Pitch Deck</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #faf8f5;
      --slide-bg: #ffffff;
      --text: #18181b;
      --text-muted: #52525b;
      --text-subtle: #71717a;
      --border: #e8e3d8;
      --border-subtle: #f4f0e8;

      --accent: #c8441b;
      --accent-light: #fdf2ee;
      --accent-border: #f8c9bc;
      --accent-hover: #b13712;

      --juniper: #0d5c4e;
      --juniper-light: #edf7f4;
      --juniper-border: #bce3db;

      --amber: #b45309;
      --amber-light: #fffbeb;
      --amber-border: #fde68a;

      --rose: #be123c;
      --rose-light: #fff1f2;
      --rose-border: #fecdd3;

      --card-bg: #fdfcf9;
      --shadow-sm: 0 1px 3px rgba(39, 30, 20, 0.05);
      --shadow-md: 0 8px 24px -4px rgba(39, 30, 20, 0.08);
      --shadow-lg: 0 20px 50px -10px rgba(39, 30, 20, 0.12);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 24px;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }

    /* Deck Controls Header */
    .controls-header {
      width: 100%;
      max-width: 1120px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      gap: 16px;
      flex-wrap: wrap;
    }

    .brand-tag {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 1.05rem;
      font-weight: 800;
      color: var(--text);
      letter-spacing: -0.02em;
    }

    .brand-logo-mark {
      width: 32px;
      height: 32px;
      flex-shrink: 0;
    }

    .deck-nav-btns {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }

    .btn {
      background: #ffffff;
      color: var(--text);
      border: 1px solid var(--border);
      padding: 8px 15px;
      border-radius: 8px;
      font-size: 0.84rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
      box-shadow: var(--shadow-sm);
      text-decoration: none;
      font-family: inherit;
    }

    .btn:hover {
      background: var(--bg);
      border-color: #d1c8b8;
      color: var(--text);
    }

    .btn-toggle-play {
      background: #ffffff;
      border: 1px solid var(--border);
      color: var(--text);
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-weight: 700;
      padding: 8px 14px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.82rem;
      font-family: inherit;
      transition: all 0.15s;
    }
    .btn-toggle-play:hover {
      border-color: var(--accent);
      background: var(--accent-light);
      color: var(--accent);
    }

    .pulse-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10b981;
      display: inline-block;
      animation: pulseGreen 1.8s infinite;
    }
    .pulse-dot.paused {
      background: #f59e0b;
      animation: none;
    }

    @keyframes pulseGreen {
      0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
      70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
      100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    .slide-counter {
      font-size: 0.86rem;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      color: var(--text-muted);
      min-width: 95px;
      text-align: center;
      background: #ffffff;
      padding: 7px 12px;
      border-radius: 8px;
      border: 1px solid var(--border);
    }

    /* Slide Frame (16:9 Aspect Ratio) */
    .deck-stage {
      width: 100%;
      max-width: 1120px;
      background: var(--slide-bg);
      border: 1px solid var(--border);
      border-radius: 16px;
      box-shadow: var(--shadow-lg);
      aspect-ratio: 16 / 9;
      position: relative;
      overflow: hidden;
      display: block;
    }

    /* Auto-Advance Progress Bar */
    .slide-progress-track {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 4px;
      background: rgba(232, 227, 216, 0.5);
      z-index: 50;
    }

    .slide-progress-bar {
      height: 100%;
      width: 0%;
      background: var(--accent);
      transition: width 0.04s linear;
    }

    .slide-stage-overlay-notice {
      position: absolute;
      bottom: 12px;
      right: 20px;
      z-index: 40;
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--text-subtle);
      background: rgba(255, 255, 255, 0.92);
      padding: 4px 10px;
      border-radius: 20px;
      border: 1px solid var(--border);
      backdrop-filter: blur(4px);
      pointer-events: none;
      opacity: 0.85;
      transition: opacity 0.2s;
    }

    /* REAL FLUID SLIDE TRANSITION (Glides with inertia) */
    .slide {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      padding: 48px 60px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: var(--slide-bg);
      opacity: 0;
      transform: translateX(100%);
      filter: blur(4px);
      pointer-events: none;
      transition: transform 0.75s cubic-bezier(0.16, 1, 0.3, 1),
                  opacity 0.65s cubic-bezier(0.16, 1, 0.3, 1),
                  filter 0.65s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 1;
    }

    .slide.active {
      opacity: 1;
      transform: translateX(0);
      filter: blur(0);
      pointer-events: auto;
      z-index: 2;
    }

    .slide.slide-prev {
      opacity: 0;
      transform: translateX(-100%);
      filter: blur(4px);
      pointer-events: none;
      z-index: 1;
    }

    .slide.slide-next {
      opacity: 0;
      transform: translateX(100%);
      filter: blur(4px);
      pointer-events: none;
      z-index: 1;
    }

    /* Slide Typography & Elements */
    .slide-top-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.74rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-subtle);
    }

    .slide-badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    .badge-terracotta { background: var(--accent-light); color: var(--accent); border: 1px solid var(--accent-border); }
    .badge-amber { background: var(--amber-light); color: var(--amber); border: 1px solid var(--amber-border); }
    .badge-juniper { background: var(--juniper-light); color: var(--juniper); border: 1px solid var(--juniper-border); }

    .slide-body {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      margin: 14px 0;
    }

    .slide-title {
      font-size: 2.15rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1.16;
      color: var(--text);
      margin-bottom: 10px;
    }

    .serif-accent {
      font-family: 'Instrument Serif', Georgia, serif;
      font-style: italic;
      font-weight: 400;
      color: var(--accent);
    }

    .slide-subtitle {
      font-size: 1.05rem;
      color: var(--text-muted);
      line-height: 1.55;
      max-width: 860px;
      margin-bottom: 20px;
    }

    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
    .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }

    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      position: relative;
      transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
    }
    .card:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
      border-color: #d8d0c2;
    }

    .card-title {
      font-size: 1.02rem;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 6px;
    }

    .card-desc {
      font-size: 0.85rem;
      color: var(--text-muted);
      line-height: 1.55;
    }

    .metric-num {
      font-size: 2.2rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      color: var(--text);
      line-height: 1;
      margin-bottom: 6px;
    }

    .metric-lbl {
      font-size: 0.74rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-subtle);
    }

    /* Interactive Editorial Tooltips */
    .has-tooltip {
      position: relative;
      cursor: help;
      border-bottom: 1px dashed var(--accent);
    }
    .has-tooltip:hover::after {
      content: attr(data-tooltip);
      position: absolute;
      bottom: 125%;
      left: 50%;
      transform: translateX(-50%);
      background: #18181b;
      color: #faf8f5;
      padding: 7px 12px;
      border-radius: 6px;
      font-size: 0.76rem;
      font-weight: 500;
      line-height: 1.4;
      white-space: normal;
      width: 240px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.25);
      border: 1px solid #3f3f46;
      z-index: 100;
      pointer-events: none;
      animation: fadeIn 0.15s ease;
      text-transform: none;
      letter-spacing: normal;
    }
    .has-tooltip:hover::before {
      content: '';
      position: absolute;
      bottom: 110%;
      left: 50%;
      transform: translateX(-50%);
      border: 6px solid transparent;
      border-top-color: #18181b;
      z-index: 101;
      pointer-events: none;
    }

    table.deck-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
    }

    table.deck-table th, table.deck-table td {
      padding: 10px 14px;
      border-bottom: 1px solid var(--border);
      text-align: left;
    }

    table.deck-table th {
      background: var(--bg);
      color: var(--text-muted);
      font-weight: 700;
      text-transform: uppercase;
      font-size: 0.72rem;
      letter-spacing: 0.05em;
    }

    table.deck-table td.col-highlight {
      background: var(--accent-light);
      font-weight: 700;
      color: var(--accent);
    }

    table.deck-table th.col-highlight {
      background: var(--accent-light);
      color: var(--accent);
      font-weight: 800;
    }

    code {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      background: #ffffff;
      border: 1px solid var(--border);
      padding: 2px 7px;
      border-radius: 5px;
      color: var(--text);
    }

    .slide-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid var(--border-subtle);
      padding-top: 12px;
      font-size: 0.74rem;
      color: var(--text-subtle);
      font-weight: 600;
    }
  </style>
</head>
<body>

  <!-- Controls Header -->
  <div class="controls-header">
    <div class="brand-tag">
      <svg class="brand-logo-mark" viewBox="0 0 32 32" fill="none">
        <rect width="32" height="32" rx="8" fill="#18181b"/>
        <path d="M9 22V10L14 20V22H9Z" fill="#c8441b"/>
        <path d="M23 10V22L18 12V10H23Z" fill="#c8441b"/>
        <circle cx="16" cy="16" r="2.2" fill="#faf8f5"/>
      </svg>
      <span>Normative<span style="color: var(--accent);">.AI</span></span>
      <span style="font-weight: 500; color: var(--text-subtle); font-size: 0.85rem;">• 16:9 Master Pitch Deck</span>
    </div>

    <div class="deck-nav-btns">
      <button class="btn-toggle-play" id="playPauseBtn" onclick="togglePlayPause()" title="Pause or Resume Auto-Advance">
        <span class="pulse-dot" id="pulseDot"></span>
        <span id="playPauseLabel">Auto-Advancing</span>
      </button>
      <button class="btn" onclick="cyclePacing()" id="pacingBtn" title="Change presentation pace">⏱ 6s Pace</button>
      <button class="btn" onclick="prevSlide()" title="Previous slide (Left Arrow)">← Prev</button>
      <span class="slide-counter" id="slideCounter">Slide 1 of 12</span>
      <button class="btn" onclick="nextSlide()" title="Next slide (Right Arrow)">Next →</button>
      <a class="btn" href="/" title="Return to Showcase Home">Studio Desk</a>
      <a class="btn" href="/benchmarks" title="Explore Empirical Whitepaper">Whitepaper</a>
    </div>
  </div>

  <!-- Deck Stage -->
  <div class="deck-stage" id="deckStage" onmouseenter="onHoverPause()" onmouseleave="onHoverResume()">

    <!-- Progress Track (Auto-Play Timer Bar) -->
    <div class="slide-progress-track">
      <div class="slide-progress-bar" id="progressBar"></div>
    </div>

    <div class="slide-stage-overlay-notice">
      Hover cursor to pause slide &bull; Left/Right keys to navigate
    </div>

    <!-- SLIDE 1: Title & Strategic Purpose -->
    <div class="slide active">
      <div class="slide-top-meta">
        <span>Autonomous Discourse Infrastructure</span>
        <span class="slide-badge badge-terracotta has-tooltip" data-tooltip="Sovereign enterprise infrastructure designed for mission-critical digital discourse.">Enterprise Infrastructure</span>
      </div>
      <div class="slide-body" style="text-align: center; max-width: 860px; margin: 0 auto;">
        <div style="display: inline-flex; align-items: center; gap: 10px; margin-bottom: 22px;">
          <svg style="width: 38px; height: 38px;" viewBox="0 0 32 32" fill="none">
            <rect width="32" height="32" rx="8" fill="#18181b"/>
            <path d="M9 22V10L14 20V22H9Z" fill="#c8441b"/>
            <path d="M23 10V22L18 12V10H23Z" fill="#c8441b"/>
            <circle cx="16" cy="16" r="2.2" fill="#faf8f5"/>
          </svg>
          <span style="font-size: 1.65rem; font-weight: 800; letter-spacing: -0.03em;">Normative<span style="color: var(--accent);">.AI</span></span>
        </div>
        <h1 class="slide-title" style="font-size: 2.75rem;">
          The Drop-In Prosocial Infrastructure for <em class="serif-accent">Digital Discourse.</em>
        </h1>
        <p class="slide-subtitle" style="margin: 0 auto 28px auto;">
          The <span class="has-tooltip" data-tooltip="100% Bitwise schema parity: returns identical attributeScores.TOXICITY responses to existing Perspective clients.">1:1 bitwise successor</span> to Google Perspective API. Moving digital journalism and enterprise forums from binary censorship to continuous normative epistemic intelligence.
        </p>
        <div style="font-size: 0.86rem; color: var(--text-subtle); display: inline-flex; align-items: center; gap: 8px; background: var(--card-bg); border: 1px solid var(--border); padding: 8px 18px; border-radius: 30px;">
          <span>Architect &amp; Founder: <strong>Bhaskar Pandey</strong></span>
          <span>&bull;</span>
          <span>Executive Contact: <code style="background: var(--accent-light); color: var(--accent); border-color: var(--accent-border);">bhaskarauthor@gmail.com</code></span>
        </div>
      </div>
      <div class="slide-footer">
        <span>Normative Intelligence &bull; Confidential Board &amp; Investor Deck</span>
        <span>Perspective Sunset: Dec 31, 2026</span>
      </div>
    </div>

    <!-- SLIDE 2: The Catalyst (Perspective Sunset) -->
    <div class="slide slide-next">
      <div class="slide-top-meta">
        <span>Market Urgency</span>
        <span class="slide-badge badge-amber has-tooltip" data-tooltip="Google Jigsaw is permanently taking down the Perspective API servers on Dec 31, 2026.">Hard Sunset: Dec 31, 2026</span>
      </div>
      <div class="slide-body">
        <h2 class="slide-title">Google Is Turning Off the Perspective API in <em class="serif-accent">60 Days.</em></h2>
        <p class="slide-subtitle">
          On December 31, 2026, Google Jigsaw decommissions Perspective API. Over 1,000+ digital publishers, newsrooms, and online communities face an immediate operational cliff.
        </p>
        <div class="grid-3">
          <div class="card" style="border-left: 4px solid var(--amber);">
            <div class="metric-num" style="color: var(--amber);">60 Days</div>
            <div class="metric-lbl">Remaining Until Outage</div>
            <p class="card-desc" style="margin-top: 10px;">
              Publishers that fail to cut over will see automated moderation fail, swamping editorial desks with unreviewed queues.
            </p>
          </div>
          <div class="card" style="border-left: 4px solid var(--accent);">
            <div class="metric-num" style="color: var(--accent);">Zero Refactor</div>
            <div class="metric-lbl">Engineering Requirement</div>
            <p class="card-desc" style="margin-top: 10px;">
              Newsrooms lack 6 months to rebuild pipelines. They require an immediate, bitwise drop-in replacement that takes 5 minutes.
            </p>
          </div>
          <div class="card" style="border-left: 4px solid var(--juniper);">
            <div class="metric-num" style="color: var(--juniper);">100% Ready</div>
            <div class="metric-lbl">Normative Drop-in Gateway</div>
            <p class="card-desc" style="margin-top: 10px;">
              Normative Intelligence consumes exact Perspective JSON schemas and responds with identical fields.
            </p>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <span>The Market Catalyst &bull; Perspective API Deprecation</span>
        <span>Slide 2 / 12</span>
      </div>
    </div>

    <!-- SLIDE 3: The Deeper Crisis (Binary Toxicity Failure) -->
    <div class="slide slide-next">
      <div class="slide-top-meta">
        <span>Structural Failure of Legacy Tools</span>
        <span class="slide-badge badge-terracotta">The Core Problem</span>
      </div>
      <div class="slide-body">
        <h2 class="slide-title">Keyword &amp; Toxicity Filters <em class="serif-accent">Broke Online Discourse.</em></h2>
        <p class="slide-subtitle">
          Legacy classifiers (2017–2025) measured only one negative dimension: crude toxicity. This created four critical points of failure across digital publishers:
        </p>
        <div class="grid-4">
          <div class="card">
            <div class="card-title">1. False Positive Bans</div>
            <p class="card-desc">Bans benign technical syntax (<code class="has-tooltip" data-tooltip="Perspective incorrectly flags this command as violent suicide/threat language.">kill -9</code>, <code>fatal error</code>) and medical discussions, alienating high-IQ subscribers.</p>
          </div>
          <div class="card">
            <div class="card-title">2. Low-Effort Snark</div>
            <p class="card-desc">Permits passive-aggressive, zero-value cynicism as long as no explicit slurs are used, destroying discussion signal.</p>
          </div>
          <div class="card">
            <div class="card-title">3. Censorship Backlash</div>
            <p class="card-desc">Silent deletions anger paying subscribers. Readers feel treated like children rather than intellectual peers.</p>
          </div>
          <div class="card">
            <div class="card-title">4. Queue Burnout</div>
            <p class="card-desc">Publishers spend hundreds of thousands in human moderator hours manually resolving false flags and appeals.</p>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <span>The Problem &bull; Why Legacy Toxicity Classifiers Failed</span>
        <span>Slide 3 / 12</span>
      </div>
    </div>

    <!-- SLIDE 4: The Solution (4D Normative Intelligence) -->
    <div class="slide slide-next">
      <div class="slide-top-meta">
        <span>Proprietary 4D Normative Rubric</span>
        <span class="slide-badge badge-juniper">The Solution</span>
      </div>
      <div class="slide-body">
        <h2 class="slide-title">Normative 4D Intelligence: <em class="serif-accent">Prosocial Governance.</em></h2>
        <p class="slide-subtitle">
          Instead of binary censorship, we evaluate discourse across four continuous normative dimensions engineered for high-stakes digital communities:
        </p>
        <div class="grid-4">
          <div class="card" style="border-top: 4px solid var(--accent);">
            <div style="font-size: 1.25rem; font-weight: 800; color: var(--accent); margin-bottom: 4px;">Constructiveness</div>
            <div style="font-weight: 700; font-size: 0.76rem; color: var(--text-subtle); margin-bottom: 8px;">35% WEIGHT</div>
            <p class="card-desc">Does the comment substantiate claims with empirical evidence, benchmarks, or actionable alternatives?</p>
          </div>
          <div class="card" style="border-top: 4px solid var(--juniper);">
            <div style="font-size: 1.25rem; font-weight: 800; color: var(--juniper); margin-bottom: 4px;">Civility</div>
            <div style="font-weight: 700; font-size: 0.76rem; color: var(--text-subtle); margin-bottom: 8px;">25% WEIGHT</div>
            <p class="card-desc">Evaluates mutual intellectual respect without suppressing intense scientific or technical debate.</p>
          </div>
          <div class="card" style="border-top: 4px solid var(--amber);">
            <div style="font-size: 1.25rem; font-weight: 800; color: var(--amber); margin-bottom: 4px;">Persuasiveness</div>
            <div style="font-weight: 700; font-size: 0.76rem; color: var(--text-subtle); margin-bottom: 8px;">20% WEIGHT</div>
            <p class="card-desc">Epistemic grounding, logical consistency, and coherence rather than purely emotive hyperbole.</p>
          </div>
          <div class="card" style="border-top: 4px solid var(--text);">
            <div style="font-size: 1.25rem; font-weight: 800; color: var(--text); margin-bottom: 4px;">Relevance</div>
            <div style="font-weight: 700; font-size: 0.76rem; color: var(--text-subtle); margin-bottom: 8px;">20% WEIGHT</div>
            <p class="card-desc">Topical alignment to article context, filtering out spam, off-topic derails, and promotional link clutter.</p>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <span>The Solution &bull; 4D Normative Evaluation Rubric</span>
        <span>Slide 4 / 12</span>
      </div>
    </div>

    <!-- SLIDE 5: Technical Parity & Cutover Architecture -->
    <div class="slide slide-next">
      <div class="slide-top-meta">
        <span>Architecture &amp; Parity</span>
        <span class="slide-badge badge-terracotta">1:1 Drop-in Ready</span>
      </div>
      <div class="slide-body">
        <h2 class="slide-title">Zero-Code Engineering Cutover: <em class="serif-accent">5 Minutes.</em></h2>
        <div class="grid-2">
          <div>
            <p class="card-desc" style="font-size: 0.94rem; margin-bottom: 16px;">
              Publishers switch one endpoint URL. Existing ingestion webhooks, background queues, and administrative tools keep running with 100% bitwise parity.
            </p>
            <div class="card" style="margin-bottom: 12px; background: var(--rose-light); border-color: var(--rose-border);">
              <div style="font-size: 0.76rem; font-weight: 700; color: var(--rose); margin-bottom: 6px;">BEFORE: Google Perspective (Deprecating Dec 31, 2026)</div>
              <code style="font-size: 0.78rem; color: var(--rose); background: #ffffff;">POST https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze</code>
            </div>
            <div class="card" style="background: var(--juniper-light); border-color: var(--juniper-border);">
              <div style="font-size: 0.76rem; font-weight: 700; color: var(--juniper); margin-bottom: 6px;">AFTER: Normative Intelligence (Drop-in Gateway)</div>
              <code style="font-size: 0.78rem; color: var(--juniper); background: #ffffff;">POST https://beyond-likes-platform.onrender.com/v1/comments:analyze</code>
            </div>
          </div>
          <div>
            <div class="card" style="height: 100%;">
              <div class="card-title">Engineering SLA Guarantee</div>
              <ul style="list-style: none; font-size: 0.86rem; color: var(--text-muted); line-height: 2.1;">
                <li>⚡ <strong>&lt; 3.0 ms Latency:</strong> Local quantized CPU engine (vs 195ms WAN).</li>
                <li>🔒 <strong>100% Schema Parity:</strong> Returns identical <code>attributeScores.TOXICITY</code>.</li>
                <li>🛡️ <strong>Anti-Evasion:</strong> Intercepts leetspeak, zero-width, and stealth slurs.</li>
                <li>⚖️ <strong>DSA Art. 20 Ready:</strong> Built-in algorithmic transparency portal.</li>
                <li>🟢 <strong>99.99% Uptime:</strong> Enterprise SLA backing with financial credits.</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <span>Technical Architecture &bull; 100% Bitwise Perspective Wire Parity</span>
        <span>Slide 5 / 12</span>
      </div>
    </div>

    <!-- SLIDE 6: Product Suite (In-Composer Nudge & Appeals) -->
    <div class="slide slide-next">
      <div class="slide-top-meta">
        <span>Full Ecosystem</span>
        <span class="slide-badge badge-juniper">Complete Enterprise Suite</span>
      </div>
      <div class="slide-body">
        <h2 class="slide-title">Beyond Filtering: <em class="serif-accent">The Prosocial Triad.</em></h2>
        <div class="grid-3">
          <div class="card">
            <div class="metric-num" style="color: var(--accent); font-size: 1.8rem;">In-Composer</div>
            <div class="metric-lbl">Pre-submission Nudges</div>
            <p class="card-desc" style="margin-top: 10px;">
              Git-style inline diff suggestions guide commenters to substantiate heated claims before submitting, reducing moderator queues by ~35%.
            </p>
          </div>
          <div class="card">
            <div class="metric-num" style="color: var(--juniper); font-size: 1.8rem;">Shadow Mirror</div>
            <div class="metric-lbl">Dual-Run Parallel Mode</div>
            <p class="card-desc" style="margin-top: 10px;">
              Run side-by-side with Perspective on live production traffic with zero DNS risk to verify parity before formal cutover.
            </p>
          </div>
          <div class="card">
            <div class="metric-num" style="color: var(--amber); font-size: 1.8rem;">DSA Portal</div>
            <div class="metric-lbl">Statutory Article 20 Appeals</div>
            <p class="card-desc" style="margin-top: 10px;">
              Automated Statement-of-Reasons generation and internal complaint management satisfying European Union Digital Services Act mandates.
            </p>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <span>Product Suite &bull; Real-time Nudges, Parity Mirror &amp; Compliance</span>
        <span>Slide 6 / 12</span>
      </div>
    </div>

    <!-- SLIDE 7: High-Scale Deployment Reach & Ecosystem Architecture -->
    <div class="slide slide-next">
      <div class="slide-top-meta">
        <span>Enterprise Ecosystem Reach</span>
        <span class="slide-badge badge-juniper">Universal Compatibility</span>
      </div>
      <div class="slide-body">
        <h2 class="slide-title">Engineered for High-Scale <em class="serif-accent">Publishing Architectures.</em></h2>
        <div class="grid-4" style="margin-bottom: 20px;">
          <div class="card">
            <div class="metric-num" style="color: var(--juniper);">100M+</div>
            <div class="metric-lbl">Monthly Addressable Events</div>
            <p class="card-desc" style="font-size: 0.8rem; margin-top: 4px;">High-throughput comment pipelines across digital media.</p>
          </div>
          <div class="card">
            <div class="metric-num" style="color: var(--accent);">4 Archetypes</div>
            <div class="metric-lbl">Ecosystem Footprint</div>
            <p class="card-desc" style="font-size: 0.8rem; margin-top: 4px;">Newsrooms, Tech Forums, Creator Networks, Open Communities.</p>
          </div>
          <div class="card">
            <div class="metric-num" style="color: var(--amber);">&lt; 3.0 ms</div>
            <div class="metric-lbl">Edge Latency SLA</div>
            <p class="card-desc" style="font-size: 0.8rem; margin-top: 4px;">Runs local quantized inference without external roundtrips.</p>
          </div>
          <div class="card">
            <div class="metric-num" style="color: var(--text);">100%</div>
            <div class="metric-lbl">Zero Refactor Parity</div>
            <p class="card-desc" style="font-size: 0.8rem; margin-top: 4px;">WordPress VIP, Discourse, Coral Project, and Custom CMS.</p>
          </div>
        </div>
        <p class="card-desc" style="text-align: center; font-size: 0.9rem; max-width: 780px; margin: 0 auto;">
          Built to replace the sunsetting Perspective API infrastructure across all major CMS platforms, discussion software, and custom newsroom backends without requiring internal engineering refactoring.
        </p>
      </div>
      <div class="slide-footer">
        <span>Deployment Footprint &bull; Universal CMS &amp; Forum Compatibility</span>
        <span>Slide 7 / 12</span>
      </div>
    </div>

    <!-- SLIDE 8: Business Model & Pricing Tiers -->
    <div class="slide slide-next">
      <div class="slide-top-meta">
        <span>Business Model</span>
        <span class="slide-badge badge-terracotta">Predictable B2B SaaS</span>
      </div>
      <div class="slide-body">
        <h2 class="slide-title">Subscription Economics &amp; <em class="serif-accent">Tiered Pricing.</em></h2>
        <div class="grid-3">
          <div class="card">
            <div class="card-title">Starter</div>
            <div class="metric-num" style="font-size: 2rem;">$99<span style="font-size: 0.9rem; color: var(--text-subtle);">/mo</span></div>
            <div class="metric-lbl">Boutique &amp; Creator Blogs</div>
            <ul style="list-style: none; font-size: 0.82rem; color: var(--text-muted); margin-top: 14px; line-height: 1.8;">
              <li>&bull; Up to 50k comments/month</li>
              <li>&bull; Perspective Drop-in Gateway</li>
              <li>&bull; WordPress Plugin Included</li>
              <li>&bull; Community Support</li>
            </ul>
          </div>
          <div class="card" style="border: 2px solid var(--accent); background: var(--accent-light);">
            <div class="card-title" style="color: var(--accent);">Growth (Most Popular)</div>
            <div class="metric-num" style="font-size: 2rem; color: var(--accent);">$499<span style="font-size: 0.9rem; color: var(--text-subtle);">/mo</span></div>
            <div class="metric-lbl">Mid-Market Newsrooms</div>
            <ul style="list-style: none; font-size: 0.82rem; color: var(--text-muted); margin-top: 14px; line-height: 1.8;">
              <li>&bull; Up to 250k comments/month</li>
              <li>&bull; 1:1 Perspective Drop-in SLA</li>
              <li>&bull; In-Composer Nudge Widget</li>
              <li>&bull; Dual-Run Shadow Mirror</li>
              <li>&bull; Standard 99.9% Uptime SLA</li>
            </ul>
          </div>
          <div class="card">
            <div class="card-title">Enterprise</div>
            <div class="metric-num" style="font-size: 2rem;">$1,499<span style="font-size: 0.9rem; color: var(--text-subtle);">/mo</span></div>
            <div class="metric-lbl">Tier-1 Publishing Networks</div>
            <ul style="list-style: none; font-size: 0.82rem; color: var(--text-muted); margin-top: 14px; line-height: 1.8;">
              <li>&bull; Unlimited Volume / Custom Quotas</li>
              <li>&bull; Sub-3.0ms Latency SLA Guarantee</li>
              <li>&bull; 99.99% Uptime Contract (MSA)</li>
              <li>&bull; Dedicated Cutover Engineers</li>
              <li>&bull; Full EU DSA Article 20 Portal</li>
            </ul>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <span>Business Model &bull; Predictable Annual Recurring SaaS</span>
        <span>Slide 8 / 12</span>
      </div>
    </div>

    <!-- SLIDE 9: Gross Margin & Infrastructure Economics -->
    <div class="slide slide-next">
      <div class="slide-top-meta">
        <span>Unit Economics</span>
        <span class="slide-badge badge-juniper">94% Gross Margin</span>
      </div>
      <div class="slide-body">
        <h2 class="slide-title">Quantized CPU Engine vs. <em class="serif-accent">Cloud LLM Inflation.</em></h2>
        <div class="grid-2">
          <div class="card">
            <div class="card-title">The Cloud LLM Margin Trap</div>
            <p class="card-desc" style="margin-bottom: 12px;">
              Competitors routing every comment to OpenAI/Anthropic pay ~$0.005 per evaluation, blowing up latency (>800ms) and destroying margins.
            </p>
            <div class="metric-num" style="color: var(--rose); font-size: 1.8rem;">$500 per 100k</div>
            <div class="metric-lbl">LLM Cloud Inference Cost</div>
          </div>
          <div class="card" style="border: 2px solid var(--juniper); background: var(--juniper-light);">
            <div class="card-title" style="color: var(--juniper);">Normative Local Quantization</div>
            <p class="card-desc" style="margin-bottom: 12px;">
              Our quantized DeBERTa + heuristic gate runs locally on commodity CPU cores with zero external GPU API fees.
            </p>
            <div class="metric-num" style="color: var(--juniper); font-size: 1.8rem;">&lt; $0.05 per 100k</div>
            <div class="metric-lbl">Normative Infrastructure Cost (94%+ Margin)</div>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <span>Unit Economics &bull; Scalable High-Margin Infrastructure</span>
        <span>Slide 9 / 12</span>
      </div>
    </div>

    <!-- SLIDE 10: Competitive Differentiation Matrix -->
    <div class="slide slide-next">
      <div class="slide-top-meta">
        <span>Competitive Landscape</span>
        <span class="slide-badge badge-terracotta">Unmatched Position</span>
      </div>
      <div class="slide-body">
        <h2 class="slide-title">How Normative Intelligence <em class="serif-accent">Compares.</em></h2>
        <table class="deck-table">
          <thead>
            <tr>
              <th>Evaluation Dimension</th>
              <th>Google Perspective</th>
              <th>OpenAI Moderation</th>
              <th>Hive / Automod</th>
              <th class="col-highlight">Normative Intelligence</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Status Post-2026</strong></td>
              <td style="color: var(--rose); font-weight: 600;">Dead (Dec 31, 2026)</td>
              <td>Active</td>
              <td>Active</td>
              <td class="col-highlight">Drop-in Successor</td>
            </tr>
            <tr>
              <td><strong>Wire Compatibility</strong></td>
              <td>Original Schema</td>
              <td>New Schema Needed</td>
              <td>New Schema Needed</td>
              <td class="col-highlight">100% Bitwise Parity</td>
            </tr>
            <tr>
              <td><strong>Latency</strong></td>
              <td>195 ms (WAN)</td>
              <td>400–900 ms</td>
              <td>150–300 ms</td>
              <td class="col-highlight">&lt; 3.0 ms CPU</td>
            </tr>
            <tr>
              <td><strong>Intervention Mode</strong></td>
              <td>Post-publish Delete</td>
              <td>Post-publish Flag</td>
              <td>Keyword Deletion</td>
              <td class="col-highlight">Pre-submission Nudges</td>
            </tr>
            <tr>
              <td><strong>EU DSA Compliance</strong></td>
              <td>None</td>
              <td>None</td>
              <td>None</td>
              <td class="col-highlight">Full Article 20 Portal</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="slide-footer">
        <span>Competitive Landscape &bull; Direct Differentiation</span>
        <span>Slide 10 / 12</span>
      </div>
    </div>

    <!-- SLIDE 11: Architectural Pedigree -->
    <div class="slide slide-next">
      <div class="slide-top-meta">
        <span>Research Foundation</span>
        <span class="slide-badge badge-juniper">Architectural Pedigree</span>
      </div>
      <div class="slide-body">
        <h2 class="slide-title">Theoretical Motivation &amp; <em class="serif-accent">Enterprise Architecture.</em></h2>
        <p class="slide-subtitle">
          Commercialized from breakthrough research on normative multidimensional feedback systems on digital platforms:
        </p>
        <div class="grid-3">
          <div class="card">
            <div class="metric-num" style="font-size: 2rem; color: var(--accent);">+17.6%</div>
            <div class="metric-lbl">Constructive Engagement Lift</div>
            <p class="card-desc" style="margin-top: 8px;">Dual constructive feedback yields a 17.6% increase in empirical evidence sharing.</p>
          </div>
          <div class="card">
            <div class="metric-num" style="font-size: 2rem; color: var(--juniper);">-34.8%</div>
            <div class="metric-lbl">Ad Hominem Derailment</div>
            <p class="card-desc" style="margin-top: 8px;">In-composer nudges de-escalate emotional hostility prior to thread propagation.</p>
          </div>
          <div class="card">
            <div class="metric-num" style="font-size: 2rem; color: var(--amber);">100%</div>
            <div class="metric-lbl">Open Standard Compliance</div>
            <p class="card-desc" style="margin-top: 8px;">OpenAPI 3.0.3, W3C ActivityPub, and European Commission DSA compliance.</p>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <span>Sovereign Deep-Tech Venture &bull; Lead Architect &amp; Founder: Bhaskar Pandey</span>
        <span>Slide 11 / 12</span>
      </div>
    </div>

    <!-- SLIDE 12: Executive Cutover Invitation & Call to Action -->
    <div class="slide slide-next">
      <div class="slide-top-meta">
        <span>Next Steps</span>
        <span class="slide-badge badge-juniper">Activate 30-Day Sandbox</span>
      </div>
      <div class="slide-body" style="text-align: center; max-width: 800px; margin: 0 auto;">
        <h2 class="slide-title" style="font-size: 2.4rem;">Secure Your Perspective EOL Cutover <em class="serif-accent">Today.</em></h2>
        <p class="slide-subtitle" style="margin: 0 auto 24px auto;">
          Do not wait for Google's December 31, 2026 sunset. Activate a zero-risk 30-day dual-run shadow mirror on your live traffic with zero DNS impact.
        </p>
        <div style="background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 24px; margin-bottom: 24px;">
          <div style="font-weight: 700; font-size: 1.1rem; color: var(--text); margin-bottom: 6px;">
            Executive Technical Briefing &amp; Sandbox Setup
          </div>
          <p style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 16px;">
            15-minute architecture briefing with dedicated onboarding engineers.
          </p>
          <a class="btn btn-primary" href="mailto:bhaskarauthor@gmail.com?subject=Executive%20Briefing%3A%20Normative%20Perspective%20Cutover&body=Hi%20Bhaskar%2C%0A%0AWe%20would%20like%20to%20schedule%20a%2015-minute%20technical%20briefing%20to%20review%20the%20Perspective%20sunset%20cutover%20for%20our%20platform.%0A%0ABest%20regards%2C" style="font-size: 0.95rem; padding: 12px 28px; background: var(--accent); color: #fff; border-color: var(--accent);">
            📅 Schedule 15-Min Technical Briefing
          </a>
        </div>
        <div style="font-size: 0.82rem; color: var(--text-subtle);">
          Direct Founder Email: <a href="mailto:bhaskarauthor@gmail.com" style="color: var(--accent); text-decoration: none; font-weight: 600;">bhaskarauthor@gmail.com</a> &bull; Interactive Studio: <a href="/" style="color: var(--accent); text-decoration: none; font-weight: 600;">Studio Desk</a>
        </div>
      </div>
      <div class="slide-footer">
        <span>Normative Intelligence &bull; Executive Procurement &amp; Briefing</span>
        <span>Slide 12 / 12</span>
      </div>
    </div>

  </div>

  <script>
    let currentSlide = 0;
    const slides = Array.from(document.querySelectorAll('.slide'));
    const totalSlides = slides.length;
    const counter = document.getElementById('slideCounter');
    const progressBar = document.getElementById('progressBar');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const playPauseLabel = document.getElementById('playPauseLabel');
    const pulseDot = document.getElementById('pulseDot');
    const pacingBtn = document.getElementById('pacingBtn');

    // Auto-advance configuration (Human-readable pacing)
    const PACING_OPTIONS = [6000, 8000, 4000]; // 6s, 8s, 4s
    let pacingIndex = 0;
    let slideDurationMs = PACING_OPTIONS[pacingIndex];
    const PROGRESS_INTERVAL_MS = 25;
    let isAutoPlaying = true;
    let isHoverPaused = false;
    let elapsedMs = 0;
    let timerInterval = null;

    function cyclePacing() {
      pacingIndex = (pacingIndex + 1) % PACING_OPTIONS.length;
      slideDurationMs = PACING_OPTIONS[pacingIndex];
      const sec = Math.round(slideDurationMs / 1000);
      pacingBtn.textContent = `⏱ ${sec}s Pace`;
      elapsedMs = 0;
      progressBar.style.width = '0%';
    }

    // Initialize slide positions
    slides.forEach((s, idx) => {
      if (idx === 0) {
        s.className = 'slide active';
      } else {
        s.className = 'slide slide-next';
      }
    });

    function updateSlide(nextIndex, direction = 1) {
      if (nextIndex < 0) nextIndex = totalSlides - 1;
      if (nextIndex >= totalSlides) nextIndex = 0;
      if (nextIndex === currentSlide) return;

      const oldSlide = slides[currentSlide];
      const newSlide = slides[nextIndex];

      // Prepare target slide for incoming glide
      if (direction >= 0) {
        // Sliding forward: old slides out left, new slides in from right
        newSlide.style.transition = 'none';
        newSlide.className = 'slide slide-next';
        void newSlide.offsetWidth; // Force reflow
        newSlide.style.transition = '';

        oldSlide.className = 'slide slide-prev';
        newSlide.className = 'slide active';
      } else {
        // Sliding backward: old slides out right, new slides in from left
        newSlide.style.transition = 'none';
        newSlide.className = 'slide slide-prev';
        void newSlide.offsetWidth; // Force reflow
        newSlide.style.transition = '';

        oldSlide.className = 'slide slide-next';
        newSlide.className = 'slide active';
      }

      currentSlide = nextIndex;
      counter.textContent = `Slide ${currentSlide + 1} of ${totalSlides}`;
      elapsedMs = 0;
      progressBar.style.width = '0%';
    }

    function nextSlide() {
      updateSlide(currentSlide + 1, 1);
    }

    function prevSlide() {
      updateSlide(currentSlide - 1, -1);
    }

    function startTimer() {
      if (timerInterval) clearInterval(timerInterval);
      timerInterval = setInterval(() => {
        if (!isAutoPlaying || isHoverPaused) return;

        elapsedMs += PROGRESS_INTERVAL_MS;
        const pct = Math.min((elapsedMs / slideDurationMs) * 100, 100);
        progressBar.style.width = pct + '%';

        if (elapsedMs >= slideDurationMs) {
          nextSlide();
        }
      }, PROGRESS_INTERVAL_MS);
    }

    function togglePlayPause() {
      isAutoPlaying = !isAutoPlaying;
      updatePlayPauseUI();
    }

    function onHoverPause() {
      isHoverPaused = true;
      updatePlayPauseUI();
    }

    function onHoverResume() {
      isHoverPaused = false;
      updatePlayPauseUI();
    }

    function updatePlayPauseUI() {
      if (isAutoPlaying && !isHoverPaused) {
        pulseDot.classList.remove('paused');
        playPauseLabel.textContent = 'Auto-Advancing';
      } else if (isHoverPaused && isAutoPlaying) {
        pulseDot.classList.add('paused');
        playPauseLabel.textContent = 'Paused (Studying)';
      } else {
        pulseDot.classList.add('paused');
        playPauseLabel.textContent = 'Paused';
      }
    }

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === 'PageDown') {
        nextSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        prevSlide();
      } else if (e.key === ' ') {
        togglePlayPause();
      } else if (e.key === 'Home') {
        updateSlide(0, -1);
      } else if (e.key === 'End') {
        updateSlide(totalSlides - 1, 1);
      }
    });

    // Start auto-play timer on load
    startTimer();
  </script>
</body>
</html>
"""

def main():
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Successfully generated {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
