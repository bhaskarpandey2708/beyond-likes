# Normative Intelligence — Brand Kit & Visual Identity Guidelines

**Document Version:** 1.0.0-institutional  
**Release Date:** November 2026  
**Identity System:** Academic Rigor &bull; Enterprise Infrastructure &bull; Prosocial Governance  
**Lineage:** Proprietary Deep-Tech Venture (BL-001)  

---

## 1. Brand Philosophy & Core Positioning

Normative Intelligence builds enterprise editorial and Trust & Safety infrastructure. We are the **1:1 drop-in successor to the Google Perspective API** (which shuts down permanently on December 31, 2026).

* **Who We Are:** Editorial infrastructure and Trust & Safety middleware backed by academic research from Proprietary Architecture.
* **Who We Are NOT:** We are not a social media like-counter, an ad-tech analytics tracker, or a crude keyword blacklisting engine.
* **Visual Tone:** Pristine, institutional, authoritative, crisp, and restrained. Think **Anthropic / Stripe / McKinsey Technology Practice / MIT Lincoln Lab**. We design exclusively on crisp, high-contrast light and white canvases with deep obsidian slate typography and Cobalt Tech Blue accents.

---

## 2. Logo & Mark Specifications

### Primary Logo Mark (`brand/logo.svg`)
The logo mark consists of a rounded obsidian square containing two directional pillars linked by an epistemic bridge, representing multidimensional discourse balance, signal uplift, and normative calibration.

```
       [  ■ ■  ]    Obsidian Base: #0F172A (Stability, Infrastructure)
       [  ▲ ▲  ]    Left Pillar:   #1D4ED8 (Constructiveness & Rigor)
       [  ● ●  ]    Right Pillar:  #3B82F6 (Civility & Epistemic Grounding)
       [  ◆ ◆  ]    Core Bridge:   #60A5FA (Synthesis & Balance)
```

* **Minimum Digital Size:** 24px x 24px
* **Minimum Print Size:** 8mm x 8mm
* **Clearspace:** Equal to 50% of the mark's width on all four sides.
* **Prohibited Modifications:** Never rotate the mark, never apply drop shadows, never place on noisy photographic backgrounds, and never recolor in non-brand hues.

### Wordmark Lockup (`brand/logo-horizontal.svg`)
The horizontal lockup pairs the primary mark with `Normative.AI` in bold obsidian sans-serif (`#0F172A`) with a blue period accent (`#1D4ED8`), underlined by `AUTONOMOUS DISCOURSE INFRASTRUCTURE` in uppercase tracked slate (`#64748B`).

---

## 3. Official Color System (Editorial Warm Palette)

All customer-facing materials—including executive proposals, slide decks, PDFs, and website documentation—follow this distinctive, intellectual warm palette:

| Role | Color Name | Hex Code | RGB | Usage & Guidelines |
| :--- | :--- | :--- | :--- | :--- |
| **Canvas Primary** | Warm Linen / Alabaster | `#FAF8F5` | `250, 248, 245` | Primary warm background for all website surfaces, proposals, and slides. |
| **Surface Elevated** | Pure Surface White | `#FFFFFF` | `255, 255, 255` | Elevated cards, interactive composer frames, and callout boxes. |
| **Surface Subtle** | Warm Sand Wash | `#F4F0E8` | `244, 240, 232` | Secondary containers, table headers, and pill badges. |
| **Border / Rule** | Warm Stone | `#E8E3D8` | `232, 227, 216` | 1px clean dividers, card borders, and table gridlines. |
| **Text Primary** | Espresso Obsidian | `#18181B` | `24, 24, 27` | Document titles, main headers (H1/H2), bold metrics, and primary text (WCAG AAA). |
| **Text Secondary** | Muted Graphite | `#4A4A50` | `74, 74, 80` | Body paragraphs, explanatory copy, and metadata labels. |
| **Primary Brand** | Warm Terracotta | `#C8441B` | `200, 68, 27` | Signature action buttons, italicized editorial display accents, and primary brand marks. |
| **Success / Parity** | Forest Juniper | `#0D5C4E` | `13, 92, 78` | Parity Pass badges, prosocial diff additions, and SLA guarantees. |
| **Alert / Sunset** | Sandstone Amber | `#B45309` | `180, 83, 9` | Perspective sunset countdowns, latency warnings, and EOL milestones. |

---

## 4. Typography System

We use a distinctive, intellectual typography pairing combining contemporary luxury editorial serif with high-legibility geometric sans:
* **Display Serif (Headlines & Accents):** `Instrument Serif` (Italic, warm terracotta).
* **Primary Sans (Headings & UI):** `Plus Jakarta Sans` (Weight 600, 700, 800).
* **Data & Monospace:** `Space Mono` / `JetBrains Mono` for cryptographic hashes, code samples, and latency scores.

### Font Families
* **Display & Headings:** `Inter`, `-apple-system`, `BlinkMacSystemFont`, `"Plus Jakarta Sans"`, sans-serif.
  - Weight: SemiBold (600) for H2/H3; Bold (700) for Title / H1.
  - Letter Spacing: `-0.025em` for large titles (creates tight, authoritative German/Swiss editorial rhythm).
* **Body Text:** `Inter`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, Roboto, sans-serif.
  - Weight: Regular (400) for narrative; Medium (500) for emphasis and UI labels.
  - Line Height: `1.65` (optimum readability for dense technical briefs).
* **Monospace / Code / Hashes:** `ui-monospace`, `JetBrains Mono`, `SFMono-Regular`, `Menlo`, Consolas, monospace.
  - Weight: Regular (400) and SemiBold (600).
  - Used for API endpoints, JSON payloads, SHA-256 fingerprints, and SLA figures.

### Scale Hierarchy (Web & PDF)
* **Document Title (H1):** `1.85rem` (29.6px), `line-height: 1.25`, `weight: 700`, `color: #0F172A`
* **Section Heading (H2):** `1.35rem` (21.6px), `line-height: 1.35`, `weight: 600`, `color: #0F172A`
* **Subsection (H3):** `1.05rem` (16.8px), `line-height: 1.45`, `weight: 600`, `color: #1E293B`
* **Body Copy:** `0.94rem` (15.0px), `line-height: 1.65`, `weight: 400`, `color: #334155`
* **Table & Small Meta:** `0.82rem` (13.1px), `line-height: 1.5`, `weight: 500`, `color: #475569`
* **Footnotes & Disclaimers:** `0.75rem` (12.0px), `line-height: 1.4`, `weight: 400`, `color: #64748B`

---

## 5. Document & PDF Formatting Standards

When generating client packets, migration memos, or statutory reports:

1. **Page Architecture:**
   - Background: Pure white `#FFFFFF`.
   - Max Width: `880px` centered on canvas.
   - Margins: `48px 56px` padding.
   - Borders: Subdued `1px solid #E2E8F0`.
   - Box Shadow: Subtle `0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.03)`.
2. **KPI Metric Cards:**
   - 4-column grid (`grid-template-columns: repeat(4, 1fr); gap: 16px;`).
   - Card Background: `#FFFFFF` with `1px solid #E2E8F0` and `border-radius: 8px`.
   - Metric Value: `1.75rem`, Bold, `#0F172A`.
   - Metric Label: `0.72rem`, Uppercase, Letter-spacing `0.06em`, `#475569`.
3. **Tables:**
   - Header Row: `#F8FAFC`, text `#475569`, border-bottom `2px solid #E2E8F0`.
   - Data Rows: Alternating hover `#F8FAFC`, border-bottom `1px solid #F1F5F9`.
   - Numeric alignment: Right-aligned or bold-emphasized.
4. **Print Optimization (`@media print`):**
   - Background forced to pure `#FFFFFF !important`.
   - Hide interactive buttons (`.no-print { display: none !important; }`).
   - Box shadow removed; borders simplified to clean 1px lines.
   - Crisp 100% black text for ink clarity.

---

## 6. Startup Pitch Deck & Slide Specifications (16:9 Widescreen)

For executive briefings, board reviews, and investor presentations:

* **Aspect Ratio:** 16:9 (1920x1080px digital canvas).
* **Grid:** 12-column layout with 80px outer margins and 40px column gutters.
* **Slide Archetypes:**
  1. *Title / Cover Slide:* Clean white canvas, primary horizontal logo, bold thesis headline, author/origin metadata.
  2. *Market Crisis / Cliff Slide:* The Google Perspective sunset timeline, visual timeline bar, operational risk summary.
  3. *Problem vs Solution Split:* 2-column comparison (Legacy Binary Censorship vs Normative 4D Guidance).
  4. *Architecture Blueprint:* Technical schematic showing 1:1 `/comments:analyze` wire parity and sub-3ms quantized inference.
  5. *Traction & Pipeline Dashboard:* Funnel metrics ($109.5k active ARR pipeline, 20 enterprise publishers).
  6. *Financial Model & Unit Economics:* Gross margin advantage of local quantized execution over cloud LLM inference.
  7. *Closing / Executive Briefing Request:* Clear single CTA with direct contact link.

---

## 7. Social Media & Digital Asset Kit

### X / Twitter Banner (1500 x 500 px)
* **Background:** Soft Platinum White `#F8FAFC` with fine grid lines (`#E2E8F0`).
* **Left Alignment (at 100px):** Official mark + `Normative Intelligence`.
* **Headline:** `The Drop-in Prosocial Successor to Google Perspective API.`
* **Supporting Tag:** `100% Wire Parity • < 3.0 ms Latency SLA • Venture BL-001`
* **Right Accent:** Geometric waveform illustration in `#1D4ED8` and `#3B82F6`.

### LinkedIn Company Banner (1584 x 396 px)
* **Background:** Crisp White `#FFFFFF` with 1px bottom border `#E2E8F0`.
* **Copy:** `Enterprise Discourse Intelligence & Perspective API Sunset Contingency Infrastructure.`
* **Metadata Badge:** `Certified Dec 31, 2026 EOL Migration Ready`.

### OpenGraph Social Card (1200 x 630 px)
* **Card Dimensions:** 1200px wide, 630px high.
* **Visual Lockup:** Left-hand branding lockup with live endpoint code snippet on right (`POST /v1/comments:analyze`).
* **Author / Domain:** `https://beyond-likes-platform.onrender.com/docs`.
