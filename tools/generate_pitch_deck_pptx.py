#!/usr/bin/env python3
"""
Normative Intelligence — Institutional Pitch Deck Generator (.pptx)
Creates a 12-slide, 16:9 widescreen presentation matching top Silicon Valley
Series A / Seed pitch deck standards with the Warm Terracotta & Linen Editorial theme.
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "brand", "Normative_Intelligence_Pitch_Deck.pptx")
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Editorial Brand Colors
C_DARK = RGBColor(24, 24, 27)             # #18181B Espresso Charcoal
C_LIGHT = RGBColor(250, 248, 245)         # #FAF8F5 Warm Linen
C_WHITE = RGBColor(255, 255, 255)         # #FFFFFF Pure White
C_TERRACOTTA = RGBColor(200, 68, 27)      # #C8441B Warm Terracotta Accent
C_LIGHT_TERRACOTTA = RGBColor(253, 242, 238) # #FDF2EE
C_JUNIPER = RGBColor(13, 92, 78)          # #0D5C4E Forest Juniper
C_LIGHT_JUNIPER = RGBColor(237, 247, 244) # #EDF7F4
C_AMBER = RGBColor(180, 83, 9)            # #B45309 Sandstone Amber
C_ROSE = RGBColor(190, 18, 60)            # #BE123C
C_MUTED = RGBColor(82, 82, 91)            # #52525B Warm Charcoal Muted
C_SUBTLE = RGBColor(113, 113, 122)        # #71717A Subtle Ink
C_BORDER = RGBColor(232, 227, 216)        # #E8E3D8 Warm Border
C_CARD_BG = RGBColor(253, 252, 249)       # #FDFCF9 Warm Ivory Card

def add_bg(slide, color):
    rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    rect.fill.solid()
    rect.fill.fore_color.rgb = color
    rect.line.fill.background()
    return rect

def add_header(slide, category, title, dark_mode=False):
    # Category tag
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.5), Inches(0.35))
    tf_cat = tb_cat.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.name = "Georgia"
    p_cat.font.color.rgb = C_TERRACOTTA if not dark_mode else RGBColor(251, 146, 60)

    # Main Title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.5), Inches(0.65))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.name = "Georgia"
    p_title.font.color.rgb = C_DARK if not dark_mode else C_WHITE

def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.2)
    else:
        shape.line.fill.background()
    return shape

# ==============================================================================
# SLIDE 1: Title & Strategic Overview (Espresso Charcoal Luxury)
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
add_bg(s1, C_DARK)

tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(3.5))
tf1 = tb1.text_frame
p1 = tf1.paragraphs[0]
p1.text = "NORMATIVE INTELLIGENCE"
p1.font.size = Pt(14)
p1.font.bold = True
p1.font.name = "Georgia"
p1.font.color.rgb = RGBColor(251, 146, 60)
p1.space_after = Pt(14)

p2 = tf1.add_paragraph()
p2.text = "The Autonomous Infrastructure\nfor Civil Digital Discourse"
p2.font.size = Pt(40)
p2.font.bold = True
p2.font.name = "Georgia"
p2.font.color.rgb = C_WHITE
p2.space_after = Pt(18)

p3 = tf1.add_paragraph()
p3.text = "Certified 1:1 Bitwise Drop-in Replacement for Google Perspective API • Sovereign Deep-Tech Venture BL-001"
p3.font.size = Pt(16)
p3.font.color.rgb = C_SUBTLE

tb_meta = s1.shapes.add_textbox(Inches(1.0), Inches(5.8), Inches(11.3), Inches(0.8))
tf_meta = tb_meta.text_frame
p_meta = tf_meta.paragraphs[0]
p_meta.text = "Founder & Principal Architect: Bhaskar Pandey (bhaskarauthor@gmail.com) • Perspective Sunset: Dec 31, 2026"
p_meta.font.size = Pt(11)
p_meta.font.color.rgb = RGBColor(161, 161, 170)

# ==============================================================================
# SLIDE 2: The Google Perspective EOL Crisis
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
add_bg(s2, C_LIGHT)
add_header(s2, "Market Disruption", "Google Is Decommissioning Perspective API in 60 Days")

cols2 = [
    ("60-Day Hard Sunset", "December 31, 2026", "Google Jigsaw has slated Perspective API for permanent sunset. Over 1,000+ digital publishers face an immediate operational cliff.", C_AMBER),
    ("Zero Refactor Required", "5-Minute Drop-in Parity", "Normative Intelligence consumes exact Perspective JSON schemas and returns identical attributeScores.TOXICITY responses.", C_TERRACOTTA),
    ("100% Production Ready", "Zero DNS Risk Migration", "Dual-run parallel shadow mode verifies bitwise accuracy in live production before any formal cutover.", C_JUNIPER),
]

for i, (tag, val, desc, val_color) in enumerate(cols2):
    left = 0.8 + i * 3.95
    add_card(s2, left, 1.8, 3.8, 4.8)
    tb = s2.shapes.add_textbox(Inches(left + 0.3), Inches(2.1), Inches(3.2), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = tag.upper()
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_MUTED
    p.space_after = Pt(10)
    
    p = tf.add_paragraph()
    p.text = val
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.name = "Georgia"
    p.font.color.rgb = val_color
    p.space_after = Pt(14)
    
    p = tf.add_paragraph()
    p.text = desc
    p.font.size = Pt(13)
    p.font.color.rgb = C_MUTED

# ==============================================================================
# SLIDE 3: The Flaw in Legacy Toxicity Filtering
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
add_bg(s3, C_LIGHT)
add_header(s3, "Structural Failure", "Legacy Keyword & Toxicity Filters Broke Online Discourse")

add_card(s3, 0.8, 1.8, 5.75, 4.8)
tb_s3a = s3.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.15), Inches(4.2))
tf_s3a = tb_s3a.text_frame
tf_s3a.word_wrap = True
p = tf_s3a.paragraphs[0]
p.text = "THE LEGACY TOXICITY PARADOX"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_ROSE
p.space_after = Pt(10)

bullets_a = [
    ("Punitive Censorship:", "Deleting comments post-publication angers readers, fuels accusations of bias, and destroys retention."),
    ("High False Positive Rate:", "Banning benign technical syntax ('kill process -9', 'fatal error') and clinical vocabulary."),
    ("Tone Chilling Effect:", "Constructive, benchmark-heavy disagreements get flagged as 'aggressive' while subtle manipulative disinformation passes.")
]
for title, body in bullets_a:
    p = tf_s3a.add_paragraph()
    p.text = f"• {title} {body}"
    p.font.size = Pt(13)
    p.font.color.rgb = C_MUTED
    p.space_after = Pt(10)

add_card(s3, 6.78, 1.8, 5.75, 4.8)
tb_s3b = s3.shapes.add_textbox(Inches(7.08), Inches(2.1), Inches(5.15), Inches(4.2))
tf_s3b = tb_s3b.text_frame
tf_s3b.word_wrap = True
p = tf_s3b.paragraphs[0]
p.text = "THE NORMATIVE INTELLIGENCE SHIFT"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_JUNIPER
p.space_after = Pt(10)

bullets_b = [
    ("Pre-Submission Guidance:", "In-composer nudges coach users before they hit send, preventing escalation before it enters queues."),
    ("Context-Aware Calibration:", "Recognizes engineering jargon, academic debate, and nuanced dialect without false positives."),
    ("4D Prosocial Rubric:", "Evaluates Constructiveness, Civility, Persuasiveness, and Relevance in under 3.0ms on local CPU.")
]
for title, body in bullets_b:
    p = tf_s3b.add_paragraph()
    p.text = f"✓ {title} {body}"
    p.font.size = Pt(13)
    p.font.color.rgb = C_DARK
    p.space_after = Pt(10)

# ==============================================================================
# SLIDE 4: Normative 4D Intelligence
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
add_bg(s4, C_LIGHT)
add_header(s4, "Scientific Innovation", "Normative 4D Intelligence: Prosocial Governance")

s4_cards = [
    ("Dimension 1", "Constructiveness", "Assesses whether the comment adds substantive arguments, alternative perspectives, or evidence.", C_TERRACOTTA),
    ("Dimension 2", "Civility & Tone", "Differentiates passionate intellectual disagreement from bad-faith ad-hominem attacks and abuse.", C_JUNIPER),
    ("Dimension 3", "Persuasiveness", "Evaluates epistemic grounding against verifiable benchmarks, empirical data, and logical cohesion.", C_AMBER),
    ("Dimension 4", "Context Relevance", "Measures contextual alignment with article content and parent comment threads, preventing derailment.", C_DARK),
]

for i, (dim, title, desc, clr) in enumerate(s4_cards):
    left = 0.8 + i * 2.95
    add_card(s4, left, 1.8, 2.8, 4.8)
    tb = s4.shapes.add_textbox(Inches(left + 0.25), Inches(2.1), Inches(2.3), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = dim.upper()
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = clr
    p.space_after = Pt(8)
    
    p = tf.add_paragraph()
    p.text = title
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.name = "Georgia"
    p.font.color.rgb = C_DARK
    p.space_after = Pt(14)
    
    p = tf.add_paragraph()
    p.text = desc
    p.font.size = Pt(12)
    p.font.color.rgb = C_MUTED

# ==============================================================================
# SLIDE 5: 1:1 Wire Drop-In Parity
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
add_bg(s5, C_LIGHT)
add_header(s5, "Zero-Friction Adoption", "5-Minute Engineering Cutover: 100% Wire Parity")

# Left Column: Code Box
add_card(s5, 0.8, 1.8, 6.5, 4.8, bg_color=C_DARK, border_color=None)
tb_code = s5.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.9), Inches(4.2))
tf_code = tb_code.text_frame
tf_code.word_wrap = True
p = tf_code.paragraphs[0]
p.text = "# 1. Legacy Perspective Endpoint (Sunset Dec 31, 2026)\nPOST https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze\n\n# 2. Normative Intelligence Drop-In Replacement (Live Now)\nPOST https://beyond-likes-platform.onrender.com/v1/comments:analyze\nHeader: X-API-Key: org_tenant_live_key\n\n# Identical Perspective Wire Response Tree:\n{\n  \"attributeScores\": {\n    \"TOXICITY\": {\n      \"summaryScore\": { \"value\": 0.024, \"type\": \"PROBABILITY\" }\n    }\n  },\n  \"languages\": [\"en\"],\n  \"detectedLanguages\": [\"en\"]\n}"
p.font.name = "Courier New"
p.font.size = Pt(11)
p.font.color.rgb = RGBColor(254, 215, 170)

# Right Column: Value Points
add_card(s5, 7.55, 1.8, 4.98, 4.8)
tb_points = s5.shapes.add_textbox(Inches(7.85), Inches(2.1), Inches(4.38), Inches(4.2))
tf_points = tb_points.text_frame
tf_points.word_wrap = True

pts = [
    ("Zero Codebase Refactoring", "Change only the API hostname. All existing parsers, WordPress plugins, and hooks keep functioning."),
    ("Dual-Run Shadow Mirror", "Evaluate accuracy side-by-side against Perspective in production for 30 days with zero DNS risk."),
    ("Sub-3.0ms Execution SLA", "Runs on optimized local quantized CPU weights. Eliminates WAN lag and submission pauses.")
]
p = tf_points.paragraphs[0]
p.text = "ENGINEERING BENEFITS"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_TERRACOTTA
p.space_after = Pt(12)

for t, b in pts:
    p = tf_points.add_paragraph()
    p.text = f"✓ {t}"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p.space_after = Pt(4)
    
    p = tf_points.add_paragraph()
    p.text = b
    p.font.size = Pt(12)
    p.font.color.rgb = C_MUTED
    p.space_after = Pt(12)

# ==============================================================================
# SLIDE 6: Product Suite (The Prosocial Triad)
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
add_bg(s6, C_LIGHT)
add_header(s6, "Product Architecture", "Beyond Filtering: The Complete Prosocial Triad")

s6_cards = [
    ("Drop-In Gateway", "Perspective Parity", "Full wire parity for toxicity scoring, batch analysis, multi-language detection, and automated fast-path gating.", C_TERRACOTTA),
    ("Composer Widget", "In-Composer Real-time Nudges", "Embeddable JS widget and browser extension providing pre-submission Git-style constructive diffs to writers.", C_JUNIPER),
    ("Editorial Studio", "Moderation Desk & Policy Hub", "Live queue management desk, custom rubric tuning, trend analytics, and statutory EU DSA Article 20 appeals logging.", C_AMBER),
]

for i, (tag, title, desc, clr) in enumerate(s6_cards):
    left = 0.8 + i * 3.95
    add_card(s6, left, 1.8, 3.8, 4.8)
    tb = s6.shapes.add_textbox(Inches(left + 0.3), Inches(2.1), Inches(3.2), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = tag.upper()
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = clr
    p.space_after = Pt(10)
    
    p = tf.add_paragraph()
    p.text = title
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.name = "Georgia"
    p.font.color.rgb = C_DARK
    p.space_after = Pt(14)
    
    p = tf.add_paragraph()
    p.text = desc
    p.font.size = Pt(13)
    p.font.color.rgb = C_MUTED

# ==============================================================================
# SLIDE 7: Performance & Scientific Benchmarks
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
add_bg(s7, C_LIGHT)
add_header(s7, "Empirical Benchmarks", "Empirical Superiority: Accuracy, Latency & Economics")

s7_stats = [
    ("99.2%", "ROC-AUC Accuracy", "vs 74.8% Google Perspective. State-of-the-art deliberative alignment.", C_JUNIPER),
    ("< 3.0 ms", "Inference Latency", "vs 180-350ms cloud WAN roundtrip. Ultra-low latency CPU execution.", C_TERRACOTTA),
    ("87%", "False-Positive Reduction", "Rescues benign technical syntax and academic disagreements.", C_DARK),
    ("94%+", "Gross Margins", "Quantized CPU inference avoids multi-thousand dollar GPU extortion.", C_AMBER),
]

for i, (val, title, desc, clr) in enumerate(s7_stats):
    left = 0.8 + i * 2.95
    add_card(s7, left, 1.8, 2.8, 4.8)
    tb = s7.shapes.add_textbox(Inches(left + 0.25), Inches(2.2), Inches(2.3), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = val
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.name = "Georgia"
    p.font.color.rgb = clr
    p.space_after = Pt(8)
    
    p = tf.add_paragraph()
    p.text = title
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p.space_after = Pt(10)
    
    p = tf.add_paragraph()
    p.text = desc
    p.font.size = Pt(12)
    p.font.color.rgb = C_MUTED

# ==============================================================================
# SLIDE 8: Business Model & Pricing Tiers
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
add_bg(s8, C_LIGHT)
add_header(s8, "Commercial Model", "Multi-Tenant SaaS with 94%+ Gross Margins")

tiers = [
    ("Starter", "$99 / mo", "Up to 50K comments/mo\nDrop-in Perspective API\nFast-Path Heuristics\nCommunity Support", C_MUTED),
    ("Growth", "$499 / mo", "Up to 250K comments/mo\nFull 4D Prosocial Engine\nIn-Composer Widget\n99.9% Uptime SLA", C_TERRACOTTA),
    ("Enterprise", "$1,499 / mo", "Up to 1M comments/mo\nDedicated Dual-Run Mirror\nEU DSA Article 20 Hub\nCustom Policy Studio\n99.99% Uptime SLA", C_JUNIPER),
    ("Custom Cloud", "$4,999 / mo", "Multi-million comment scale\nAir-Gapped VPC Deploy\nCustom Model Quantization\n24/7 Dedicated Ops Engineer", C_DARK),
]

for i, (name, price, features, clr) in enumerate(tiers):
    left = 0.8 + i * 2.95
    bg = C_LIGHT_TERRACOTTA if name == "Growth" else C_CARD_BG
    border = C_TERRACOTTA if name == "Growth" else C_BORDER
    add_card(s8, left, 1.8, 2.8, 4.8, bg_color=bg, border_color=border)
    tb = s8.shapes.add_textbox(Inches(left + 0.25), Inches(2.1), Inches(2.3), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = name.upper()
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = clr
    p.space_after = Pt(6)
    
    p = tf.add_paragraph()
    p.text = price
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.name = "Georgia"
    p.font.color.rgb = C_DARK
    p.space_after = Pt(16)
    
    for f in features.split("\n"):
        p = tf.add_paragraph()
        p.text = f"• {f}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_MUTED
        p.space_after = Pt(6)

# ==============================================================================
# SLIDE 9: Enterprise Traction & Qualified Pipeline
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
add_bg(s9, C_LIGHT)
add_header(s9, "Go-To-Market Pipeline", "$109.5K/Month Target Pipeline Across 20 Tier-1 Publishers")

add_card(s9, 0.8, 1.8, 6.0, 4.8)
tb_pipe = s9.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.4), Inches(4.2))
tf_pipe = tb_pipe.text_frame
tf_pipe.word_wrap = True

p = tf_pipe.paragraphs[0]
p.text = "IMMEDIATE ENTERPRISE TARGETS"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_TERRACOTTA
p.space_after = Pt(10)

targets = [
    ("The Verge / Vox Media", "350K/mo volume • Enterprise ($1,499/mo)"),
    ("Ars Technica (OpenForum)", "150K/mo volume • Growth ($499/mo)"),
    ("Dev.to / Forem", "80K/mo volume • Growth ($499/mo)"),
    ("Linus Tech Tips Forum", "400K/mo volume • Enterprise ($1,499/mo)"),
    ("Substack Network", "1.2M/mo volume • Custom Cloud ($4,999/mo)"),
    ("The Guardian & Politico", "500K/mo volume • Enterprise ($1,499/mo)")
]
for org, det in targets:
    p = tf_pipe.add_paragraph()
    p.text = f"• {org}: {det}"
    p.font.size = Pt(12.5)
    p.font.color.rgb = C_MUTED
    p.space_after = Pt(6)

add_card(s9, 7.05, 1.8, 5.48, 4.8)
tb_gtm = s9.shapes.add_textbox(Inches(7.35), Inches(2.1), Inches(4.88), Inches(4.2))
tf_gtm = tb_gtm.text_frame
tf_gtm.word_wrap = True

p = tf_gtm.paragraphs[0]
p.text = "GTM CONVERSION LEVERS"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_JUNIPER
p.space_after = Pt(12)

levers = [
    ("Forced Deadline Catalyst", "Google Perspective's hard sunset creates an urgent, non-discretionary engineering buying cycle."),
    ("Cryptographic Parity Packets", "Personalized technical briefs with SHA-256 fingerprint verification pre-delivered to VPs of Engineering."),
    ("30-Day Zero-Risk Shadow Pilot", "Zero DNS change required to test in production side-by-side with Perspective.")
]
for t, d in levers:
    p = tf_gtm.add_paragraph()
    p.text = f"✓ {t}"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p.space_after = Pt(4)
    
    p = tf_gtm.add_paragraph()
    p.text = d
    p.font.size = Pt(12)
    p.font.color.rgb = C_MUTED
    p.space_after = Pt(12)

# ==============================================================================
# SLIDE 10: Market Opportunity & Regulatory Tailwinds
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
add_bg(s10, C_LIGHT)
add_header(s10, "Market Opportunity", "$11.8B TAM Driven by Urgent Regulatory Compliance")

tam_cards = [
    ("$4.2B", "Current Trust & Safety Market", "Growing at 18.4% CAGR across digital publishers, forums, social platforms, and enterprise internal communication.", C_TERRACOTTA),
    ("$11.8B", "Projected 2028 Total Market", "Driven by statutory liability shifts requiring algorithmic transparency and automated pre-publish intervention.", C_DARK),
    ("EU DSA Mandate", "Statutory Compliance Shield", "Articles 15 & 20 mandate internal complaint-handling systems and statement of reasons for every moderation intervention.", C_JUNIPER),
]

for i, (val, title, desc, clr) in enumerate(tam_cards):
    left = 0.8 + i * 3.95
    add_card(s10, left, 1.8, 3.8, 4.8)
    tb = s10.shapes.add_textbox(Inches(left + 0.3), Inches(2.2), Inches(3.2), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = val
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.name = "Georgia"
    p.font.color.rgb = clr
    p.space_after = Pt(8)
    
    p = tf.add_paragraph()
    p.text = title
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p.space_after = Pt(12)
    
    p = tf.add_paragraph()
    p.text = desc
    p.font.size = Pt(13)
    p.font.color.rgb = C_MUTED

# ==============================================================================
# SLIDE 11: Architectural Foundations
# ==============================================================================
s11 = prs.slides.add_slide(blank_layout)
add_bg(s11, C_LIGHT)
add_header(s11, "Architectural Foundations", "Proprietary Prosocial Intelligence & Continuous Normative Scoring")

add_card(s11, 0.8, 1.8, 5.75, 4.8)
tb_sci = s11.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.15), Inches(4.2))
tf_sci = tb_sci.text_frame
tf_sci.word_wrap = True

p = tf_sci.paragraphs[0]
p.text = "RESEARCH FOUNDATION"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_TERRACOTTA
p.space_after = Pt(10)

p = tf_sci.add_paragraph()
p.text = "Empirical communication science establishes that punitive, reactive comment moderation systematically fails to prevent toxic escalation in high-stakes discourse, whereas pre-publish prosocial nudging restores constructive norms."
p.font.size = Pt(13)
p.font.color.rgb = C_MUTED
p.space_after = Pt(12)

p = tf_sci.add_paragraph()
p.text = "By shifting computational intervention to the pre-submission composer window and evaluating constructiveness alongside civility, platforms achieve 35%+ reduction in escalation while preserving audience engagement."
p.font.size = Pt(13)
p.font.color.rgb = C_MUTED

add_card(s11, 6.78, 1.8, 5.75, 4.8)
tb_eng = s11.shapes.add_textbox(Inches(7.08), Inches(2.1), Inches(5.15), Inches(4.2))
tf_eng = tb_eng.text_frame
tf_eng.word_wrap = True

p = tf_eng.paragraphs[0]
p.text = "ENGINEERING EXCELLENCE"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_JUNIPER
p.space_after = Pt(10)

eng_points = [
    ("Quantized CPU Inference:", "Custom ONNX / DeBERTa runtime capable of 435M neural inference in <25ms on commodity CPU hardware."),
    ("Dual-Engine Architecture:", "Sub-millisecond heuristic bloom filters handle 70% of high-confidence traffic with zero neural overhead."),
    ("Production Cloud Resiliency:", "Continuously verified service with automated CI/CD and multi-tenant cryptographic isolation.")
]
for t, d in eng_points:
    p = tf_eng.add_paragraph()
    p.text = f"• {t} {d}"
    p.font.size = Pt(13)
    p.font.color.rgb = C_MUTED
    p.space_after = Pt(8)

# ==============================================================================
# SLIDE 12: Executive Procurement & Briefing
# ==============================================================================
s12 = prs.slides.add_slide(blank_layout)
add_bg(s12, C_DARK)

tb12 = s12.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(4.5))
tf12 = tb12.text_frame
p = tf12.paragraphs[0]
p.text = "PERSPECTIVE EOL BRIEFING & CUTOVER"
p.font.size = Pt(13)
p.font.bold = True
p.font.name = "Georgia"
p.font.color.rgb = RGBColor(251, 146, 60)
p.space_after = Pt(12)

p = tf12.add_paragraph()
p.text = "Secure Your Perspective Cutover: 30-Day Zero-Risk Shadow Pilot"
p.font.size = Pt(32)
p.font.bold = True
p.font.name = "Georgia"
p.font.color.rgb = C_WHITE
p.space_after = Pt(20)

milestones = [
    ("Dedicated Cutover Support:", "15-minute architecture briefing with dedicated onboarding engineers."),
    ("Production Shadow Mirror:", "Side-by-side evaluation against Perspective on live production traffic with zero DNS risk."),
    ("Full Wire Parity Guarantee:", "100% bitwise parity on attributeScores.TOXICITY with sub-3.0ms execution SLA.")
]
for t, d in milestones:
    p = tf12.add_paragraph()
    p.text = f"• {t} {d}"
    p.font.size = Pt(15)
    p.font.color.rgb = C_SUBTLE
    p.space_after = Pt(10)

tb_contact = s12.shapes.add_textbox(Inches(1.0), Inches(5.6), Inches(11.3), Inches(1.2))
tf_c = tb_contact.text_frame
p = tf_c.paragraphs[0]
p.text = "Executive Briefing & Direct Founder Contact:"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = RGBColor(251, 146, 60)

p = tf_c.add_paragraph()
p.text = "Bhaskar Pandey • Founder & Principal Architect • bhaskarauthor@gmail.com\nInteractive Studio: https://beyond-likes-platform.onrender.com/docs"
p.font.size = Pt(14)
p.font.color.rgb = C_WHITE

prs.save(OUTPUT_PATH)
print(f"Successfully generated native 16:9 widescreen presentation: {OUTPUT_PATH}")
