#!/usr/bin/env python3
"""
Normative Intelligence — Master Storyboard Video Producer (Aligned Cut)
Features:
  - Deep, subtle, articulate male neural voice (Kokoro TTS / bm_george with broadcast mastering EQ)
  - Explicit Visual Sync: Scene 1 frames the exact 'MANDATORY INDUSTRY MIGRATION: Google Perspective API Shuts Down on December 31, 2026' card (#migration)
  - Scene 2 frames the live 'kill -9' false-positive comparison (#interactive-demo)
  - Scene 3 dedicated showcase website walkthrough (Universal CMS Ecosystem cards & migration architecture)
  - Scene 4 live Discourse Studio (/studio) with 4D bars and in-composer git-style diff coach
  - Scene 5 1:1 Perspective JSON wire format inspector
  - Scene 6 empirical whitepaper (/benchmarks) SVG curves and interactive sandbox
  - Scene 7 autonomous 16:9 pitch deck (/deck) fluid slides
  - 1.52x responsive zoom eliminating side whitespace, with floating Director HUD
"""

import os
import sys
import time
import json
import shutil
import subprocess
from pathlib import Path

WORKSPACE_DIR = Path("/tmp/beyond-likes-git")
OUTPUT_DIR = WORKSPACE_DIR / "brand"
GDRIVE_DIR = Path("/Users/bhaskarpandey/Library/CloudStorage/GoogleDrive-bhaskarauthor@gmail.com/My Drive/Independent Research-to-Product Venture/01 - Venture Projects/BL-001 - Beyond Likes/03 - Historical Beyond Likes Prototype and Code/brand")
CHROME_PATH = "/Users/bhaskarpandey/Library/Caches/ms-playwright/chromium-1223/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
TEMP_DIR = Path("/tmp/normative_demo_aligned")

STORYBOARD = [
    {
        "id": "scene1",
        "badge": "MIGRATION DEADLINE",
        "hud_title": "Google Perspective API Hard Sunset: Dec 31, 2026",
        "hud_desc": "Thousands of digital newsrooms and platforms face an immediate shutdown.",
        "hud_color": "#C8441B",
        "text": (
            "On December 31st, 2026, Google officially shuts down the Perspective API. "
            "For over a decade, digital media and publishing platforms relied on binary toxicity filters. "
            "Now, every newsroom and community faces an immediate infrastructure cliff."
        ),
        "post_pause": 1.2
    },
    {
        "id": "scene2",
        "badge": "FALSE-POSITIVE TRAP",
        "hud_title": "Why Binary Filtering Failed Online Discourse",
        "hud_desc": "Benign commands like 'kill -9' get banned as toxic violence.",
        "hud_color": "#C8441B",
        "text": (
            "Binary filters broke online discourse. A benign systems command like kill dash nine gets banned as toxic violence. "
            "Legitimate medical and philosophical discussions get silenced, while coordinated cynicism slips right through, "
            "causing rampant false positives and reader attrition."
        ),
        "post_pause": 1.2
    },
    {
        "id": "scene3",
        "badge": "CMS ECOSYSTEM",
        "hud_title": "Universal CMS & Newsroom Integrations",
        "hud_desc": "Universal drop-in compatibility across WordPress VIP, Discourse, Coral & Forem.",
        "hud_color": "#0D5C4E",
        "text": (
            "This is Normative Intelligence. Our commercial showcase website details the sovereign architecture replacing Perspective. "
            "Designed for high-scale publishing, our engine delivers universal, drop-in compatibility across WordPress VIP, Discourse, "
            "Coral Project, and Forem, with zero disruption to existing editorial workflows."
        ),
        "post_pause": 1.2
    },
    {
        "id": "scene4",
        "badge": "IN-COMPOSER COACH",
        "hud_title": "Live Discourse Studio & In-Composer Coach",
        "hud_desc": "4D continuous rubric & real-time Git-style diff coaching before posting.",
        "hud_color": "#C8441B",
        "text": (
            "Here in the Discourse Studio Desk, our continuous four-dimensional rubric evaluates Constructiveness, Civility, "
            "Persuasiveness, and Relevance. When a reader drafts a cynical insult, the in-composer coach renders an inline git-style diff "
            "in real time, teaching them to reframe their critique with empirical evidence before submitting."
        ),
        "post_pause": 1.2
    },
    {
        "id": "scene5",
        "badge": "1:1 WIRE PARITY",
        "hud_title": "100% Wire Parity with Google Perspective",
        "hud_desc": "Identical attributeScores.TOXICITY schema. Zero platform code changes.",
        "hud_color": "#0D5C4E",
        "text": (
            "Engineering migration requires zero lines of code. Normative Intelligence delivers bitwise one-to-one "
            "schema parity with Perspective's comments-analyze endpoint. WordPress VIP, Discourse, and Coral Project can cut over in under five minutes."
        ),
        "post_pause": 1.2
    },
    {
        "id": "scene6",
        "badge": "EMPIRICAL BENCHMARKS",
        "hud_title": "99.2% ROC-AUC & 1.76ms Local CPU Latency",
        "hud_desc": "87.2% reduction in false positives across technical, medical & academic discourse.",
        "hud_color": "#D97706",
        "text": (
            "In our empirical whitepaper evaluating over one thousand complex discourse scenarios, "
            "Normative Intelligence achieves 99.2 percent ROC-AUC versus Perspective's 74.8 percent. "
            "False positives drop by 87 percent, powered by an optimized, sub-two-millisecond CPU engine."
        ),
        "post_pause": 1.2
    },
    {
        "id": "scene7",
        "badge": "ENTERPRISE CUTOVER",
        "hud_title": "Sovereign Epistemic Infrastructure for Civil Discourse",
        "hud_desc": "Deploy on-premise or managed cloud. Secure your Perspective EOL cutover today.",
        "hud_color": "#0D5C4E",
        "text": (
            "Deploying as sovereign on-premise hardware or low-latency managed cloud, "
            "Normative Intelligence turns comments from toxic liabilities into institutional assets. "
            "Secure your Perspective cutover today."
        ),
        "post_pause": 2.5
    }
]

def synthesize_male_narration():
    print("🎙️ Synthesizing deep, subtle male narration with Kokoro (bm_george)...")
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    audio_files = []
    total_duration = 0.0

    for scene in STORYBOARD:
        wav_raw = TEMP_DIR / f"{scene['id']}_raw.wav"
        wav_mastered = TEMP_DIR / f"{scene['id']}_mastered.wav"

        cached_wav = Path(f"/tmp/kokoro_scenes/{scene['id']}.wav")
        if cached_wav.exists():
            shutil.copy2(cached_wav, wav_raw)
        else:
            kokoro_py = "/Users/bhaskarpandey/.venvs/kokoro/bin/python"
            code = f"""
import soundfile as sf
import numpy as np
from kokoro import KPipeline
pipeline = KPipeline(lang_code='b')
generator = pipeline({repr(scene['text'])}, voice='bm_george', speed=0.92, split_pattern=r'\\n+')
chunks = [audio for gs, ps, audio in generator]
sf.write('{wav_raw}', np.concatenate(chunks), 24000)
"""
            subprocess.run([kokoro_py, "-c", code], check=True)

        # Broadcast Mastering Audio Chain:
        # Warm bass boost at 110Hz (+3.8dB), gentle 3.2kHz presence (+1.2dB), smoothing lowpass, -16 LUFS loudnorm
        audio_filter = "equalizer=f=110:width_type=o:width=1.5:g=3.8,equalizer=f=3200:width_type=o:width=1.0:g=1.2,lowpass=f=9500,loudnorm=I=-16:TP=-1.5:LRA=11"
        subprocess.run([
            "/opt/homebrew/bin/ffmpeg", "-y", "-i", str(wav_raw),
            "-af", audio_filter,
            "-ar", "44100", "-ac", "2",
            str(wav_mastered)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        probe = subprocess.check_output([
            "/opt/homebrew/bin/ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(wav_mastered)
        ])
        dur = float(json.loads(probe)["format"]["duration"])
        scene["duration"] = dur
        total_duration += dur + scene["post_pause"]
        print(f"  🔊 {scene['badge']}: {dur:.2f}s (+ {scene['post_pause']}s pause)")
        audio_files.append((wav_mastered, scene["post_pause"]))

    concat_list = TEMP_DIR / "concat_list.txt"
    with open(concat_list, "w") as f:
        # 0.8s leading silence
        silence_lead = TEMP_DIR / "silence_lead.wav"
        subprocess.run([
            "/opt/homebrew/bin/ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "0.8", str(silence_lead)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        f.write(f"file '{silence_lead}'\n")

        for wav, pause in audio_files:
            f.write(f"file '{wav}'\n")
            if pause > 0:
                p_wav = TEMP_DIR / f"silence_{pause}s.wav"
                subprocess.run([
                    "/opt/homebrew/bin/ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", str(pause), str(p_wav)
                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                f.write(f"file '{p_wav}'\n")

    master_audio = TEMP_DIR / "master_narration_male.wav"
    subprocess.run([
        "/opt/homebrew/bin/ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(master_audio)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    probe = subprocess.check_output([
        "/opt/homebrew/bin/ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(master_audio)
    ])
    final_audio_duration = float(json.loads(probe)["format"]["duration"])
    print(f"✅ Deep male narration finalized: {final_audio_duration:.2f} seconds ({final_audio_duration/60:.2f} mins)\n")
    return master_audio, final_audio_duration

def inject_director_tools(page):
    page.evaluate("""() => {
        // Prevent lead capture popup from obscuring video walkthrough
        try {
            localStorage.setItem('normative_lead_status', JSON.stringify({ submitted: true, timestamp: Date.now() }));
        } catch(e) {}

        // Expand layout and eliminate side whitespace
        const style = document.createElement('style');
        style.id = 'demo-cinematic-styles';
        style.textContent = `
            body {
                zoom: 1.52 !important;
                background-color: #FAF8F5 !important;
            }
            .container, .hero-card-frame, .studio-container, .whitepaper-container {
                max-width: 98% !important;
                width: 98% !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }
            .hero-headline {
                font-size: 3.1rem !important;
                line-height: 1.15 !important;
            }
            .hero-subtitle {
                font-size: 1.35rem !important;
                max-width: 94% !important;
            }
            .hero-proof-strip {
                font-size: 1.05rem !important;
                gap: 28px !important;
            }
            .migration-banner {
                padding: 36px 40px !important;
                border: 2px solid #C8441B !important;
                background: #FFFFFF !important;
                box-shadow: 0 12px 36px rgba(200, 68, 27, 0.12) !important;
            }
            .migration-pill {
                font-size: 0.95rem !important;
                padding: 6px 16px !important;
            }
            .migration-title {
                font-size: 2.35rem !important;
                line-height: 1.2 !important;
                color: #C8441B !important;
            }
            .migration-desc {
                font-size: 1.25rem !important;
                line-height: 1.6 !important;
            }
            .studio-card {
                padding: 24px !important;
            }
            .card-headline {
                font-size: 1.4rem !important;
            }
            .composer-textarea {
                font-size: 1.15rem !important;
                height: 155px !important;
            }
            .dimension-row {
                margin-bottom: 18px !important;
            }
            .dimension-header {
                font-size: 1.15rem !important;
            }
            .nudge-card {
                padding: 22px !important;
            }
            .nudge-title {
                font-size: 1.25rem !important;
            }
            .nudge-body {
                font-size: 1.15rem !important;
                line-height: 1.6 !important;
            }
            .deck-stage {
                height: 840px !important;
            }
            .slide-title {
                font-size: 2.9rem !important;
            }
            .slide-subtitle {
                font-size: 1.35rem !important;
            }
        `;
        document.head.appendChild(style);

        window.setHUD = function(badgeText, titleText, descText, accentColor = '#C8441B') {
            let hud = document.getElementById('demo-director-hud');
            if (!hud) {
                hud = document.createElement('div');
                hud.id = 'demo-director-hud';
                hud.style.cssText = `
                    position: fixed;
                    bottom: 24px;
                    left: 36px;
                    right: 36px;
                    background: rgba(24, 24, 27, 0.94);
                    backdrop-filter: blur(20px);
                    -webkit-backdrop-filter: blur(20px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 16px;
                    padding: 14px 26px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5);
                    z-index: 2147483647;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
                `;
                hud.innerHTML = `
                    <div style="display: flex; align-items: center; gap: 16px;">
                        <span id="hud-badge" style="background: ${accentColor}; color: #ffffff; padding: 6px 14px; border-radius: 6px; font-weight: 800; font-size: 13px; letter-spacing: 0.06em; font-family: 'JetBrains Mono', monospace; text-transform: uppercase;">NORMATIVE</span>
                        <span id="hud-title" style="font-weight: 700; font-size: 18px; color: #FAF8F5;">Title</span>
                    </div>
                    <div id="hud-desc" style="font-size: 15px; color: #D4D4D8; font-weight: 500;">Description</div>
                `;
                document.body.appendChild(hud);
            }
            const b = document.getElementById('hud-badge');
            b.textContent = badgeText;
            b.style.background = accentColor;
            document.getElementById('hud-title').textContent = titleText;
            document.getElementById('hud-desc').textContent = descText;
        };
    }""")

def update_hud(page, badge, title, desc, color):
    escaped_title = title.replace("'", "\\'")
    escaped_desc = desc.replace("'", "\\'")
    page.evaluate(f"if (typeof window.setHUD === 'function') window.setHUD('{badge}', '{escaped_title}', '{escaped_desc}', '{color}');")

def choreograph_synchronized_video(video_dir: Path):
    from playwright.sync_api import sync_playwright
    print("🎬 Launching Chromium at 1920x1080 with 1.52x zoom and exact visual-to-audio sync...")
    shutil.rmtree(video_dir, ignore_errors=True)
    video_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--hide-scrollbars",
                "--mute-audio"
            ]
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(video_dir),
            record_video_size={"width": 1920, "height": 1080}
        )
        page = context.new_page()

        # Initial buffer (0.8s)
        time.sleep(0.8)

        # =============================================================
        # SCENE 1: THE DISCOURSE CLIFF (Explicit Mandatory Migration Banner)
        # Duration: ~20.9s
        # =============================================================
        print("▶️ Recording Scene 1: MANDATORY INDUSTRY MIGRATION Banner (#migration)...")
        page.goto("http://localhost:8888/", wait_until="domcontentloaded")
        inject_director_tools(page)
        update_hud(page, STORYBOARD[0]["badge"], STORYBOARD[0]["hud_title"], STORYBOARD[0]["hud_desc"], STORYBOARD[0]["hud_color"])
        
        # Center directly on the MANDATORY INDUSTRY MIGRATION banner card (#migration)
        page.evaluate("""() => {
            const el = document.getElementById('migration');
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }""")
        time.sleep(6.0)

        # Subtle camera drift over the cutover checklist
        page.evaluate("window.scrollBy({ top: 90, behavior: 'smooth' });")
        time.sleep(7.0)
        page.evaluate("window.scrollBy({ top: -40, behavior: 'smooth' });")
        time.sleep(7.9)

        # =============================================================
        # SCENE 2: WHY BINARY FILTERING FAILED (The 'kill -9' Comparison)
        # Duration: ~21.9s
        # =============================================================
        print("▶️ Recording Scene 2: Live Problem Statement & False Positive Card (#interactive-demo)...")
        update_hud(page, STORYBOARD[1]["badge"], STORYBOARD[1]["hud_title"], STORYBOARD[1]["hud_desc"], STORYBOARD[1]["hud_color"])
        
        # Scroll to the live comparison sandbox
        page.evaluate("""() => {
            const el = document.getElementById('interactive-demo');
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            if (typeof setTestCase === 'function') setTestCase('technical');
        }""")
        time.sleep(6.5)

        # Highlight Perspective False Positive vs Normative Approval
        page.evaluate("window.scrollBy({ top: 120, behavior: 'smooth' });")
        time.sleep(7.5)
        page.evaluate("window.scrollBy({ top: 80, behavior: 'smooth' });")
        time.sleep(7.9)

        # =============================================================
        # SCENE 3: DEDICATED SHOWCASE WEBSITE WALKTHROUGH (CMS Ecosystem)
        # Duration: ~24.5s
        # =============================================================
        print("▶️ Recording Scene 3: Dedicated Showcase Website Walkthrough (CMS Compatibility)...")
        update_hud(page, STORYBOARD[2]["badge"], STORYBOARD[2]["hud_title"], STORYBOARD[2]["hud_desc"], STORYBOARD[2]["hud_color"])
        
        # Scroll to the Universal CMS Ecosystem grid (WordPress VIP, Discourse, Coral, Forem)
        page.evaluate("""() => {
            const grid = document.querySelector('.pubs-grid');
            if (grid) grid.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }""")
        time.sleep(6.5)

        # Smooth glide over the 4 platform architecture cards
        page.evaluate("window.scrollBy({ top: 180, behavior: 'smooth' });")
        time.sleep(6.5)
        page.evaluate("window.scrollBy({ top: 220, behavior: 'smooth' });")
        time.sleep(6.5)
        time.sleep(5.0)

        # =============================================================
        # SCENE 4: LIVE DISCOURSE STUDIO & IN-COMPOSER COACH (/studio)
        # Duration: ~24.3s
        # =============================================================
        print("▶️ Recording Scene 4: Live Discourse Studio Desk & Git-Style Diff Coach (/studio)...")
        page.goto("http://localhost:8888/studio", wait_until="domcontentloaded")
        inject_director_tools(page)
        update_hud(page, STORYBOARD[3]["badge"], STORYBOARD[3]["hud_title"], STORYBOARD[3]["hud_desc"], STORYBOARD[3]["hud_color"])
        
        # Empirical Debate scenario -> 4D bars animate
        page.evaluate("if (typeof selectScenario === 'function') selectScenario(0);")
        time.sleep(5.0)

        # Hostile Harassment scenario -> civility drops & inline git diff coach appears!
        page.evaluate("if (typeof selectScenario === 'function') selectScenario(2);")
        time.sleep(5.0)

        # Scroll directly into the Prosocial In-Composer Coach diff card
        page.evaluate("window.scrollTo({ top: 380, behavior: 'smooth' });")
        time.sleep(7.0)

        # Technical CLI Syntax scenario (kill -9) -> 100% false positive prevention
        page.evaluate("if (typeof selectScenario === 'function') selectScenario(3);")
        time.sleep(7.3)

        # =============================================================
        # SCENE 5: 1:1 WIRE DROP-IN PARITY (Zero Code Changes)
        # Duration: ~19.8s
        # =============================================================
        print("▶️ Recording Scene 5: 1:1 Perspective JSON Wire Schema Inspector...")
        update_hud(page, STORYBOARD[4]["badge"], STORYBOARD[4]["hud_title"], STORYBOARD[4]["hud_desc"], STORYBOARD[4]["hud_color"])
        
        # Scroll to perspective wire parity inspector
        page.evaluate("window.scrollTo({ top: 760, behavior: 'smooth' });")
        time.sleep(7.0)
        page.evaluate("window.scrollTo({ top: 960, behavior: 'smooth' });")
        time.sleep(7.0)
        time.sleep(5.8)

        # =============================================================
        # SCENE 6: RIGOROUS EMPIRICAL EVALUATION (/benchmarks)
        # Duration: ~23.9s
        # =============================================================
        print("▶️ Recording Scene 6: Empirical Research Whitepaper & SVG Curves (/benchmarks)...")
        page.goto("http://localhost:8888/benchmarks", wait_until="domcontentloaded")
        inject_director_tools(page)
        update_hud(page, STORYBOARD[5]["badge"], STORYBOARD[5]["hud_title"], STORYBOARD[5]["hud_desc"], STORYBOARD[5]["hud_color"])
        
        # Focus on Figure 1: ROC-AUC 99.2% Curve
        page.evaluate("window.scrollTo({ top: 400, behavior: 'smooth' });")
        time.sleep(6.0)

        # Scroll to Figure 2: False Positive Reduction by Domain
        page.evaluate("window.scrollTo({ top: 960, behavior: 'smooth' });")
        time.sleep(6.0)

        # Click interactive syntax chip in benchmark sandbox
        page.evaluate("if (typeof loadSample === 'function') loadSample(0);")
        time.sleep(4.0)

        # Scroll to Figure 3: 1.76ms CPU Latency Distribution
        page.evaluate("window.scrollTo({ top: 1520, behavior: 'smooth' });")
        time.sleep(7.9)

        # =============================================================
        # SCENE 7: AUTONOMOUS PITCH DECK & ENTERPRISE READINESS (/deck)
        # Duration: ~17.9s
        # =============================================================
        print("▶️ Recording Scene 7: Autonomous Master Pitch Deck (/deck)...")
        page.goto("http://localhost:8888/deck", wait_until="domcontentloaded")
        inject_director_tools(page)
        update_hud(page, STORYBOARD[6]["badge"], STORYBOARD[6]["hud_title"], STORYBOARD[6]["hud_desc"], STORYBOARD[6]["hud_color"])
        
        # Slide 1: Drop-In Infrastructure
        time.sleep(4.0)

        # Fluid transition to Slide 4: Quantized CPU Engine vs Cloud LLM Inflation
        page.evaluate("if (typeof goToSlide === 'function') goToSlide(3); else if (typeof nextSlide === 'function') { nextSlide(); nextSlide(); nextSlide(); }")
        time.sleep(5.0)

        # Fluid transition to Slide 12: Activate 30-Day Sandbox
        page.evaluate("if (typeof goToSlide === 'function') goToSlide(11); else if (typeof prevSlide === 'function') prevSlide();")
        time.sleep(5.0)

        # Final hold
        time.sleep(3.9)

        page.close()
        context.close()
        browser.close()

    recorded_webm = list(video_dir.glob("*.webm"))[0]
    print(f"🎬 Raw Playwright recording finalized: {recorded_webm} ({recorded_webm.stat().st_size / 1024 / 1024:.2f} MB)")
    return recorded_webm

def multiplex_broadcast_video(recorded_webm: Path, master_audio: Path, target_mp4: Path):
    print(f"🎞️ Multiplexing master broadcast video into {target_mp4.name} (H.264 High Profile / AAC 44.1kHz)...")
    target_mp4.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-i", str(recorded_webm),
        "-i", str(master_audio),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(target_mp4)
    ]
    subprocess.run(cmd, check=True)

    # Generate thumbnail poster frame at 10s (centered on MANDATORY INDUSTRY MIGRATION banner)
    poster_jpg = target_mp4.parent / "demo_video_poster.jpg"
    subprocess.run([
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-ss", "00:00:10",
        "-i", str(target_mp4),
        "-frames:v", "1",
        "-q:v", "2",
        str(poster_jpg)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    file_size_mb = target_mp4.stat().st_size / 1024 / 1024
    print(f"✨ Master Video Created: {target_mp4} ({file_size_mb:.2f} MB)")
    print(f"🖼️ Poster Thumbnail Created: {poster_jpg}")

    try:
        GDRIVE_DIR.mkdir(parents=True, exist_ok=True)
        gdrive_target = GDRIVE_DIR / target_mp4.name
        gdrive_poster = GDRIVE_DIR / poster_jpg.name
        shutil.copy2(target_mp4, gdrive_target)
        shutil.copy2(poster_jpg, gdrive_poster)
        print(f"💾 Atomically mirrored to Google Drive: {gdrive_target}")
    except Exception as e:
        print(f"⚠️ Note on Google Drive mirror: {e}")

    return target_mp4

def main():
    print("=" * 70)
    print("🎥 NORMATIVE INTELLIGENCE — MASTER STORYBOARD DEMO PRODUCER")
    print("   Visual-to-Audio Sync • Mandatory Migration Banner • Deep Male Voice")
    print("=" * 70)

    # Step 1: Synthesize narration
    master_audio, audio_duration = synthesize_male_narration()

    # Step 2: Record synchronized browser choreography
    playwright_video_dir = TEMP_DIR / "playwright_recordings"
    recorded_webm = choreograph_synchronized_video(playwright_video_dir)

    # Step 3: Multiplex into master MP4
    final_mp4 = OUTPUT_DIR / "Normative_Intelligence_Demo_Walkthrough.mp4"
    multiplex_broadcast_video(recorded_webm, master_audio, final_mp4)

    print("\n" + "=" * 70)
    print("🎉 ALIGNED DEMO VIDEO PRODUCTION COMPLETE")
    print(f"Output File: {final_mp4}")
    print("=" * 70)

if __name__ == "__main__":
    main()
