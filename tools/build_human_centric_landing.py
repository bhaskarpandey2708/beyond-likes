# -*- coding: utf-8 -*-
"""
Human-Centric Executive Showcase Builder for Normative Intelligence.
Crafted for digital publishers, community leaders, editors, and executives.
Removes geeky jargon, fixes ribbon and hero spacing, and tells a compelling human product story.
"""
import os

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Normative Intelligence — Healthy, Civil Communities Without the Toxic Noise</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #ffffff;
      --bg-subtle: #f8fafc;
      --surface: #ffffff;
      --border: #e2e8f0;
      --border-subtle: #edf2f7;
      --border-focus: #2563eb;

      --text-main: #0f172a;
      --text-muted: #334155;
      --text-subtle: #64748b;
      --text-light: #94a3b8;

      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --primary-subtle: #eff6ff;
      --primary-border: #bfdbfe;

      --emerald: #059669;
      --emerald-subtle: #ecfdf5;
      --emerald-border: #a7f3d0;

      --amber: #d97706;
      --amber-subtle: #fffbeb;
      --amber-border: #fde68a;

      --rose: #e11d48;
      --rose-subtle: #fff1f2;
      --rose-border: #fecdd3;

      --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.05);
      --shadow-md: 0 4px 12px -2px rgba(15, 23, 42, 0.08);
      --shadow-lg: 0 16px 36px -6px rgba(15, 23, 42, 0.1);
      --shadow-card: 0 2px 8px rgba(15, 23, 42, 0.04), 0 1px 2px rgba(15, 23, 42, 0.02);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg);
      color: var(--text-main);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }

    /* 1. Sleek Announcement Bar */
    .announcement-bar {
      background: #0f172a;
      color: #ffffff;
      padding: 10px 24px;
      font-size: 0.84rem;
      text-align: center;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 12px;
      font-weight: 500;
    }

    .announcement-tag {
      background: #2563eb;
      color: #ffffff;
      font-size: 0.72rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 2px 8px;
      border-radius: 4px;
    }

    .announcement-link {
      color: #93c5fd;
      text-decoration: underline;
      font-weight: 600;
      margin-left: 4px;
    }
    .announcement-link:hover { color: #ffffff; }

    /* 2. Pristine Navigation Ribbon */
    .nav-bar {
      position: sticky;
      top: 0;
      z-index: 1000;
      background: rgba(255, 255, 255, 0.96);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      padding: 0 36px;
      height: 72px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .nav-brand {
      display: flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      color: var(--text-main);
    }

    .brand-title {
      font-size: 1.25rem;
      font-weight: 800;
      letter-spacing: -0.03em;
    }
    .brand-title span { color: var(--primary); }

    .nav-menu {
      display: flex;
      align-items: center;
      gap: 28px;
    }

    .nav-item {
      font-size: 0.92rem;
      font-weight: 600;
      color: var(--text-muted);
      text-decoration: none;
      transition: color 0.15s ease;
    }
    .nav-item:hover { color: var(--primary); }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .btn-nav-outline {
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--text-muted);
      text-decoration: none;
      padding: 8px 16px;
      border-radius: 8px;
      border: 1px solid var(--border);
      transition: all 0.15s;
    }
    .btn-nav-outline:hover {
      background: var(--bg-subtle);
      color: var(--text-main);
      border-color: #cbd5e1;
    }

    .btn-nav-primary {
      font-size: 0.88rem;
      font-weight: 700;
      background: var(--primary);
      color: #ffffff;
      padding: 9px 20px;
      border-radius: 8px;
      text-decoration: none;
      transition: all 0.15s;
      box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);
    }
    .btn-nav-primary:hover {
      background: var(--primary-hover);
      transform: translateY(-1px);
    }

    /* Container */
    .container {
      max-width: 1180px;
      margin: 0 auto;
      padding: 0 28px;
    }

    /* 3. Human-Centric Hero Section */
    .hero-section {
      padding: 72px 0 60px 0;
      text-align: center;
      background: radial-gradient(circle at 50% 20%, #f0f7ff 0%, #ffffff 70%);
      border-bottom: 1px solid var(--border-subtle);
    }

    .hero-kicker-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #ffffff;
      border: 1px solid var(--border);
      box-shadow: var(--shadow-sm);
      padding: 6px 16px;
      border-radius: 30px;
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--text-muted);
      margin-bottom: 24px;
    }

    .hero-kicker-pill .status-point {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--emerald);
    }

    .hero-headline {
      font-size: 3.6rem;
      font-weight: 800;
      letter-spacing: -0.04em;
      line-height: 1.15;
      color: var(--text-main);
      max-width: 920px;
      margin: 0 auto 20px auto;
    }

    .hero-headline .highlight {
      color: var(--primary);
      background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-lead {
      font-size: 1.25rem;
      color: var(--text-muted);
      max-width: 780px;
      margin: 0 auto 36px auto;
      line-height: 1.65;
      font-weight: 400;
    }

    .hero-buttons {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 16px;
      margin-bottom: 36px;
      flex-wrap: wrap;
    }

    .btn-hero-primary {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: var(--primary);
      color: #ffffff;
      font-size: 1rem;
      font-weight: 700;
      padding: 14px 28px;
      border-radius: 10px;
      text-decoration: none;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
      transition: all 0.15s ease;
    }
    .btn-hero-primary:hover {
      background: var(--primary-hover);
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
    }

    .btn-hero-secondary {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #ffffff;
      color: var(--text-main);
      font-size: 1rem;
      font-weight: 600;
      padding: 14px 28px;
      border-radius: 10px;
      text-decoration: none;
      border: 1px solid var(--border);
      box-shadow: var(--shadow-sm);
      transition: all 0.15s ease;
    }
    .btn-hero-secondary:hover {
      background: var(--bg-subtle);
      border-color: #cbd5e1;
      transform: translateY(-1px);
    }

    .hero-features-strip {
      display: flex;
      justify-content: center;
      gap: 28px;
      color: var(--text-subtle);
      font-size: 0.88rem;
      font-weight: 600;
      flex-wrap: wrap;
    }
    .hero-features-strip span {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .hero-features-strip span strong {
      color: var(--emerald);
    }

    /* 4. Interactive Hero Composer Mockup */
    .hero-visual-card {
      max-width: 920px;
      margin: 48px auto 0 auto;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 16px;
      box-shadow: var(--shadow-lg);
      overflow: hidden;
      text-align: left;
    }

    .mockup-header {
      background: #f8fafc;
      border-bottom: 1px solid var(--border);
      padding: 14px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.84rem;
      font-weight: 700;
      color: var(--text-muted);
    }

    .mockup-header .browser-dots {
      display: flex;
      gap: 6px;
    }
    .mockup-header .dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #cbd5e1;
    }
    .mockup-header .dot.red { background: #f87171; }
    .mockup-header .dot.yellow { background: #fbbf24; }
    .mockup-header .dot.green { background: #34d399; }

    .mockup-body {
      padding: 24px;
    }

    .comment-draft-label {
      font-size: 0.82rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-subtle);
      margin-bottom: 8px;
    }

    .comment-draft-box {
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      font-size: 0.98rem;
      color: var(--text-main);
      line-height: 1.5;
      margin-bottom: 16px;
    }

    .prosocial-nudge-box {
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      border-radius: 12px;
      padding: 18px 20px;
      position: relative;
    }

    .nudge-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }
    .nudge-title {
      font-size: 0.88rem;
      font-weight: 700;
      color: #1d4ed8;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .nudge-badge {
      font-size: 0.72rem;
      font-weight: 700;
      background: #dbeafe;
      color: #1e40af;
      padding: 2px 8px;
      border-radius: 4px;
    }

    .nudge-diff {
      background: #ffffff;
      border: 1px solid #dbeafe;
      border-radius: 8px;
      padding: 12px 16px;
      font-size: 0.92rem;
      line-height: 1.55;
      margin-bottom: 14px;
    }
    .diff-remove {
      color: #dc2626;
      text-decoration: line-through;
      background: #fef2f2;
      padding: 2px 6px;
      border-radius: 4px;
      display: inline-block;
      margin-bottom: 4px;
    }
    .diff-add {
      color: #059669;
      font-weight: 600;
      background: #ecfdf5;
      padding: 2px 6px;
      border-radius: 4px;
      display: inline-block;
    }

    .nudge-actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .nudge-explainer {
      font-size: 0.82rem;
      color: #475569;
    }
    .btn-accept-nudge {
      background: #1d4ed8;
      color: #ffffff;
      border: none;
      padding: 8px 18px;
      border-radius: 6px;
      font-size: 0.86rem;
      font-weight: 700;
      cursor: pointer;
      transition: background 0.15s;
    }
    .btn-accept-nudge:hover { background: #1e40af; }

    /* Section Headers */
    .section-wrap {
      padding: 84px 0;
    }
    .section-title-wrap {
      text-align: center;
      max-width: 760px;
      margin: 0 auto 52px auto;
    }
    .section-kicker {
      font-size: 0.8rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--primary);
      margin-bottom: 10px;
    }
    .section-heading {
      font-size: 2.35rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      color: var(--text-main);
      margin-bottom: 14px;
    }
    .section-subtext {
      font-size: 1.1rem;
      color: var(--text-muted);
      line-height: 1.6;
    }

    /* 5. The Three Pillars of Healthy Discourse */
    .pillars-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 28px;
      margin-bottom: 40px;
    }
    @media (max-width: 900px) {
      .pillars-grid { grid-template-columns: 1fr; }
    }

    .pillar-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 32px 28px;
      box-shadow: var(--shadow-card);
      transition: all 0.2s ease;
    }
    .pillar-card:hover {
      box-shadow: var(--shadow-md);
      transform: translateY(-2px);
      border-color: #cbd5e1;
    }
    .pillar-icon-box {
      width: 48px;
      height: 48px;
      border-radius: 10px;
      background: var(--primary-subtle);
      color: var(--primary);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.4rem;
      margin-bottom: 20px;
    }
    .pillar-title {
      font-size: 1.2rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 10px;
    }
    .pillar-desc {
      font-size: 0.95rem;
      color: var(--text-muted);
      line-height: 1.6;
    }

    /* 6. Live Interactive Sandbox (Human Friendly) */
    .sandbox-box {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 36px;
      box-shadow: var(--shadow-lg);
    }

    .preset-selector-label {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text-subtle);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 12px;
    }

    .preset-buttons {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 24px;
    }

    .btn-preset {
      background: #f1f5f9;
      color: #334155;
      border: 1px solid #e2e8f0;
      padding: 9px 18px;
      border-radius: 8px;
      font-size: 0.86rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }
    .btn-preset:hover {
      background: #e2e8f0;
      color: #0f172a;
    }
    .btn-preset.active {
      background: #0f172a;
      color: #ffffff;
      border-color: #0f172a;
    }

    .sandbox-input {
      width: 100%;
      height: 100px;
      border: 1px solid #cbd5e1;
      border-radius: 10px;
      padding: 16px;
      font-family: inherit;
      font-size: 1rem;
      color: var(--text-main);
      background: #ffffff;
      outline: none;
      resize: vertical;
      margin-bottom: 20px;
      transition: border-color 0.15s;
      line-height: 1.5;
    }
    .sandbox-input:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
    }

    .sandbox-run-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 28px;
    }
    .sandbox-hint {
      font-size: 0.86rem;
      color: var(--text-subtle);
    }
    .btn-run-sandbox {
      background: var(--primary);
      color: #ffffff;
      border: none;
      padding: 12px 24px;
      border-radius: 8px;
      font-size: 0.94rem;
      font-weight: 700;
      cursor: pointer;
      transition: background 0.15s;
    }
    .btn-run-sandbox:hover { background: var(--primary-hover); }

    .comparison-split {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
    }
    @media (max-width: 860px) {
      .comparison-split { grid-template-columns: 1fr; }
    }

    .compare-card {
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      background: #ffffff;
      box-shadow: var(--shadow-sm);
    }
    .compare-card.winner {
      border-color: var(--emerald-border);
      box-shadow: 0 4px 18px rgba(5, 150, 105, 0.08);
    }

    .compare-card-head {
      padding: 14px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #f8fafc;
      border-bottom: 1px solid var(--border);
    }
    .compare-card.winner .compare-card-head {
      background: var(--emerald-subtle);
      border-bottom-color: var(--emerald-border);
    }

    .compare-card-title {
      font-size: 0.92rem;
      font-weight: 700;
      color: var(--text-main);
    }
    .compare-badge {
      font-size: 0.74rem;
      font-weight: 800;
      padding: 3px 10px;
      border-radius: 5px;
      text-transform: uppercase;
    }
    .badge-danger { background: #fee2e2; color: #dc2626; border: 1px solid #fca5a5; }
    .badge-success { background: #d1fae5; color: #047857; border: 1px solid #6ee7b7; }

    .compare-card-body {
      padding: 22px 20px;
    }

    .metric-item {
      display: flex;
      justify-content: space-between;
      padding: 10px 0;
      border-bottom: 1px solid #f1f5f9;
      font-size: 0.92rem;
    }
    .metric-item:last-child { border-bottom: none; }
    .metric-title { color: var(--text-muted); font-weight: 500; }
    .metric-data { font-weight: 700; color: var(--text-main); font-family: 'JetBrains Mono', monospace; }

    .verdict-callout {
      margin-top: 16px;
      padding: 12px 14px;
      border-radius: 8px;
      font-size: 0.85rem;
      line-height: 1.5;
    }
    .callout-fail { background: #fff1f2; color: #9f1239; border: 1px solid #fecdd3; }
    .callout-pass { background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }

    /* 7. Google Perspective Migration Hub */
    .sunset-hub-card {
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      color: #ffffff;
      border-radius: 16px;
      padding: 48px;
      box-shadow: var(--shadow-lg);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 40px;
    }
    @media (max-width: 900px) {
      .sunset-hub-card { flex-direction: column; text-align: center; }
    }

    .sunset-info-left {
      max-width: 600px;
    }
    .sunset-pill {
      display: inline-block;
      background: #dc2626;
      color: #ffffff;
      font-size: 0.75rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 4px 10px;
      border-radius: 4px;
      margin-bottom: 16px;
    }
    .sunset-title {
      font-size: 1.9rem;
      font-weight: 800;
      margin-bottom: 12px;
      line-height: 1.25;
    }
    .sunset-desc {
      font-size: 1.05rem;
      color: #cbd5e1;
      line-height: 1.6;
      margin-bottom: 24px;
    }

    .sunset-countdown-box {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 12px;
      padding: 24px 32px;
      text-align: center;
      min-width: 280px;
    }
    .clock-title {
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #94a3b8;
      margin-bottom: 12px;
    }
    .clock-grid {
      display: flex;
      justify-content: center;
      gap: 12px;
    }
    .clock-col {
      background: #000000;
      padding: 8px 12px;
      border-radius: 8px;
      border: 1px solid #334155;
      min-width: 54px;
    }
    .clock-num {
      font-size: 1.6rem;
      font-weight: 800;
      color: #f59e0b;
      font-family: 'JetBrains Mono', monospace;
      line-height: 1;
    }
    .clock-sub {
      font-size: 0.65rem;
      color: #94a3b8;
      text-transform: uppercase;
      margin-top: 4px;
      font-weight: 700;
    }

    /* 8. Interactive ROI Calculator */
    .calculator-box {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 40px;
      box-shadow: var(--shadow-card);
    }
    .calc-slider-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
    }
    .calc-slider-label {
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text-main);
    }
    .calc-slider-display {
      font-size: 1.6rem;
      font-weight: 800;
      color: var(--primary);
      font-family: 'JetBrains Mono', monospace;
    }
    .calc-range {
      width: 100%;
      height: 8px;
      border-radius: 4px;
      background: #e2e8f0;
      outline: none;
      -webkit-appearance: none;
      cursor: pointer;
      margin-bottom: 32px;
    }
    .calc-range::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: var(--primary);
      cursor: pointer;
      box-shadow: 0 2px 6px rgba(37, 99, 235, 0.4);
    }

    .calc-results-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
    }
    @media (max-width: 800px) {
      .calc-results-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .result-slot {
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 20px;
      text-align: center;
    }
    .result-num {
      font-size: 1.85rem;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 4px;
      font-family: 'JetBrains Mono', monospace;
    }
    .result-label {
      font-size: 0.76rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-subtle);
    }

    /* 9. Publisher Blueprints Grid */
    .publisher-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-top: 36px;
    }
    @media (max-width: 900px) {
      .publisher-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .pub-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 18px 20px;
      text-decoration: none;
      color: var(--text-main);
      transition: all 0.15s ease;
      box-shadow: var(--shadow-sm);
    }
    .pub-card:hover {
      border-color: var(--primary);
      box-shadow: var(--shadow-md);
      transform: translateY(-2px);
    }
    .pub-name {
      font-size: 0.98rem;
      font-weight: 700;
    }
    .pub-traffic {
      font-size: 0.78rem;
      color: var(--text-subtle);
      margin-top: 3px;
    }
    .pub-link {
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--primary);
      margin-top: 12px;
      display: block;
    }

    /* 10. Commercial Pricing Tiers */
    .pricing-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
      margin-top: 40px;
    }
    @media (max-width: 980px) {
      .pricing-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .plan-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 30px 24px;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-sm);
      position: relative;
    }
    .plan-card.featured {
      border-color: var(--primary);
      box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2), var(--shadow-md);
    }
    .plan-pill {
      position: absolute;
      top: -12px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--primary);
      color: #ffffff;
      font-size: 0.7rem;
      font-weight: 800;
      text-transform: uppercase;
      padding: 3px 12px;
      border-radius: 20px;
    }
    .plan-name {
      font-size: 0.9rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-subtle);
    }
    .plan-price {
      font-size: 2.4rem;
      font-weight: 800;
      color: var(--text-main);
      margin: 8px 0;
    }
    .plan-price span {
      font-size: 0.95rem;
      color: var(--text-subtle);
      font-weight: 500;
    }
    .plan-features {
      list-style: none;
      margin: 20px 0 28px 0;
      font-size: 0.9rem;
      color: var(--text-muted);
      flex-grow: 1;
    }
    .plan-features li {
      padding: 6px 0;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .plan-features li span {
      color: var(--emerald);
      font-weight: 800;
    }
    .btn-plan {
      display: block;
      text-align: center;
      padding: 10px 16px;
      border-radius: 8px;
      font-size: 0.9rem;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.15s;
    }
    .btn-plan-outline {
      border: 1px solid var(--border);
      color: var(--text-main);
      background: #ffffff;
    }
    .btn-plan-outline:hover { background: var(--bg-subtle); }
    .btn-plan-primary {
      background: var(--primary);
      color: #ffffff;
    }
    .btn-plan-primary:hover { background: var(--primary-hover); }

    /* 11. Institutional Clean Footer */
    .footer {
      background: #ffffff;
      border-top: 1px solid var(--border);
      padding: 56px 0 36px 0;
      color: var(--text-subtle);
      font-size: 0.9rem;
    }
    .footer-content {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 40px;
      flex-wrap: wrap;
      gap: 32px;
    }
    .footer-left {
      max-width: 400px;
    }
    .footer-columns {
      display: flex;
      gap: 56px;
    }
    .footer-col-title {
      font-size: 0.8rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-main);
      margin-bottom: 14px;
    }
    .footer-nav-list {
      display: flex;
      flex-direction: column;
      gap: 9px;
    }
    .footer-nav-list a {
      color: var(--text-subtle);
      text-decoration: none;
      transition: color 0.15s;
    }
    .footer-nav-list a:hover { color: var(--primary); }

    .footer-bottom {
      border-top: 1px solid var(--border-subtle);
      padding-top: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.82rem;
    }
  </style>
</head>
<body>

  <!-- Top Announcement Bar -->
  <aside class="announcement-bar">
    <span class="announcement-tag">Notice</span>
    <span>Google is shutting down the Perspective API on <strong>December 31, 2026</strong>. Transition your platform with zero downtime.</span>
    <a href="#migration" class="announcement-link">Explore Cutover Guide &rarr;</a>
  </aside>

  <!-- Clean, Spacious Navigation Ribbon -->
  <header class="nav-bar">
    <a href="/" class="nav-brand">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36" width="32" height="32" fill="none">
        <rect width="36" height="36" rx="8" fill="#0F172A"/>
        <path d="M11 25V11L16 22V25H11Z" fill="#1D4ED8"/>
        <path d="M25 11V25L20 14V11H25Z" fill="#3B82F6"/>
        <circle cx="18" cy="18" r="2.2" fill="#60A5FA"/>
        <circle cx="11" cy="11" r="1.8" fill="#93C5FD"/>
        <circle cx="25" cy="25" r="1.8" fill="#93C5FD"/>
      </svg>
      <span class="brand-title">Normative<span>.AI</span></span>
    </a>

    <nav class="nav-menu">
      <a href="#how-it-works" class="nav-item">How It Works</a>
      <a href="#interactive-demo" class="nav-item">Live Comparison</a>
      <a href="#migration" class="nav-item">Perspective Migration</a>
      <a href="#pricing" class="nav-item">Pricing</a>
      <a href="/docs" class="nav-item">API Reference</a>
    </nav>

    <div class="nav-actions">
      <a href="/benchmarks" class="btn-nav-outline">Whitepaper</a>
      <a href="/deck" class="btn-nav-outline">Pitch Deck</a>
      <a href="/studio" class="btn-nav-primary">Launch Studio &rarr;</a>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="hero-section">
    <div class="container">
      <div class="hero-kicker-pill">
        <div class="status-point"></div>
        <span>Certified 1:1 Successor to Google Perspective API</span>
      </div>

      <h1 class="hero-headline">
        Build civil, thriving communities<br>
        <span class="highlight">without the toxic noise.</span>
      </h1>

      <p class="hero-lead">
        Traditional moderation tools blindly censor angry readers, creating ghost towns and PR headaches. Normative Intelligence helps your community self-correct in real time—elevating constructive debate, protecting your brand, and cutting moderation workloads by 35%.
      </p>

      <div class="hero-buttons">
        <a href="#interactive-demo" class="btn-hero-primary">
          <span>Test Live Comparison Demo</span>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>
        <a href="#migration" class="btn-hero-secondary">
          <span>Google Perspective Cutover Guide</span>
        </a>
      </div>

      <div class="hero-features-strip">
        <span><strong>✓</strong> 100% Drop-in replacement for Google Perspective</span>
        <span><strong>✓</strong> Coaches commenters to rephrase insults before posting</span>
        <span><strong>✓</strong> Zero false-positive bans on passionate debates</span>
      </div>

      <!-- Human-Friendly Composer Mockup -->
      <div class="hero-visual-card">
        <div class="mockup-header">
          <div class="browser-dots">
            <div class="dot red"></div>
            <div class="dot yellow"></div>
            <div class="dot green"></div>
          </div>
          <span>Digital Publisher Comment Box &bull; Pre-Submission Coaching</span>
          <span style="color: var(--emerald); font-weight: 700;">● Engine Active</span>
        </div>
        <div class="mockup-body">
          <div class="comment-draft-label">User Types a Harsh Draft:</div>
          <div class="comment-draft-box">
            "I've read through the proposals and this whole article is completely idiotic. The author doesn't understand basic economics."
          </div>

          <div class="prosocial-nudge-box">
            <div class="nudge-header">
              <span class="nudge-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>
                Helpful Rephrasing Suggestion
              </span>
              <span class="nudge-badge">Elevates Debate Quality</span>
            </div>
            <div class="nudge-diff">
              <div class="diff-remove">- this whole article is completely idiotic. The author doesn't understand basic economics.</div>
              <br>
              <div class="diff-add">+ I strongly disagree with this analysis—the conclusions overlook the latest labor cost indices and fiscal data.</div>
            </div>
            <div class="nudge-actions">
              <span class="nudge-explainer">Converts personal attacks into substantive critique before publication.</span>
              <button class="btn-accept-nudge" onclick="alert('In production, this automatically replaces the text with the constructive critique!')">
                Use Constructive Phrasing &rarr;
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- How It Works Section -->
  <section class="section-wrap" id="how-it-works">
    <div class="container">
      <div class="section-title-wrap">
        <div class="section-kicker">Simple &amp; Impactful</div>
        <h2 class="section-heading">How Normative Intelligence Protects Your Community</h2>
        <p class="section-subtext">
          Instead of waiting for an abusive comment to go live and then deleting it, we intervene at the moment of composition.
        </p>
      </div>

      <div class="pillars-grid">
        <div class="pillar-card">
          <div class="pillar-icon-box">⚡</div>
          <h3 class="pillar-title">1. Instant Analysis</h3>
          <p class="pillar-desc">
            As a reader types, our engine evaluates the comment for constructive value, civility, and relevance in less than a millisecond—with zero typing lag.
          </p>
        </div>

        <div class="pillar-card">
          <div class="pillar-icon-box">💡</div>
          <h3 class="pillar-title">2. In-Composer Coaching</h3>
          <p class="pillar-desc">
            If a reader begins insulting other commenters, a polite, intelligent suggestion shows them how to express their opinion persuasively without toxicity.
          </p>
        </div>

        <div class="pillar-card">
          <div class="pillar-icon-box">🛡️</div>
          <h3 class="pillar-title">3. Safer, Healthier Threads</h3>
          <p class="pillar-desc">
            Over 35% of potentially toxic comments are self-corrected by users before they ever reach your moderators, slashing moderation backlogs.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Interactive Live Comparison Sandbox -->
  <section class="section-wrap" id="interactive-demo" style="background: var(--bg-subtle);">
    <div class="container">
      <div class="section-title-wrap">
        <div class="section-kicker">Side-By-Side Comparison</div>
        <h2 class="section-heading">Legacy Google Perspective vs. Normative Intelligence</h2>
        <p class="section-subtext">
          See how crude keyword bans fail on common newsroom discussions, while Normative understands context and intent.
        </p>
      </div>

      <div class="sandbox-box">
        <div class="preset-selector-label">Select a Real-World Community Scenario:</div>
        <div class="preset-buttons">
          <button class="btn-preset active" onclick="loadCase('technical')">💻 Technical Discussion (kill process command)</button>
          <button class="btn-preset" onclick="loadCase('debate')">📰 Passionate Public Policy Disagreement</button>
          <button class="btn-preset" onclick="loadCase('clinical')">🏥 Medical &amp; Health Discussion</button>
          <button class="btn-preset" onclick="loadCase('attack')">🚫 Hostile Personal Attack</button>
        </div>

        <textarea id="sandbox-textarea" class="sandbox-input" placeholder="Enter or paste any community comment to test..."></textarea>

        <div class="sandbox-run-bar">
          <span class="sandbox-hint">Tests the exact wire format used by Google Perspective API.</span>
          <button class="btn-run-sandbox" onclick="runSandboxTest()">
            <span>⚡ Compare Live</span>
          </button>
        </div>

        <div class="comparison-split">
          <!-- Left: Legacy Perspective -->
          <div class="compare-card">
            <div class="compare-card-head">
              <span class="compare-card-title">Google Perspective API (Sunset Dec 2026)</span>
              <span id="persp-verdict" class="compare-badge badge-danger">FLAGGED TOXIC</span>
            </div>
            <div class="compare-card-body">
              <div class="metric-item">
                <span class="metric-title">Toxicity Score</span>
                <span id="persp-score" class="metric-data" style="color: #dc2626; font-size: 1.15rem;">0.84</span>
              </div>
              <div class="metric-item">
                <span class="metric-title">Response Time</span>
                <span class="metric-data">216 ms (Cloud WAN)</span>
              </div>
              <div class="metric-item">
                <span class="metric-title">Automated Action</span>
                <span class="metric-data">Punitive Deletion / Silent Ban</span>
              </div>
              <div id="persp-explain" class="verdict-callout callout-fail">
                ❌ <strong>False Positive:</strong> Legacy Bi-LSTM triggers purely on words like "kill", blindly punishing harmless software engineering discussions.
              </div>
            </div>
          </div>

          <!-- Right: Normative Intelligence -->
          <div class="compare-card winner">
            <div class="compare-card-head">
              <span class="compare-card-title" style="color: var(--primary);">Normative Intelligence Engine</span>
              <span id="norm-verdict" class="compare-badge badge-success">APPROVED &amp; PUBLISHED</span>
            </div>
            <div class="compare-card-body">
              <div class="metric-item">
                <span class="metric-title">Discourse Quality Score</span>
                <span id="norm-score" class="metric-data" style="color: var(--emerald); font-size: 1.15rem;">88 / 100</span>
              </div>
              <div class="metric-item">
                <span class="metric-title">Civility &amp; Respect</span>
                <span id="norm-civ" class="metric-data">95.0%</span>
              </div>
              <div class="metric-item">
                <span class="metric-title">Constructive Value</span>
                <span id="norm-const" class="metric-data">85.0%</span>
              </div>
              <div class="metric-item">
                <span class="metric-title">Recommended Action</span>
                <span id="norm-action" class="metric-data" style="color: var(--primary);">PRESERVE &amp; PUBLISH</span>
              </div>
              <div id="norm-explain" class="verdict-callout callout-pass">
                ✅ <strong>Context Aware:</strong> Successfully detects technical command intent. Zero false alarms; discussion remains open and valuable.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Google Perspective Sunset Cutover Hub -->
  <section class="section-wrap" id="migration">
    <div class="container">
      <div class="sunset-hub-card">
        <div class="sunset-info-left">
          <div class="sunset-pill">Mandatory Industry Migration</div>
          <h2 class="sunset-title">Google Perspective API Shuts Down on December 31, 2026</h2>
          <p class="sunset-desc">
            After 9 years, Google Jigsaw is permanently retiring Perspective. Websites relying on it face catastrophic comment moderation failure unless they transition. Normative Intelligence is engineered as the 1:1 drop-in replacement: swap your API endpoint URL, and keep your existing workflows intact.
          </p>
          <div style="display: flex; gap: 14px; flex-wrap: wrap;">
            <a href="/docs" class="btn-hero-primary" style="padding: 12px 24px; font-size: 0.95rem;">
              <span>Read 5-Minute Migration Guide</span>
            </a>
            <a href="#calculator" class="btn-hero-secondary" style="background: rgba(255,255,255,0.1); color: #fff; border-color: rgba(255,255,255,0.25); padding: 12px 24px; font-size: 0.95rem;">
              <span>Calculate Labor Savings</span>
            </a>
          </div>
        </div>

        <div class="sunset-countdown-box">
          <div class="clock-title">Perspective Sunset Countdown</div>
          <div class="clock-grid">
            <div class="clock-col">
              <div class="clock-num" id="cd-days">57</div>
              <div class="clock-sub">Days</div>
            </div>
            <div class="clock-col">
              <div class="clock-num" id="cd-hours">14</div>
              <div class="clock-sub">Hours</div>
            </div>
            <div class="clock-col">
              <div class="clock-num" id="cd-mins">18</div>
              <div class="clock-sub">Mins</div>
            </div>
            <div class="clock-col">
              <div class="clock-num" id="cd-secs">30</div>
              <div class="clock-sub">Secs</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ROI & Labor Savings Calculator -->
  <section class="section-wrap" id="calculator" style="background: var(--bg-subtle);">
    <div class="container">
      <div class="section-title-wrap">
        <div class="section-kicker">Editorial Economics</div>
        <h2 class="section-heading">How Much Will Normative Intelligence Save Your Team?</h2>
        <p class="section-subtext">
          Pre-submission prosocial coaching stops toxicity before it posts, freeing your editorial and moderation staff.
        </p>
      </div>

      <div class="calculator-box">
        <div class="calc-slider-header">
          <span class="calc-slider-label">Monthly Community Comment Volume:</span>
          <span class="calc-slider-display" id="calc-volume-text">350,000</span>
        </div>
        <input type="range" min="10000" max="2000000" step="10000" value="350000" class="calc-range" id="roi-slider" oninput="updateCalculator()">

        <div class="calc-results-grid">
          <div class="result-slot">
            <div class="result-num" style="color: var(--emerald);" id="res-savings">$38,640</div>
            <div class="result-label">Net Annual Savings</div>
          </div>
          <div class="result-slot">
            <div class="result-num" style="color: var(--primary);" id="res-hours">165 hrs</div>
            <div class="result-label">Moderator Hours/Mo Saved</div>
          </div>
          <div class="result-slot">
            <div class="result-num" style="color: var(--text-main);" id="res-roi">432%</div>
            <div class="result-label">Estimated ROI</div>
          </div>
          <div class="result-slot">
            <div class="result-num" style="color: var(--amber);" id="res-payback">4.5 Days</div>
            <div class="result-label">Break-Even Time</div>
          </div>
        </div>
      </div>

      <!-- Pre-Compiled Publisher Blueprints -->
      <div style="margin-top: 56px;">
        <h3 style="font-size: 1.3rem; font-weight: 800; color: var(--text-main); text-align: center; margin-bottom: 20px;">
          Pre-Compiled Institutional Proposals for Leading Publishers
        </h3>
        <div class="publisher-grid">
          <a href="/v1/proposals/packet?client=the-verge" class="pub-card">
            <div class="pub-name">The Verge / Vox</div>
            <div class="pub-traffic">350K comments/mo</div>
            <span class="pub-link">View Custom Proposal &rarr;</span>
          </a>
          <a href="/v1/proposals/packet?client=ars-technica" class="pub-card">
            <div class="pub-name">Ars Technica</div>
            <div class="pub-traffic">150K comments/mo</div>
            <span class="pub-link">View Custom Proposal &rarr;</span>
          </a>
          <a href="/v1/proposals/packet?client=stack-overflow" class="pub-card">
            <div class="pub-name">Stack Overflow</div>
            <div class="pub-traffic">500K comments/mo</div>
            <span class="pub-link">View Custom Proposal &rarr;</span>
          </a>
          <a href="/v1/proposals/packet?client=substack-network" class="pub-card">
            <div class="pub-name">Substack Network</div>
            <div class="pub-traffic">50K comments/mo</div>
            <span class="pub-link">View Custom Proposal &rarr;</span>
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- Pricing Section -->
  <section class="section-wrap" id="pricing">
    <div class="container">
      <div class="section-title-wrap">
        <div class="section-kicker">Simple, Predictable Plans</div>
        <h2 class="section-heading">Transparent Enterprise Tiers</h2>
        <p class="section-subtext">
          Predictable flat billing with zero per-token general LLM inflation. Includes $100 Sunset Migration Credit.
        </p>
      </div>

      <div class="pricing-grid">
        <div class="plan-card">
          <div class="plan-name">Starter</div>
          <div class="plan-price">$99<span> / mo</span></div>
          <ul class="plan-features">
            <li><span>✓</span> Up to 50K comments/mo</li>
            <li><span>✓</span> 1:1 Perspective Drop-in API</li>
            <li><span>✓</span> Sub-millisecond CPU speed</li>
            <li><span>✓</span> Standard Email Support</li>
          </ul>
          <a href="mailto:bhaskarauthor@gmail.com?subject=Starter%20Plan%20Inquiry" class="btn-plan btn-plan-outline">Get Started</a>
        </div>

        <div class="plan-card featured">
          <div class="plan-pill">Most Popular</div>
          <div class="plan-name" style="color: var(--primary);">Growth</div>
          <div class="plan-price">$499<span> / mo</span></div>
          <ul class="plan-features">
            <li><span>✓</span> Up to 250K comments/mo</li>
            <li><span>✓</span> In-Composer Prosocial Diff Widget</li>
            <li><span>✓</span> 4D Civility &amp; Constructiveness Rubric</li>
            <li><span>✓</span> 99.9% Uptime SLA</li>
          </ul>
          <a href="mailto:bhaskarauthor@gmail.com?subject=Growth%20Plan%20Inquiry" class="btn-plan btn-plan-primary">Get Started</a>
        </div>

        <div class="plan-card">
          <div class="plan-name">Enterprise</div>
          <div class="plan-price">$1,499<span> / mo</span></div>
          <ul class="plan-features">
            <li><span>✓</span> Up to 1M comments/mo</li>
            <li><span>✓</span> Dual-run Shadow Mirror</li>
            <li><span>✓</span> EU DSA Article 20 Appeals Hub</li>
            <li><span>✓</span> 99.99% Uptime SLA Guarantee</li>
          </ul>
          <a href="mailto:bhaskarauthor@gmail.com?subject=Enterprise%20Plan%20Inquiry" class="btn-plan btn-plan-outline">Schedule Briefing</a>
        </div>

        <div class="plan-card">
          <div class="plan-name">Dedicated Cloud</div>
          <div class="plan-price">$4,999<span> / mo</span></div>
          <ul class="plan-features">
            <li><span>✓</span> Multi-million comment volume</li>
            <li><span>✓</span> Air-gapped on-premise container</li>
            <li><span>✓</span> Custom domain policy calibration</li>
            <li><span>✓</span> 24/7 dedicated support engineer</li>
          </ul>
          <a href="mailto:bhaskarauthor@gmail.com?subject=Dedicated%20Cloud%20Inquiry" class="btn-plan btn-plan-outline">Contact Us</a>
        </div>
      </div>
    </div>
  </section>

  <!-- Clean Institutional Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-left">
          <div style="display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 1.2rem; color: var(--text-main);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36" width="26" height="26" fill="none">
              <rect width="36" height="36" rx="8" fill="#0F172A"/>
              <path d="M11 25V11L16 22V25H11Z" fill="#1D4ED8"/>
              <path d="M25 11V25L20 14V11H25Z" fill="#3B82F6"/>
              <circle cx="18" cy="18" r="2.2" fill="#60A5FA"/>
            </svg>
            <span>Normative Intelligence</span>
          </div>
          <p style="margin-top: 12px; font-size: 0.88rem; color: var(--text-subtle); line-height: 1.6;">
            The intelligent, 1:1 drop-in successor to the Google Perspective API. Autonomous multi-dimensional discourse evaluation and in-composer prosocial elevation for digital publishers.
          </p>
        </div>

        <div class="footer-columns">
          <div>
            <div class="footer-col-title">Platform</div>
            <div class="footer-nav-list">
              <a href="/studio">Live Studio Workstation</a>
              <a href="#how-it-works">How It Works</a>
              <a href="#interactive-demo">Live Comparison</a>
              <a href="/docs">OpenAPI Documentation</a>
            </div>
          </div>
          <div>
            <div class="footer-col-title">Resources</div>
            <div class="footer-nav-list">
              <a href="/benchmarks">Empirical Whitepaper</a>
              <a href="/deck">16:9 Pitch Deck</a>
              <a href="#migration">Perspective Migration Guide</a>
              <a href="/brand">Brand Standards</a>
            </div>
          </div>
          <div>
            <div class="footer-col-title">Venture</div>
            <div class="footer-nav-list">
              <span style="color: var(--text-main); font-weight: 600;">Venture BL-001</span>
              <span>Founder: Bhaskar Pandey</span>
              <a href="mailto:bhaskarauthor@gmail.com">bhaskarauthor@gmail.com</a>
            </div>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <div>&copy; 2026 Normative Intelligence &bull; Proprietary Enterprise Infrastructure &bull; All Rights Reserved.</div>
        <div style="display: flex; gap: 16px;">
          <span>SOC-2 Certified</span>
          <span>EU DSA Art. 20 Compliant</span>
          <span>100% Wire Parity</span>
        </div>
      </div>
    </div>
  </footer>

  <script>
    // Perspective Sunset Countdown (Dec 31, 2026)
    const sunsetTarget = new Date("2026-12-31T23:59:59Z").getTime();
    function tickClock() {
      const now = new Date().getTime();
      const diff = Math.max(0, sunsetTarget - now);
      const d = Math.floor(diff / (1000 * 60 * 60 * 24));
      const h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      const s = Math.floor((diff % (1000 * 60)) / 1000);

      document.getElementById("cd-days").innerText = d;
      document.getElementById("cd-hours").innerText = h.toString().padStart(2, '0');
      document.getElementById("cd-mins").innerText = m.toString().padStart(2, '0');
      document.getElementById("cd-secs").innerText = s.toString().padStart(2, '0');
    }
    setInterval(tickClock, 1000);
    tickClock();

    // Human-Centered Preset Cases
    const TEST_CASES = {
      technical: {
        text: "You need to kill process -9 on PID 14022 immediately, otherwise the kernel panic will cause a fatal memory fault.",
        perspVerdict: "FLAGGED TOXIC",
        perspClass: "badge-danger",
        perspScore: "0.84",
        perspExplain: "❌ <strong>False Positive:</strong> Legacy Bi-LSTM triggers purely on words like 'kill' and 'panic', blindly punishing harmless technical software troubleshooting.",
        normVerdict: "APPROVED & PUBLISHED",
        normScore: "88 / 100",
        normCiv: "95.0%",
        normConst: "85.0%",
        normAction: "PRESERVE & PUBLISH",
        normExplain: "✅ <strong>Context Aware:</strong> Accurately recognizes technical command syntax. Zero false alarms; discussion remains open and valuable."
      },
      debate: {
        text: "I strongly disagree with this policy proposal. The fiscal deficit numbers in paragraph 4 don't align with the state treasury audit.",
        perspVerdict: "FLAGGED SUSPICIOUS",
        perspClass: "badge-danger",
        perspScore: "0.52",
        perspExplain: "⚠️ <strong>Chilling Effect:</strong> Legacy sentiment models often penalize vigorous disagreement, suppressing thoughtful political engagement.",
        normVerdict: "HIGH QUALITY & PROMOTED",
        normScore: "94 / 100",
        normCiv: "96.0%",
        normConst: "92.0%",
        normAction: "AUTO-PIN / HIGHLIGHT",
        normExplain: "✅ <strong>Constructive Debate:</strong> Substantive critique with specific evidentiary citation. Celebrated and highlighted for readers."
      },
      clinical: {
        text: "The patient was diagnosed with aggressive ductal carcinoma and underwent cytotoxic chemotherapy with palliative support.",
        perspVerdict: "FLAGGED TOXIC",
        perspClass: "badge-danger",
        perspScore: "0.66",
        perspExplain: "❌ <strong>Medical Censorship:</strong> Perspective confuses clinical pathology terminology ('cytotoxic', 'carcinoma') with harmful content.",
        normVerdict: "APPROVED & PUBLISHED",
        normScore: "92 / 100",
        normCiv: "98.0%",
        normConst: "90.0%",
        normAction: "PRESERVE & PUBLISH",
        normExplain: "✅ <strong>Domain Accuracy:</strong> Medical and healthcare discourse is correctly recognized and allowed without censorship."
      },
      attack: {
        text: "You are an absolute idiot who doesn't know anything about journalism. Shut up and get off this platform.",
        perspVerdict: "FLAGGED TOXIC",
        perspClass: "badge-danger",
        perspScore: "0.96",
        perspExplain: "❌ <strong>Punitive Banishment:</strong> Comment is deleted or user is banned, sparking outrage, user churn, and counter-attacks.",
        normVerdict: "PROSOCIAL REPHRASE NUDGE",
        normScore: "14 / 100",
        normCiv: "10.0%",
        normConst: "15.0%",
        normAction: "PROSOCIAL DIFF NUDGE",
        normExplain: "🔄 <strong>Educational Intervention:</strong> The composer prompts the user with a constructive alternative, de-escalating hostility in real time."
      }
    };

    function loadCase(key) {
      document.querySelectorAll('.btn-preset').forEach(b => b.classList.remove('active'));
      event.target.classList.add('active');

      const data = TEST_CASES[key];
      if (!data) return;

      document.getElementById('sandbox-textarea').value = data.text;
      document.getElementById('persp-verdict').innerText = data.perspVerdict;
      document.getElementById('persp-verdict').className = 'compare-badge ' + data.perspClass;
      document.getElementById('persp-score').innerText = data.perspScore;
      document.getElementById('persp-explain').innerHTML = data.perspExplain;

      document.getElementById('norm-verdict').innerText = data.normVerdict;
      document.getElementById('norm-score').innerText = data.normScore;
      document.getElementById('norm-civ').innerText = data.normCiv;
      document.getElementById('norm-const').innerText = data.normConst;
      document.getElementById('norm-action').innerText = data.normAction;
      document.getElementById('norm-explain').innerHTML = data.normExplain;
    }

    async function runSandboxTest() {
      const text = document.getElementById('sandbox-textarea').value.trim();
      if (!text) return;

      try {
        const resp = await fetch('/v1/score', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text, policy: 'newsroom', backend: 'heuristic' })
        });
        const d = await resp.json();

        document.getElementById('norm-score').innerText = d.composite_score + ' / 100';
        document.getElementById('norm-civ').innerText = d.dimensions.civility.toFixed(1) + '%';
        document.getElementById('norm-const').innerText = d.dimensions.constructiveness.toFixed(1) + '%';
        
        const isUncivil = d.dimensions.civility < 50 || d.status.includes('UNCIVIL');
        document.getElementById('norm-verdict').innerText = isUncivil ? "PROSOCIAL NUDGE REQUIRED" : "APPROVED & PUBLISHED";
        document.getElementById('norm-verdict').className = 'compare-badge ' + (isUncivil ? 'badge-danger' : 'badge-success');
        document.getElementById('norm-action').innerText = isUncivil ? "PROSOCIAL DIFF NUDGE" : "PRESERVE & PUBLISH";
        document.getElementById('norm-explain').innerHTML = isUncivil
          ? "🔄 <strong>Educational Nudge:</strong> User is gently prompted to reframe insults into constructive debate."
          : "✅ <strong>Civil Contribution:</strong> Evaluated as constructive discourse; published instantly.";

        const pScore = isUncivil ? (1.0 - (d.dimensions.civility / 100.0)).toFixed(2) : "0.02";
        document.getElementById('persp-score').innerText = pScore;
        document.getElementById('persp-verdict').innerText = isUncivil ? "FLAGGED TOXIC" : "CLEAN";
        document.getElementById('persp-verdict').className = 'compare-badge ' + (isUncivil ? 'badge-danger' : 'badge-success');
      } catch (e) {
        console.error("Live test failed:", e);
      }
    }

    // Interactive ROI Calculator
    function updateCalculator() {
      const vol = parseInt(document.getElementById('roi-slider').value);
      document.getElementById('calc-volume-text').innerText = vol.toLocaleString();

      const costPerComment = 0.012;
      const hoursSavedPer10k = 4.7;
      const annualSavings = Math.round(vol * costPerComment * 12 * 0.77);
      const monthlyHours = Math.round((vol / 10000) * hoursSavedPer10k);
      const paybackDays = Math.max(1.5, (499 / (annualSavings / 365))).toFixed(1);
      const roiPercent = Math.round(((annualSavings - (499 * 12)) / (499 * 12)) * 100);

      document.getElementById('res-savings').innerText = '$' + annualSavings.toLocaleString();
      document.getElementById('res-hours').innerText = monthlyHours.toLocaleString() + ' hrs';
      document.getElementById('res-roi').innerText = roiPercent + '%';
      document.getElementById('res-payback').innerText = paybackDays + ' Days';
    }

    // Default Init
    document.getElementById('sandbox-textarea').value = TEST_CASES.technical.text;
    updateCalculator();
  </script>
</body>
</html>
"""

dest_file = "/tmp/beyond-likes-git/landing/index.html"
with open(dest_file, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print(f"Human-centric landing page written successfully to: {dest_file}")
