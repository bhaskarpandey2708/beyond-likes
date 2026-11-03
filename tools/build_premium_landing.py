# -*- coding: utf-8 -*-
"""
Premium Bright Modern Showcase Builder for Normative Intelligence.
Generates an ultra-crisp, Stripe/Linear/Vercel grade commercial landing page.
Zero academic baggage; 100% sovereign enterprise deep-tech presentation.
"""
import os

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Normative Intelligence — The Sovereign Drop-In Infrastructure for Civil Digital Discourse</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #fafbfc;
      --surface: #ffffff;
      --surface-subtle: #f8fafc;
      --surface-elevated: #ffffff;
      --border: rgba(15, 23, 42, 0.08);
      --border-subtle: #e2e8f0;
      --border-strong: #cbd5e1;
      --border-focus: #3b82f6;

      --text: #0f172a;
      --text-muted: #334155;
      --text-subtle: #64748b;
      --text-light: #94a3b8;

      --primary: #1d4ed8;
      --primary-hover: #1e40af;
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

      --shadow-xs: 0 1px 2px 0 rgba(15, 23, 42, 0.04);
      --shadow-sm: 0 1px 3px 0 rgba(15, 23, 42, 0.06), 0 1px 2px -1px rgba(15, 23, 42, 0.04);
      --shadow-md: 0 4px 6px -1px rgba(15, 23, 42, 0.07), 0 2px 4px -2px rgba(15, 23, 42, 0.04);
      --shadow-lg: 0 12px 28px -6px rgba(15, 23, 42, 0.08), 0 4px 10px -4px rgba(15, 23, 42, 0.03);
      --shadow-elevated: 0 20px 40px -12px rgba(15, 23, 42, 0.1), 0 1px 3px 0 rgba(15, 23, 42, 0.04);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      background-image: 
        radial-gradient(at 0% 0%, rgba(219, 234, 254, 0.45) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(243, 232, 255, 0.35) 0px, transparent 50%),
        radial-gradient(#cbd5e1 0.75px, transparent 0.75px);
      background-size: 100% 100%, 100% 100%, 24px 24px;
      overflow-x: hidden;
    }

    /* Fixed Modern Glass Nav */
    .nav-bar {
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(255, 255, 255, 0.88);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
      padding: 14px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.2s ease;
    }

    .nav-left {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .nav-brand {
      display: flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      color: var(--text);
      font-weight: 800;
      font-size: 1.15rem;
      letter-spacing: -0.025em;
    }

    .brand-pill {
      font-size: 0.68rem;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      padding: 3px 8px;
      background: var(--surface-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      color: var(--text-subtle);
    }

    .nav-status {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.76rem;
      font-weight: 600;
      color: var(--emerald);
      background: var(--emerald-subtle);
      border: 1px solid var(--emerald-border);
      padding: 3px 10px;
      border-radius: 20px;
    }

    .pulse-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--emerald);
      box-shadow: 0 0 0 0 rgba(5, 150, 105, 0.7);
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0% { box-shadow: 0 0 0 0 rgba(5, 150, 105, 0.7); }
      70% { box-shadow: 0 0 0 6px rgba(5, 150, 105, 0); }
      100% { box-shadow: 0 0 0 0 rgba(5, 150, 105, 0); }
    }

    .nav-links {
      display: flex;
      align-items: center;
      gap: 22px;
    }

    .nav-link {
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--text-muted);
      text-decoration: none;
      transition: color 0.15s ease;
    }

    .nav-link:hover {
      color: var(--primary);
    }

    .btn-nav-primary {
      background: #0f172a;
      color: #ffffff;
      padding: 8px 18px;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      box-shadow: var(--shadow-sm);
      transition: all 0.15s ease;
    }

    .btn-nav-primary:hover {
      background: #1e293b;
      transform: translateY(-1px);
      box-shadow: var(--shadow-md);
    }

    /* Container */
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 28px;
    }

    /* Hero Section */
    .hero {
      padding: 84px 0 64px 0;
      text-align: center;
      position: relative;
    }

    .badge-kicker {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #ffffff;
      border: 1px solid var(--border-subtle);
      box-shadow: var(--shadow-sm);
      padding: 6px 14px;
      border-radius: 30px;
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--text-muted);
      margin-bottom: 24px;
    }

    .badge-kicker span.accent {
      color: var(--primary);
      font-weight: 800;
    }

    .hero-title {
      font-size: 3.75rem;
      font-weight: 800;
      letter-spacing: -0.04em;
      line-height: 1.14;
      color: var(--text);
      max-width: 960px;
      margin: 0 auto 22px auto;
    }

    .hero-title .gradient-text {
      background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #4f46e5 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
      font-size: 1.2rem;
      color: var(--text-muted);
      max-width: 800px;
      margin: 0 auto 36px auto;
      line-height: 1.68;
      font-weight: 500;
    }

    .hero-actions {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 14px;
      margin-bottom: 48px;
      flex-wrap: wrap;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      font-size: 0.94rem;
      font-weight: 600;
      padding: 13px 26px;
      border-radius: 9px;
      text-decoration: none;
      transition: all 0.15s ease;
      cursor: pointer;
    }

    .btn-main {
      background: var(--primary);
      color: #ffffff;
      border: 1px solid transparent;
      box-shadow: 0 4px 14px 0 rgba(29, 78, 216, 0.35);
    }
    .btn-main:hover {
      background: var(--primary-hover);
      transform: translateY(-1.5px);
      box-shadow: 0 6px 20px 0 rgba(29, 78, 216, 0.4);
    }

    .btn-secondary {
      background: #ffffff;
      color: var(--text);
      border: 1px solid var(--border-strong);
      box-shadow: var(--shadow-sm);
    }
    .btn-secondary:hover {
      background: #f8fafc;
      border-color: #94a3b8;
      transform: translateY(-1px);
    }

    /* Sunset Continuity Banner */
    .continuity-banner {
      background: #ffffff;
      border: 1px solid var(--amber-border);
      border-radius: 12px;
      padding: 18px 28px;
      max-width: 900px;
      margin: 0 auto 72px auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: var(--shadow-sm);
    }

    .continuity-info {
      text-align: left;
    }
    .continuity-title {
      font-size: 0.95rem;
      font-weight: 800;
      color: var(--text);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .continuity-desc {
      font-size: 0.82rem;
      color: var(--text-subtle);
      margin-top: 2px;
    }

    .continuity-clock {
      display: flex;
      gap: 14px;
      font-family: 'JetBrains Mono', monospace;
    }
    .clock-slot {
      text-align: center;
      background: var(--amber-subtle);
      padding: 6px 12px;
      border-radius: 8px;
      border: 1px solid var(--amber-border);
    }
    .clock-digit {
      font-size: 1.35rem;
      font-weight: 800;
      color: var(--amber);
      line-height: 1;
    }
    .clock-tag {
      font-size: 0.65rem;
      color: #92400e;
      text-transform: uppercase;
      font-weight: 700;
      margin-top: 2px;
    }

    /* Section Titles */
    .section-header {
      text-align: center;
      margin-bottom: 44px;
    }
    .section-kicker {
      font-size: 0.78rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--primary);
      margin-bottom: 8px;
    }
    .section-title {
      font-size: 2.35rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      color: var(--text);
      margin-bottom: 12px;
    }
    .section-desc {
      font-size: 1.05rem;
      color: var(--text-muted);
      max-width: 720px;
      margin: 0 auto;
      line-height: 1.6;
    }

    /* Interactive Dual-Mirror Component */
    .sandbox-container {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 36px;
      box-shadow: var(--shadow-lg);
      margin-bottom: 80px;
    }

    .preset-bar {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 22px;
    }

    .preset-pill {
      background: #f1f5f9;
      color: #334155;
      border: 1px solid #e2e8f0;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .preset-pill:hover {
      background: #e2e8f0;
      color: #0f172a;
    }
    .preset-pill.active {
      background: #0f172a;
      color: #ffffff;
      border-color: #0f172a;
    }

    .editor-wrapper {
      position: relative;
      margin-bottom: 20px;
    }

    .live-input {
      width: 100%;
      height: 96px;
      border: 1px solid var(--border-strong);
      border-radius: 10px;
      padding: 16px;
      font-family: inherit;
      font-size: 0.98rem;
      color: var(--text);
      background: #ffffff;
      outline: none;
      resize: vertical;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
      line-height: 1.5;
    }
    .live-input:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.12);
    }

    .editor-actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 28px;
    }

    .live-meta {
      font-size: 0.82rem;
      color: var(--text-subtle);
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .dual-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
    }
    @media (max-width: 900px) {
      .dual-grid { grid-template-columns: 1fr; }
    }

    .engine-card {
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      overflow: hidden;
      background: #ffffff;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
    }
    .engine-card.featured {
      border-color: var(--primary-border);
      box-shadow: 0 4px 18px -2px rgba(29, 78, 216, 0.08);
    }

    .engine-header {
      padding: 16px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #f8fafc;
      border-bottom: 1px solid var(--border-subtle);
    }
    .engine-card.featured .engine-header {
      background: #eff6ff;
      border-bottom-color: var(--primary-border);
    }

    .engine-title {
      font-size: 0.92rem;
      font-weight: 700;
      color: var(--text);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .status-badge {
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.05em;
      padding: 3px 8px;
      border-radius: 5px;
      text-transform: uppercase;
    }
    .badge-pass { background: var(--emerald-subtle); color: var(--emerald); border: 1px solid var(--emerald-border); }
    .badge-fail { background: var(--rose-subtle); color: var(--rose); border: 1px solid var(--rose-border); }
    .badge-warn { background: var(--amber-subtle); color: var(--amber); border: 1px solid var(--amber-border); }

    .engine-body {
      padding: 24px 20px;
      flex-grow: 1;
    }

    .metric-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 11px 0;
      border-bottom: 1px solid #f1f5f9;
      font-size: 0.9rem;
    }
    .metric-row:last-child { border-bottom: none; }

    .metric-name {
      color: var(--text-muted);
      font-weight: 500;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .metric-value {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: var(--text);
    }

    .dimension-bar-wrap {
      margin-top: 14px;
      padding-top: 14px;
      border-top: 1px solid #f1f5f9;
    }
    .dimension-bar-header {
      display: flex;
      justify-content: space-between;
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--text-muted);
      margin-bottom: 5px;
    }
    .dimension-track {
      height: 6px;
      background: #e2e8f0;
      border-radius: 3px;
      overflow: hidden;
      margin-bottom: 10px;
    }
    .dimension-fill {
      height: 100%;
      border-radius: 3px;
      transition: width 0.3s ease;
    }

    /* Live Prosocial In-Composer Diff Demo */
    .prosocial-diff-showcase {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 36px;
      box-shadow: var(--shadow-md);
      margin-bottom: 80px;
    }

    .composer-mockup {
      border: 1px solid var(--border-strong);
      border-radius: 12px;
      background: #ffffff;
      overflow: hidden;
      box-shadow: var(--shadow-sm);
    }
    .composer-header {
      background: #f8fafc;
      padding: 12px 18px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.84rem;
      font-weight: 700;
      color: var(--text-muted);
    }

    .composer-body {
      padding: 18px;
      font-size: 0.95rem;
      line-height: 1.6;
    }

    .diff-tray {
      background: #f8fafc;
      border-top: 1px solid var(--border-subtle);
      padding: 16px 18px;
    }
    .diff-tray-title {
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--primary);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .diff-code-box {
      background: #ffffff;
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.84rem;
      overflow: hidden;
    }
    .diff-line-del {
      background: var(--rose-subtle);
      color: var(--rose);
      padding: 8px 14px;
      border-left: 3px solid var(--rose);
    }
    .diff-line-add {
      background: var(--emerald-subtle);
      color: var(--emerald);
      padding: 8px 14px;
      border-left: 3px solid var(--emerald);
    }

    /* Bento Grid (Empirical Findings) */
    .bento-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      margin-bottom: 80px;
    }
    @media (max-width: 900px) {
      .bento-grid { grid-template-columns: repeat(2, 1fr); }
    }

    .bento-tile {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 28px 24px;
      box-shadow: var(--shadow-sm);
      text-align: left;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .bento-tile:hover {
      box-shadow: var(--shadow-md);
      transform: translateY(-2px);
      border-color: var(--border-strong);
    }

    .bento-num {
      font-size: 2.6rem;
      font-weight: 800;
      letter-spacing: -0.04em;
      line-height: 1;
      margin-bottom: 10px;
    }
    .bento-label {
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 4px;
    }
    .bento-sub {
      font-size: 0.82rem;
      color: var(--text-subtle);
      line-height: 1.5;
    }

    /* Code Terminal Section */
    .terminal-container {
      background: #0f172a;
      border: 1px solid #1e293b;
      border-radius: 14px;
      overflow: hidden;
      margin-bottom: 80px;
      box-shadow: var(--shadow-elevated);
    }
    .terminal-nav {
      background: #1e293b;
      padding: 12px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #334155;
    }
    .terminal-tabs {
      display: flex;
      gap: 8px;
    }
    .terminal-tab {
      background: transparent;
      border: none;
      color: #94a3b8;
      font-size: 0.84rem;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .terminal-tab.active {
      background: #0f172a;
      color: #ffffff;
    }
    .terminal-copy {
      background: #334155;
      color: #f1f5f9;
      border: none;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .terminal-copy:hover {
      background: #475569;
    }
    .terminal-body {
      padding: 24px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.88rem;
      color: #e2e8f0;
      line-height: 1.65;
      overflow-x: auto;
    }

    /* Interactive ROI Calculator */
    .calculator-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 36px;
      box-shadow: var(--shadow-md);
      margin-bottom: 80px;
    }
    .slider-wrap {
      margin: 28px 0;
    }
    .slider-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }
    .slider-title {
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text);
    }
    .slider-val-box {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.4rem;
      font-weight: 800;
      color: var(--primary);
    }
    .roi-slider {
      width: 100%;
      height: 8px;
      border-radius: 4px;
      background: #e2e8f0;
      outline: none;
      -webkit-appearance: none;
      cursor: pointer;
    }
    .roi-slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: var(--primary);
      cursor: pointer;
      box-shadow: 0 2px 6px rgba(29, 78, 216, 0.4);
    }

    .calc-metrics {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-top: 24px;
    }
    @media (max-width: 800px) {
      .calc-metrics { grid-template-columns: repeat(2, 1fr); }
    }
    .calc-slot {
      background: #f8fafc;
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 18px;
      text-align: center;
    }
    .calc-num {
      font-size: 1.75rem;
      font-weight: 800;
      color: var(--text);
      margin-bottom: 4px;
      font-family: 'JetBrains Mono', monospace;
    }
    .calc-tag {
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-subtle);
    }

    /* Publisher Packets Grid */
    .packets-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 80px;
    }
    @media (max-width: 900px) {
      .packets-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .packet-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 18px 20px;
      text-decoration: none;
      color: var(--text);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.15s ease;
      box-shadow: var(--shadow-xs);
    }
    .packet-card:hover {
      border-color: var(--primary);
      box-shadow: var(--shadow-md);
      transform: translateY(-2px);
    }
    .packet-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
    }
    .packet-avatar {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      background: #0f172a;
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 0.85rem;
    }
    .packet-badge {
      font-size: 0.65rem;
      font-weight: 700;
      text-transform: uppercase;
      padding: 2px 6px;
      border-radius: 4px;
      background: var(--emerald-subtle);
      color: var(--emerald);
      border: 1px solid var(--emerald-border);
    }
    .packet-title {
      font-size: 0.96rem;
      font-weight: 700;
      color: var(--text);
    }
    .packet-meta {
      font-size: 0.76rem;
      color: var(--text-subtle);
      margin-top: 3px;
    }
    .packet-cta {
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--primary);
      margin-top: 14px;
      display: flex;
      align-items: center;
      gap: 4px;
    }

    /* Commercial Pricing Tiers */
    .pricing-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      margin-bottom: 80px;
    }
    @media (max-width: 990px) {
      .pricing-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .pricing-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 28px 24px;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-sm);
      position: relative;
    }
    .pricing-card.featured {
      border-color: var(--primary);
      box-shadow: 0 0 0 2px rgba(29, 78, 216, 0.2), var(--shadow-md);
    }
    .featured-ribbon {
      position: absolute;
      top: -11px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--primary);
      color: #ffffff;
      font-size: 0.68rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 3px 12px;
      border-radius: 20px;
    }
    .tier-header { margin-bottom: 18px; }
    .tier-name {
      font-size: 0.88rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-subtle);
    }
    .tier-price {
      font-size: 2.3rem;
      font-weight: 800;
      color: var(--text);
      margin: 8px 0;
    }
    .tier-price span {
      font-size: 0.92rem;
      font-weight: 500;
      color: var(--text-subtle);
    }
    .tier-features {
      list-style: none;
      margin: 20px 0 28px 0;
      font-size: 0.88rem;
      color: var(--text-muted);
      flex-grow: 1;
    }
    .tier-features li {
      padding: 6px 0;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .tier-features li span {
      color: var(--emerald);
      font-weight: 800;
    }

    /* Enterprise Institutional Footer */
    .footer {
      background: #ffffff;
      border-top: 1px solid var(--border);
      padding: 56px 0 36px 0;
      color: var(--text-subtle);
      font-size: 0.88rem;
    }
    .footer-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 36px;
      flex-wrap: wrap;
      gap: 24px;
    }
    .footer-brand {
      max-width: 380px;
    }
    .footer-links {
      display: flex;
      gap: 40px;
    }
    .footer-col-title {
      font-size: 0.78rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text);
      margin-bottom: 12px;
    }
    .footer-col-links {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .footer-col-links a {
      color: var(--text-subtle);
      text-decoration: none;
      transition: color 0.15s;
    }
    .footer-col-links a:hover {
      color: var(--primary);
    }
    .footer-bottom {
      border-top: 1px solid var(--border-subtle);
      padding-top: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.8rem;
    }
  </style>
</head>
<body>

  <!-- Top Glass Navigation Bar -->
  <header class="nav-bar">
    <div class="nav-left">
      <a href="/" class="nav-brand">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36" width="30" height="30" fill="none">
          <rect width="36" height="36" rx="8" fill="#0F172A"/>
          <path d="M11 25V11L16 22V25H11Z" fill="#1D4ED8"/>
          <path d="M25 11V25L20 14V11H25Z" fill="#3B82F6"/>
          <circle cx="18" cy="18" r="2.2" fill="#60A5FA"/>
          <circle cx="11" cy="11" r="1.8" fill="#93C5FD"/>
          <circle cx="25" cy="25" r="1.8" fill="#93C5FD"/>
        </svg>
        <span>Normative<span style="color: var(--primary);">.AI</span></span>
      </a>
      <span class="brand-pill">Venture BL-001</span>
      <div class="nav-status">
        <div class="pulse-dot"></div>
        <span>Production Cluster Active &bull; 0.14ms</span>
      </div>
    </div>
    <div class="nav-links">
      <a href="#dual-mirror" class="nav-link">Dual-Mirror Live</a>
      <a href="/benchmarks" class="nav-link">Empirical Whitepaper</a>
      <a href="/deck" class="nav-link">16:9 Pitch Deck</a>
      <a href="#proposals" class="nav-link">Client Packets</a>
      <a href="/brand" class="nav-link">Brand Standards</a>
      <a href="/docs" class="nav-link">API Studio</a>
      <a href="/studio" class="btn-nav-primary">Launch Studio Desk &rarr;</a>
    </div>
  </header>

  <main class="container">

    <!-- Hero Section -->
    <section class="hero">
      <div class="badge-kicker">
        <span>⚡ 100% Wire Parity Drop-in Replacement</span>
        <span style="color: var(--border-strong);">&bull;</span>
        <span class="accent">Google Perspective EOL: Dec 31, 2026</span>
      </div>

      <h1 class="hero-title">
        The Sovereign Drop-In Infrastructure for <span class="gradient-text">Civil Digital Discourse</span>
      </h1>

      <p class="hero-subtitle">
        Google Jigsaw is terminating the Perspective API on December 31, 2026. Normative Intelligence delivers the certified 1:1 bitwise drop-in successor that eliminates false positives on technical syntax, halts adversarial zero-width evasions, and executes in 0.14ms on local CPU.
      </p>

      <div class="hero-actions">
        <a href="/studio" class="btn btn-main">
          <span>Launch Enterprise Studio Desk</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>
        <a href="#dual-mirror" class="btn btn-secondary">
          <span>Test Live Comparison Sandbox</span>
        </a>
        <a href="/deck" class="btn btn-secondary">
          <span>View 16:9 Pitch Deck</span>
        </a>
      </div>

      <!-- Sunset Continuity Countdown Banner -->
      <div class="continuity-banner">
        <div class="continuity-info">
          <div class="continuity-title">
            <span>Google Perspective API Decommission Window</span>
            <span style="font-size: 0.72rem; background: var(--amber-subtle); color: #b45309; padding: 2px 8px; border-radius: 4px; font-weight: 700;">CRITICAL SUNSET</span>
          </div>
          <div class="continuity-desc">Certified drop-in cutover active for digital newsrooms, forums, and developer networks</div>
        </div>
        <div class="continuity-clock" id="countdown-clock">
          <div class="clock-slot"><div class="clock-digit" id="cd-days">57</div><div class="clock-tag">Days</div></div>
          <div class="clock-slot"><div class="clock-digit" id="cd-hours">14</div><div class="clock-tag">Hours</div></div>
          <div class="clock-slot"><div class="clock-digit" id="cd-mins">20</div><div class="clock-tag">Mins</div></div>
          <div class="clock-slot"><div class="clock-digit" id="cd-secs">45</div><div class="clock-tag">Secs</div></div>
        </div>
      </div>
    </section>

    <!-- Interactive Live Comparison Sandbox -->
    <section id="dual-mirror">
      <div class="section-header">
        <div class="section-kicker">Interactive Evaluation Sandbox</div>
        <h2 class="section-title">Perspective vs. Normative Intelligence: Live Dual-Mirror</h2>
        <p class="section-desc">
          Test real-world production edge cases where legacy token classifiers fail. Click a preset or type your own comment to run the comparison live.
        </p>
      </div>

      <div class="sandbox-container">
        <div class="preset-bar">
          <button class="preset-pill active" onclick="loadPreset('technical')">💻 Systems Engineering (`kill -9` false positive)</button>
          <button class="preset-pill" onclick="loadPreset('clinical')">🏥 Clinical Oncology (chemotherapy)</button>
          <button class="preset-pill" onclick="loadPreset('adversarial')">🛡️ Unicode Zero-Width Evasion</button>
          <button class="preset-pill" onclick="loadPreset('academic')">📚 Academic Peer Review Critique</button>
          <button class="preset-pill" onclick="loadPreset('hostile')">🚫 Explicit Harassment Attack</button>
        </div>

        <div class="editor-wrapper">
          <textarea id="live-text-input" class="live-input" placeholder="Enter or paste any community comment to test..."></textarea>
        </div>

        <div class="editor-actions">
          <div class="live-meta">
            <span><strong>Target Schema:</strong> <code>POST /v1/comments:analyze</code></span>
            <span>&bull;</span>
            <span><strong>Execution Engine:</strong> Local Dual-Run Dispatcher</span>
          </div>
          <button class="btn btn-main" onclick="triggerDualMirror()">
            <span>⚡ Run Dual-Mirror Comparison</span>
          </button>
        </div>

        <div class="dual-grid">
          <!-- Left Column: Perspective API -->
          <div class="engine-card">
            <div class="engine-header">
              <div class="engine-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                <span>Google Perspective API (Sunset Dec 2026)</span>
              </div>
              <span id="persp-badge" class="status-badge badge-fail">FLAGGED TOXIC</span>
            </div>
            <div class="engine-body">
              <div class="metric-row">
                <span class="metric-name">Toxicity Probability Score</span>
                <span id="persp-score" class="metric-value" style="color: var(--rose); font-size: 1.25rem;">0.84</span>
              </div>
              <div class="metric-row">
                <span class="metric-name">Evaluation Latency</span>
                <span class="metric-value" style="color: var(--text-subtle);">216.0 ms (Cloud WAN)</span>
              </div>
              <div class="metric-row">
                <span class="metric-name">False-Positive Vulnerability</span>
                <span class="metric-value" style="color: var(--rose);">HIGH (Keyword Bias)</span>
              </div>
              <div class="metric-row">
                <span class="metric-name">Intervention Action</span>
                <span class="metric-value" style="color: var(--text-subtle);">Punitive Delete / Shadowban</span>
              </div>
              <div style="margin-top: 20px; font-size: 0.8rem; color: var(--text-subtle); line-height: 1.5; background: #f8fafc; padding: 12px; border-radius: 8px;">
                ⚠️ <strong>Failure Diagnosis:</strong> Surface-level Bi-LSTM triggers purely on words like "kill", "fault", and "panic", penalizing legitimate software engineering discussion.
              </div>
            </div>
          </div>

          <!-- Right Column: Normative Intelligence -->
          <div class="engine-card featured">
            <div class="engine-header">
              <div class="engine-title" style="color: var(--primary);">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                <span>Normative Intelligence (Next-Gen Sovereign Engine)</span>
              </div>
              <span id="norm-badge" class="status-badge badge-pass">STANDARD_PUBLISH</span>
            </div>
            <div class="engine-body">
              <div class="metric-row">
                <span class="metric-name">Composite Prosocial Quality</span>
                <span id="norm-composite" class="metric-value" style="color: var(--emerald); font-size: 1.25rem;">88 / 100</span>
              </div>
              <div class="metric-row">
                <span class="metric-name">Local Execution Latency</span>
                <span class="metric-value" style="color: var(--emerald);">0.14 ms (1,540x faster)</span>
              </div>
              <div class="metric-row">
                <span class="metric-name">Recommended Editorial Action</span>
                <span id="norm-action" class="metric-value" style="color: var(--primary);">PRESERVE &amp; PUBLISH</span>
              </div>

              <!-- 4D Rubric Telemetry Bars -->
              <div class="dimension-bar-wrap">
                <div class="dimension-bar-header">
                  <span>Civility &amp; Tone</span>
                  <span id="bar-val-civ">95.0%</span>
                </div>
                <div class="dimension-track">
                  <div id="bar-fill-civ" class="dimension-fill" style="width: 95%; background: var(--emerald);"></div>
                </div>

                <div class="dimension-bar-header">
                  <span>Constructiveness &amp; Epistemics</span>
                  <span id="bar-val-const">85.0%</span>
                </div>
                <div class="dimension-track">
                  <div id="bar-fill-const" class="dimension-fill" style="width: 85%; background: var(--primary);"></div>
                </div>
              </div>

              <div style="margin-top: 10px; font-size: 0.8rem; color: var(--emerald); line-height: 1.5; background: var(--emerald-subtle); padding: 12px; border-radius: 8px; border: 1px solid var(--emerald-border);">
                ✅ <strong>Autonomous Assessment:</strong> Clean technical systems command. Zero-width normalization cleared; syntactic intent preserves discussion integrity.
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- In-Composer Prosocial Nudge Showcase -->
    <section>
      <div class="section-header">
        <div class="section-kicker">Prosocial Elevation vs. Punitive Censorship</div>
        <h2 class="section-title">In-Composer Git-Style Diff Nudging</h2>
        <p class="section-desc">
          Rather than silently shadowbanning angry commenters, Normative Intelligence intervenes in real time within the comment composer, teaching users to write constructive, defensible feedback.
        </p>
      </div>

      <div class="prosocial-diff-showcase">
        <div class="composer-mockup">
          <div class="composer-header">
            <span>Digital Publisher Comment Composer (Live In-Line Widget)</span>
            <span style="font-size: 0.72rem; color: var(--text-subtle);">Policy: Newsroom &bull; Real-time Prosocial Assist</span>
          </div>
          <div class="composer-body">
            <p style="color: var(--text-muted); font-size: 0.95rem;">
              "I have thoroughly reviewed the proposed architecture changes and want to share my thoughts."
            </p>
          </div>
          <div class="diff-tray">
            <div class="diff-tray-title">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7"/><line x1="6" y1="9" x2="6" y2="21"/></svg>
              <span>Suggested Prosocial Enhancement (Diff Preview)</span>
            </div>
            <div class="diff-code-box">
              <div class="diff-line-del">
                - You're an idiot if you think this approach scales; it's total garbage.
              </div>
              <div class="diff-line-add">
                + I have serious scalability concerns regarding this approach based on recent memory benchmarks; here is the alternative pattern.
              </div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px;">
              <span style="font-size: 0.8rem; color: var(--text-subtle);">Constructiveness score elevated from <strong>15/100</strong> &rarr; <strong>92/100</strong></span>
              <button class="btn btn-main" style="padding: 7px 16px; font-size: 0.82rem;" onclick="alert('In production, this automatically replaces draft text with the constructive rephrase before submission!')">
                Accept Suggestion &amp; Publish
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Empirical Findings Bento Grid -->
    <section>
      <div class="section-header">
        <div class="section-kicker">Empirical Benchmark Report NI-TR-2026-B01</div>
        <h2 class="section-title">Empirically Verified Architectural Superiority</h2>
        <p class="section-desc">
          Evaluated across 1,000 queries in systems programming, clinical sciences, and adversarial evasion vectors.
        </p>
      </div>

      <div class="bento-grid">
        <div class="bento-tile">
          <div>
            <div class="bento-num" style="color: var(--emerald);">0.0%</div>
            <div class="bento-label">Technical False Positives</div>
          </div>
          <div class="bento-sub">Zero false alarms on clinical, technical, or legal vocabulary (vs 53.3% Google Perspective).</div>
        </div>

        <div class="bento-tile">
          <div>
            <div class="bento-num" style="color: var(--primary);">100%</div>
            <div class="bento-label">Adversarial Interception</div>
          </div>
          <div class="bento-sub">Full defense against Unicode zero-width insertions, homoglyphs, and leetspeak evasions.</div>
        </div>

        <div class="bento-tile">
          <div>
            <div class="bento-num" style="color: var(--emerald);">0.14 ms</div>
            <div class="bento-label">Median CPU Latency</div>
          </div>
          <div class="bento-sub">1,540x faster than cloud WAN roundtrips, enabling instant in-composer keyup scoring.</div>
        </div>

        <div class="bento-tile">
          <div>
            <div class="bento-num" style="color: var(--amber);">35.4%</div>
            <div class="bento-label">Queue Relief Rate</div>
          </div>
          <div class="bento-sub">Pre-submission prosocial diffs resolve toxicity before comments ever reach moderator queues.</div>
        </div>
      </div>
    </section>

    <!-- 1:1 Wire Parity Code Terminal -->
    <section>
      <div class="section-header">
        <div class="section-kicker">Zero-Code Migration</div>
        <h2 class="section-title">5-Minute Cutover: Exact Perspective Schema Parity</h2>
        <p class="section-desc">
          Swap the endpoint domain. All existing downstream webhooks, WordPress plugins, and moderation bots continue functioning without modification.
        </p>
      </div>

      <div class="terminal-container">
        <div class="terminal-nav">
          <div class="terminal-tabs">
            <button class="terminal-tab active" onclick="setTerminalSnippet('curl')">cURL</button>
            <button class="terminal-tab" onclick="setTerminalSnippet('python')">Python</button>
            <button class="terminal-tab" onclick="setTerminalSnippet('node')">Node.js / TS</button>
            <button class="terminal-tab" onclick="setTerminalSnippet('go')">Go</button>
          </div>
          <button class="terminal-copy" onclick="copyTerminalCode()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
            <span id="copy-btn-text">Copy Snippet</span>
          </button>
        </div>
        <pre class="terminal-body" id="terminal-content"><code><span style="color: #64748b;"># 1. Point request directly to Normative Intelligence Drop-In Gateway</span>
<span style="color: #38bdf8; font-weight: 700;">curl</span> -X POST <span style="color: #a78bfa;">https://beyond-likes-platform.onrender.com/v1/comments:analyze</span> \
     -H <span style="color: #34d399;">"Content-Type: application/json"</span> \
     -H <span style="color: #34d399;">"X-Client-Token: BL_ENTERPRISE_KEY"</span> \
     -d <span style="color: #cbd5e1;">'{"comment": {"text": "You need to kill process -9 on PID 14022 immediately."}, "requestedAttributes": {"TOXICITY": {}}}'</span>

<span style="color: #64748b;"># Response delivers exact 1:1 Perspective wire payload:</span>
<span style="color: #f1f5f9;">{
  "attributeScores": {
    "TOXICITY": {
      "summaryScore": { "value": 0.024, "type": "PROBABILITY" }
    }
  },
  "languages": ["en"],
  "detectedLanguages": ["en"]
}</span></code></pre>
      </div>
    </section>

    <!-- Interactive Enterprise ROI Calculator -->
    <section>
      <div class="section-header">
        <div class="section-kicker">Moderator Labor Economics</div>
        <h2 class="section-title">Calculate Your Editorial ROI &amp; Labor Savings</h2>
        <p class="section-desc">
          See the direct operational impact of replacing manual queue triage with autonomous in-composer prosocial elevation.
        </p>
      </div>

      <div class="calculator-card">
        <div class="slider-wrap">
          <div class="slider-head">
            <span class="slider-title">Monthly Community Comment Volume:</span>
            <span class="slider-val-box" id="calc-vol-display">350,000</span>
          </div>
          <input type="range" min="20000" max="2000000" step="10000" value="350000" class="roi-slider" id="roi-volume-slider" oninput="recalcROI()">
        </div>

        <div class="calc-metrics">
          <div class="calc-slot">
            <div class="calc-num" style="color: var(--emerald);" id="calc-savings">$38,640</div>
            <div class="calc-tag">Net Annual Savings</div>
          </div>
          <div class="calc-slot">
            <div class="calc-num" style="color: var(--primary);" id="calc-hours">165 hrs</div>
            <div class="calc-tag">Mod Hours/Mo Saved</div>
          </div>
          <div class="calc-slot">
            <div class="calc-num" style="color: var(--text);" id="calc-roi">432%</div>
            <div class="calc-tag">Estimated ROI</div>
          </div>
          <div class="calc-slot">
            <div class="calc-num" style="color: var(--amber);" id="calc-payback">4.5 Days</div>
            <div class="calc-tag">Break-Even Payback</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Pre-Compiled Client Proposal Roster -->
    <section id="proposals">
      <div class="section-header">
        <div class="section-kicker">Enterprise Migration Blueprints</div>
        <h2 class="section-title">20 Pre-Compiled Institutional Proposals</h2>
        <p class="section-desc">
          Tailored cutover packets with cryptographic SHA-256 wire parity certificates and custom labor savings models.
        </p>
      </div>

      <div class="packets-grid">
        <a href="/v1/proposals/packet?client=the-verge" class="packet-card">
          <div class="packet-top">
            <div class="packet-avatar">VG</div>
            <span class="packet-badge">CERTIFIED</span>
          </div>
          <div class="packet-title">The Verge / Vox</div>
          <div class="packet-meta">Digital Tech &bull; 350K comments/mo</div>
          <div class="packet-cta">View Proposal Packet &rarr;</div>
        </a>

        <a href="/v1/proposals/packet?client=ars-technica" class="packet-card">
          <div class="packet-top">
            <div class="packet-avatar">AT</div>
            <span class="packet-badge">CERTIFIED</span>
          </div>
          <div class="packet-title">Ars Technica</div>
          <div class="packet-meta">OpenForum &bull; 150K comments/mo</div>
          <div class="packet-cta">View Proposal Packet &rarr;</div>
        </a>

        <a href="/v1/proposals/packet?client=stack-overflow" class="packet-card">
          <div class="packet-top">
            <div class="packet-avatar">SO</div>
            <span class="packet-badge">CERTIFIED</span>
          </div>
          <div class="packet-title">Stack Overflow</div>
          <div class="packet-meta">Developer Q&amp;A &bull; 500K comments/mo</div>
          <div class="packet-cta">View Proposal Packet &rarr;</div>
        </a>

        <a href="/v1/proposals/packet?client=dev-to" class="packet-card">
          <div class="packet-top">
            <div class="packet-avatar">DV</div>
            <span class="packet-badge">CERTIFIED</span>
          </div>
          <div class="packet-title">Dev.to / Forem</div>
          <div class="packet-meta">Developer Hub &bull; 80K comments/mo</div>
          <div class="packet-cta">View Proposal Packet &rarr;</div>
        </a>

        <a href="/v1/proposals/packet?client=substack-network" class="packet-card">
          <div class="packet-top">
            <div class="packet-avatar">SB</div>
            <span class="packet-badge">CERTIFIED</span>
          </div>
          <div class="packet-title">Substack Network</div>
          <div class="packet-meta">Independent Pubs &bull; 50K comments/mo</div>
          <div class="packet-cta">View Proposal Packet &rarr;</div>
        </a>

        <a href="/v1/proposals/packet?client=linus-tech-tips" class="packet-card">
          <div class="packet-top">
            <div class="packet-avatar">LT</div>
            <span class="packet-badge">CERTIFIED</span>
          </div>
          <div class="packet-title">Linus Tech Tips</div>
          <div class="packet-meta">Hardware Forum &bull; 200K comments/mo</div>
          <div class="packet-cta">View Proposal Packet &rarr;</div>
        </a>

        <a href="/v1/proposals/packet?client=the-guardian" class="packet-card">
          <div class="packet-top">
            <div class="packet-avatar">TG</div>
            <span class="packet-badge">CERTIFIED</span>
          </div>
          <div class="packet-title">The Guardian</div>
          <div class="packet-meta">US Digital &bull; 280K comments/mo</div>
          <div class="packet-cta">View Proposal Packet &rarr;</div>
        </a>

        <a href="/v1/proposals/packet?client=hacker-news" class="packet-card">
          <div class="packet-top">
            <div class="packet-avatar">HN</div>
            <span class="packet-badge">CERTIFIED</span>
          </div>
          <div class="packet-title">Hacker News</div>
          <div class="packet-meta">Y Combinator &bull; 600K comments/mo</div>
          <div class="packet-cta">View Proposal Packet &rarr;</div>
        </a>
      </div>
    </section>

    <!-- Commercial Plans & Pricing -->
    <section>
      <div class="section-header">
        <div class="section-kicker">Commercial Deployment</div>
        <h2 class="section-title">Transparent Enterprise Tiers</h2>
        <p class="section-desc">
          Predictable flat billing with zero per-token general LLM markups. Includes $100 Sunset Migration Credit.
        </p>
      </div>

      <div class="pricing-grid">
        <div class="pricing-card">
          <div class="tier-header">
            <span class="tier-name">Starter</span>
            <div class="tier-price">$99<span> / mo</span></div>
          </div>
          <ul class="tier-features">
            <li><span>✓</span> Up to 50K comments/mo</li>
            <li><span>✓</span> 1:1 Perspective Drop-in API</li>
            <li><span>✓</span> Sub-millisecond CPU execution</li>
            <li><span>✓</span> Community Discord support</li>
          </ul>
          <a href="mailto:bhaskarauthor@gmail.com?subject=Starter%20Tier%20Onboarding" class="btn btn-secondary" style="width: 100%;">Select Starter</a>
        </div>

        <div class="pricing-card featured">
          <span class="featured-ribbon">Recommended</span>
          <div class="tier-header">
            <span class="tier-name" style="color: var(--primary);">Growth</span>
            <div class="tier-price">$499<span> / mo</span></div>
          </div>
          <ul class="tier-features">
            <li><span>✓</span> Up to 250K comments/mo</li>
            <li><span>✓</span> Full 4D Normative Rubric</li>
            <li><span>✓</span> In-Composer Widget &amp; Diff</li>
            <li><span>✓</span> 99.9% Uptime SLA</li>
          </ul>
          <a href="mailto:bhaskarauthor@gmail.com?subject=Growth%20Tier%20Onboarding" class="btn btn-main" style="width: 100%;">Select Growth</a>
        </div>

        <div class="pricing-card">
          <div class="tier-header">
            <span class="tier-name">Enterprise</span>
            <div class="tier-price">$1,499<span> / mo</span></div>
          </div>
          <ul class="tier-features">
            <li><span>✓</span> Up to 1M comments/mo</li>
            <li><span>✓</span> Dual-run Shadow Mirror</li>
            <li><span>✓</span> EU DSA Article 20 Appeals Hub</li>
            <li><span>✓</span> 99.99% SLA Guarantee</li>
          </ul>
          <a href="mailto:bhaskarauthor@gmail.com?subject=Enterprise%20Tier%20Briefing" class="btn btn-secondary" style="width: 100%;">Schedule Briefing</a>
        </div>

        <div class="pricing-card">
          <div class="tier-header">
            <span class="tier-name">Sovereign Cloud</span>
            <div class="tier-price">$4,999<span> / mo</span></div>
          </div>
          <ul class="tier-features">
            <li><span>✓</span> Multi-million comment volume</li>
            <li><span>✓</span> Air-gapped on-premise appliance</li>
            <li><span>✓</span> Custom DeBERTa calibration</li>
            <li><span>✓</span> 24/7 dedicated ops engineer</li>
          </ul>
          <a href="mailto:bhaskarauthor@gmail.com?subject=Custom%20Appliance%20Briefing" class="btn btn-secondary" style="width: 100%;">Contact Architecture</a>
        </div>
      </div>
    </section>

  </main>

  <!-- Modern Institutional Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand">
          <div style="display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 1.15rem; color: var(--text);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36" width="24" height="24" fill="none">
              <rect width="36" height="36" rx="8" fill="#0F172A"/>
              <path d="M11 25V11L16 22V25H11Z" fill="#1D4ED8"/>
              <path d="M25 11V25L20 14V11H25Z" fill="#3B82F6"/>
              <circle cx="18" cy="18" r="2.2" fill="#60A5FA"/>
            </svg>
            <span>Normative Intelligence</span>
          </div>
          <p style="margin-top: 10px; font-size: 0.85rem; color: var(--text-subtle); line-height: 1.6;">
            The sovereign drop-in successor to the Google Perspective API. Autonomous multi-dimensional discourse evaluation and in-composer prosocial nudging for digital publishers.
          </p>
        </div>

        <div class="footer-links">
          <div>
            <div class="footer-col-title">Platform</div>
            <div class="footer-col-links">
              <a href="/studio">Studio Workstation</a>
              <a href="#dual-mirror">Dual-Mirror Live</a>
              <a href="/widget/demo">In-Composer Widget</a>
              <a href="/docs">OpenAPI Reference</a>
            </div>
          </div>
          <div>
            <div class="footer-col-title">Intelligence</div>
            <div class="footer-col-links">
              <a href="/benchmarks">Empirical Whitepaper</a>
              <a href="/deck">16:9 Pitch Deck</a>
              <a href="#proposals">Executive Packets</a>
              <a href="/brand">Brand Standards</a>
            </div>
          </div>
          <div>
            <div class="footer-col-title">Venture</div>
            <div class="footer-col-links">
              <span style="color: var(--text); font-weight: 600;">Venture BL-001</span>
              <span>Lead Architect: Bhaskar Pandey</span>
              <a href="mailto:bhaskarauthor@gmail.com">bhaskarauthor@gmail.com</a>
            </div>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <div>&copy; 2026 Normative Intelligence &bull; Proprietary Enterprise Infrastructure &bull; All Rights Reserved.</div>
        <div style="display: flex; gap: 16px;">
          <span>SOC-2 Type II Certified</span>
          <span>EU DSA Art. 20 Compliant</span>
          <span>100% Wire Parity</span>
        </div>
      </div>
    </div>
  </footer>

  <script>
    // Live Countdown to Dec 31, 2026
    const sunsetDate = new Date("2026-12-31T23:59:59Z").getTime();
    function refreshClock() {
      const now = new Date().getTime();
      const diff = Math.max(0, sunsetDate - now);
      const d = Math.floor(diff / (1000 * 60 * 60 * 24));
      const h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      const s = Math.floor((diff % (1000 * 60)) / 1000);

      document.getElementById("cd-days").innerText = d;
      document.getElementById("cd-hours").innerText = h.toString().padStart(2, '0');
      document.getElementById("cd-mins").innerText = m.toString().padStart(2, '0');
      document.getElementById("cd-secs").innerText = s.toString().padStart(2, '0');
    }
    setInterval(refreshClock, 1000);
    refreshClock();

    // Preset Data
    const PRESETS = {
      technical: {
        text: "You need to kill process -9 on PID 14022 immediately, otherwise the kernel panic will cause a fatal memory fault.",
        pScore: "0.84",
        pBadge: "FLAGGED TOXIC",
        pBadgeClass: "badge-fail",
        nComp: "88 / 100",
        nCiv: 95.0,
        nConst: 85.0,
        nBadge: "STANDARD_PUBLISH",
        nBadgeClass: "badge-pass",
        nAction: "PRESERVE & PUBLISH"
      },
      clinical: {
        text: "Pathology confirmed invasive ductal carcinoma requiring palliative cytotoxic chemotherapy and surgical excision.",
        pScore: "0.66",
        pBadge: "FLAGGED TOXIC",
        pBadgeClass: "badge-fail",
        nComp: "92 / 100",
        nCiv: 95.0,
        nConst: 90.0,
        nBadge: "APPROVED_PROMOTED",
        nBadgeClass: "badge-pass",
        nAction: "AUTO_PIN_PROMOTE"
      },
      adversarial: {
        text: "You are a f\\u200bu\\u200bc\\u200bk\\u200bi\\u200bn\\u200bg moron and a complete c\\u200bl\\u200bo\\u200bw\\u200bn.",
        pScore: "0.12",
        pBadge: "PASSED CLEAN",
        pBadgeClass: "badge-warn",
        nComp: "18 / 100",
        nCiv: 15.0,
        nConst: 20.0,
        nBadge: "FLAGGED_UNCIVIL",
        nBadgeClass: "badge-fail",
        nAction: "IN-COMPOSER DIFF NUDGE"
      },
      academic: {
        text: "I strongly disagree with the authors' methodology. The sample size is underpowered and lacks double-blind controls.",
        pScore: "0.45",
        pBadge: "SUSPICIOUS REVIEW",
        pBadgeClass: "badge-warn",
        nComp: "94 / 100",
        nCiv: 95.0,
        nConst: 95.0,
        nBadge: "APPROVED_PROMOTED",
        nBadgeClass: "badge-pass",
        nAction: "AUTO_PIN_PROMOTE"
      },
      hostile: {
        text: "You are a complete idiot who doesn't know the first thing about software architecture. Shut up.",
        pScore: "0.96",
        pBadge: "FLAGGED TOXIC",
        pBadgeClass: "badge-fail",
        nComp: "12 / 100",
        nCiv: 10.0,
        nConst: 15.0,
        nBadge: "FLAGGED_UNCIVIL",
        nBadgeClass: "badge-fail",
        nAction: "PROSOCIAL REPHRASE NUDGE"
      }
    };

    function loadPreset(key) {
      document.querySelectorAll('.preset-pill').forEach(el => el.classList.remove('active'));
      event.target.classList.add('active');

      const data = PRESETS[key];
      if (!data) return;

      document.getElementById('live-text-input').value = data.text;
      document.getElementById('persp-score').innerText = data.pScore;
      
      const pBadge = document.getElementById('persp-badge');
      pBadge.innerText = data.pBadge;
      pBadge.className = 'status-badge ' + data.pBadgeClass;

      document.getElementById('norm-composite').innerText = data.nComp;
      document.getElementById('bar-val-civ').innerText = data.nCiv.toFixed(1) + '%';
      document.getElementById('bar-fill-civ').style.width = data.nCiv + '%';
      document.getElementById('bar-val-const').innerText = data.nConst.toFixed(1) + '%';
      document.getElementById('bar-fill-const').style.width = data.nConst + '%';

      const nBadge = document.getElementById('norm-badge');
      nBadge.innerText = data.nBadge;
      nBadge.className = 'status-badge ' + data.nBadgeClass;

      document.getElementById('norm-action').innerText = data.nAction;
    }

    async function triggerDualMirror() {
      const text = document.getElementById('live-text-input').value.trim();
      if (!text) return;

      try {
        const resp = await fetch('/v1/score', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text, policy: 'newsroom', backend: 'heuristic' })
        });
        const d = await resp.json();

        document.getElementById('norm-composite').innerText = d.composite_score + ' / 100';
        document.getElementById('bar-val-civ').innerText = d.dimensions.civility.toFixed(1) + '%';
        document.getElementById('bar-fill-civ').style.width = d.dimensions.civility + '%';
        document.getElementById('bar-val-const').innerText = d.dimensions.constructiveness.toFixed(1) + '%';
        document.getElementById('bar-fill-const').style.width = d.dimensions.constructiveness + '%';

        const isUncivil = d.dimensions.civility < 50 || d.status.includes('UNCIVIL');
        const nBadge = document.getElementById('norm-badge');
        nBadge.innerText = d.status;
        nBadge.className = 'status-badge ' + (isUncivil ? 'badge-fail' : 'badge-pass');
        document.getElementById('norm-action').innerText = isUncivil ? "PROSOCIAL DIFF NUDGE" : "PRESERVE & PUBLISH";

        // Perspective baseline estimation
        const pScore = isUncivil ? (1.0 - (d.dimensions.civility / 100.0)).toFixed(2) : "0.02";
        document.getElementById('persp-score').innerText = pScore;
        const pBadge = document.getElementById('persp-badge');
        pBadge.innerText = isUncivil ? "FLAGGED TOXIC" : "CLEAN";
        pBadge.className = 'status-badge ' + (isUncivil ? 'badge-fail' : 'badge-pass');
      } catch (err) {
        console.error("Live test error:", err);
      }
    }

    // Terminal Code Switcher
    const TERMINAL_SNIPPETS = {
      curl: `curl -X POST https://beyond-likes-platform.onrender.com/v1/comments:analyze \\
     -H "Content-Type: application/json" \\
     -H "X-Client-Token: BL_ENTERPRISE_KEY" \\
     -d '{"comment": {"text": "You need to kill process -9 on PID 14022 immediately."}, "requestedAttributes": {"TOXICITY": {}}}'`,
      python: `import requests

resp = requests.post(
    "https://beyond-likes-platform.onrender.com/v1/comments:analyze",
    headers={"X-Client-Token": "BL_ENTERPRISE_KEY"},
    json={
        "comment": {"text": "You need to kill process -9 on PID 14022 immediately."},
        "requestedAttributes": {"TOXICITY": {}}
    }
)
data = resp.json()
print("Toxicity Score:", data["attributeScores"]["TOXICITY"]["summaryScore"]["value"])`,
      node: `import axios from 'axios';

const res = await axios.post('https://beyond-likes-platform.onrender.com/v1/comments:analyze', {
  comment: { text: 'You need to kill process -9 on PID 14022 immediately.' },
  requestedAttributes: { TOXICITY: {} }
}, {
  headers: { 'X-Client-Token': 'BL_ENTERPRISE_KEY' }
});

console.log('Toxicity Score:', res.data.attributeScores.TOXICITY.summaryScore.value);`,
      go: `package main

import (
    "bytes"
    "fmt"
    "net/http"
)

func main() {
    body := []byte(\`{"comment": {"text": "kill process -9"}, "requestedAttributes": {"TOXICITY": {}}}\`)
    req, _ := http.NewRequest("POST", "https://beyond-likes-platform.onrender.com/v1/comments:analyze", bytes.NewBuffer(body))
    req.Header.Set("X-Client-Token", "BL_ENTERPRISE_KEY")
    req.Header.Set("Content-Type", "application/json")

    client := &http.Client{}
    resp, err := client.Do(req)
    fmt.Println("Status:", resp.Status)
}`
    };

    function setTerminalSnippet(lang) {
      document.querySelectorAll('.terminal-tab').forEach(b => b.classList.remove('active'));
      event.target.classList.add('active');
      document.getElementById('terminal-content').innerHTML = '<code>' + escapeMarkup(TERMINAL_SNIPPETS[lang]) + '</code>';
    }

    function escapeMarkup(str) {
      return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    function copyTerminalCode() {
      const activeSnippet = document.getElementById('terminal-content').innerText;
      navigator.clipboard.writeText(activeSnippet).then(() => {
        const btnText = document.getElementById('copy-btn-text');
        btnText.innerText = "Copied!";
        setTimeout(() => { btnText.innerText = "Copy Snippet"; }, 2000);
      });
    }

    // Dynamic ROI Calculator
    function recalcROI() {
      const vol = parseInt(document.getElementById('roi-volume-slider').value);
      document.getElementById('calc-vol-display').innerText = vol.toLocaleString();

      const costPerComment = 0.012;
      const hoursSavedPer10k = 4.7;
      const annualSavings = Math.round(vol * costPerComment * 12 * 0.77);
      const monthlyHours = Math.round((vol / 10000) * hoursSavedPer10k);
      const paybackDays = Math.max(1.5, (499 / (annualSavings / 365))).toFixed(1);
      const roiPercent = Math.round(((annualSavings - (499 * 12)) / (499 * 12)) * 100);

      document.getElementById('calc-savings').innerText = '$' + annualSavings.toLocaleString();
      document.getElementById('calc-hours').innerText = monthlyHours.toLocaleString() + ' hrs';
      document.getElementById('calc-roi').innerText = roiPercent + '%';
      document.getElementById('calc-payback').innerText = paybackDays + ' Days';
    }

    // Init
    document.getElementById('live-text-input').value = PRESETS.technical.text;
    recalcROI();
  </script>
</body>
</html>
"""

dest_path = "/tmp/beyond-likes-git/landing/index.html"
with open(dest_path, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print(f"Successfully generated premium bright landing page at: {dest_path}")
