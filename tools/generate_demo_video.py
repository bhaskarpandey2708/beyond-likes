#!/usr/bin/env python3
"""
Normative Intelligence — High-Impact Storyboard Demo Video Generator
Features:
  - Deep, subtle, articulate male neural voice (Kokoro TTS / bm_george with broadcast mastering EQ)
  - Zero side margins: Page zoom 1.55x + 98% width expansion for crystal-clear readability on mobile/social
  - Exact beat-by-beat voice & visual synchronization across 7 storyboard acts
  - Dynamic Director HUD overlays rendered natively with frosted-glass typography
  - High-definition 1080p H.264 High Profile / AAC broadcast export
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
TEMP_DIR = Path("/tmp/normative_demo_build_v2")

STORYBOARD = [
    {
        "id": "scene1",
        "act_num": "ACT 1 • THE CATALYST",
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
        "act_num": "ACT 2 • THE CORE PROBLEM",
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
        "act_num": "ACT 3 • THE ARCHITECTURE",
        "hud_title": "4D Continuous Epistemic Normative Rubric",
        "hud_desc": "Constructiveness (35%), Civility (25%), Persuasiveness (20%), Relevance (20%).",
        "hud_color": "#0D5C4E",
        "text": (
            "Normative Intelligence introduces a radically superior paradigm. "
            "Instead of punitive binary bans, our continuous four-dimensional rubric evaluates Constructiveness, Civility, "
            "Persuasiveness, and Context Relevance. We elevate substantive discourse rather than censoring dissent."
        ),
        "post_pause": 1.2
    },
    {
        "id": "scene4",
        "act_num": "ACT 4 • THE AHA MOMENT",
        "hud_title": "In-Composer Pre-Submission Guidance",
        "hud_desc": "Real-time Git-style diff guides readers to reframe insults before posting.",
        "hud_color": "#C8441B",
        "text": (
            "The real breakthrough happens before submission. When a reader drafts a cynical insult, "
            "the in-composer coach intervenes in real time, rendering an inline git-style diff that guides the author to support "
            "their critique with empirical evidence, cutting moderator appeals by 35 percent."
        ),
        "post_pause": 1.2
    },
    {
        "id": "scene5",
        "act_num": "ACT 5 • TURNKEY PARITY",
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
        "act_num": "ACT 6 • EMPIRICAL PROOF",
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
        "act_num": "ACT 7 • THE FUTURE",
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

        # Check if already generated in cache
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

        # Apply Broadcast Mastering Audio Chain:
        # 1. Warm low-end presence boost (110Hz +3.5dB) for deep subtle resonance
        # 2. Presence contour (3.2kHz +1.2dB) for crystalline diction
        # 3. High-frequency smoothing filter
        # 4. ITU-R BS.1770 broadcast loudness normalization (-16 LUFS)
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
        print(f"  🔊 {scene['act_num']}: {dur:.2f}s (+ {scene['post_pause']}s pause)")
        audio_files.append((wav_mastered, scene["post_pause"]))

    # Assemble master concatenated audio track with silence padding
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
    """Injects responsive wide-canvas zoom and the Director HUD overlay."""
    page.evaluate("""() => {
        // 1. Expand layout and eliminate side whitespace
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

        // 2. Inject floating Director HUD Overlay
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
                        <span id="hud-badge" style="background: ${accentColor}; color: #ffffff; padding: 6px 14px; border-radius: 6px; font-weight: 800; font-size: 13px; letter-spacing: 0.06em; font-family: 'JetBrains Mono', monospace; text-transform: uppercase;">ACT</span>
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

def update_hud(page, act_num, title, desc, color):
    escaped_title = title.replace("'", "\\'")
    escaped_desc = desc.replace("'", "\\'")
    page.evaluate(f"if (typeof window.setHUD === 'function') window.setHUD('{act_num}', '{escaped_title}', '{escaped_desc}', '{color}');")

def choreograph_synchronized_video(video_dir: Path):
    from playwright.sync_api import sync_playwright
    print("🎬 Launching Chromium at 1920x1080 with 1.55x zoom and Director HUD...")
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
        # SCENE 1: THE DISCOURSE CLIFF (Perspective EOL Sunset)
        # Duration: ~20.9s
        # =============================================================
        print("▶️ Recording Scene 1: Perspective EOL Sunset...")
        page.goto("http://localhost:8888/", wait_until="networkidle")
        inject_director_tools(page)
        update_hud(page, STORYBOARD[0]["act_num"], STORYBOARD[0]["hud_title"], STORYBOARD[0]["hud_desc"], STORYBOARD[0]["hud_color"])
        
        # Center tight on the hero & perspective sunset banner
        page.evaluate("window.scrollTo({ top: 40, behavior: 'smooth' });")
        time.sleep(5.0)

        # Pulse scroll through the hero narrative
        page.evaluate("window.scrollTo({ top: 180, behavior: 'smooth' });")
        time.sleep(5.0)
        page.evaluate("window.scrollTo({ top: 380, behavior: 'smooth' });")
        time.sleep(6.0)
        time.sleep(4.9)

        # =============================================================
        # SCENE 2: WHY BINARY FILTERING FAILED (False Positives)
        # Duration: ~21.9s
        # =============================================================
        print("▶️ Recording Scene 2: The Core Problem — Binary False Positives...")
        update_hud(page, STORYBOARD[1]["act_num"], STORYBOARD[1]["hud_title"], STORYBOARD[1]["hud_desc"], STORYBOARD[1]["hud_color"])
        
        # Scroll to the live problem statement & comparison
        page.evaluate("window.scrollTo({ top: 720, behavior: 'smooth' });")
        time.sleep(5.5)
        page.evaluate("window.scrollTo({ top: 1100, behavior: 'smooth' });")
        time.sleep(6.0)
        page.evaluate("window.scrollTo({ top: 1450, behavior: 'smooth' });")
        time.sleep(6.0)
        time.sleep(4.4)

        # =============================================================
        # SCENE 3: THE 4D CONTINUOUS NORMATIVE RUBRIC (/studio)
        # Duration: ~21.5s
        # =============================================================
        print("▶️ Recording Scene 3: The 4D Continuous Normative Rubric (/studio)...")
        page.goto("http://localhost:8888/studio", wait_until="networkidle")
        inject_director_tools(page)
        update_hud(page, STORYBOARD[2]["act_num"], STORYBOARD[2]["hud_title"], STORYBOARD[2]["hud_desc"], STORYBOARD[2]["hud_color"])
        
        # Focus on Empirical Debate & 4D Progress bars
        page.evaluate("if (typeof selectScenario === 'function') selectScenario(0);")
        time.sleep(5.0)
        page.evaluate("window.scrollTo({ top: 120, behavior: 'smooth' });")
        time.sleep(6.0)
        page.evaluate("window.scrollTo({ top: 220, behavior: 'smooth' });")
        time.sleep(6.0)
        time.sleep(4.5)

        # =============================================================
        # SCENE 4: IN-COMPOSER PROSOCIAL COACHING (The "Aha!" Moment)
        # Duration: ~22.0s
        # =============================================================
        print("▶️ Recording Scene 4: In-Composer Prosocial Diff Coaching...")
        update_hud(page, STORYBOARD[3]["act_num"], STORYBOARD[3]["hud_title"], STORYBOARD[3]["hud_desc"], STORYBOARD[3]["hud_color"])
        
        # Select Hostile Harassment -> shows live diff coaching!
        page.evaluate("if (typeof selectScenario === 'function') selectScenario(2);")
        time.sleep(5.5)

        # Scroll directly into the Prosocial In-Composer Coach diff card
        page.evaluate("window.scrollTo({ top: 380, behavior: 'smooth' });")
        time.sleep(6.0)

        # Select Technical CLI Syntax (kill -9 $(pgrep nginx)) to prove false-positive prevention
        page.evaluate("if (typeof selectScenario === 'function') selectScenario(3);")
        time.sleep(6.0)
        time.sleep(4.5)

        # =============================================================
        # SCENE 5: 1:1 WIRE DROP-IN PARITY (Zero Code Changes)
        # Duration: ~19.8s
        # =============================================================
        print("▶️ Recording Scene 5: 100% Bitwise Perspective Wire Parity...")
        update_hud(page, STORYBOARD[4]["act_num"], STORYBOARD[4]["hud_title"], STORYBOARD[4]["hud_desc"], STORYBOARD[4]["hud_color"])
        
        # Scroll to perspective wire inspector & ecosystem cards
        page.evaluate("window.scrollTo({ top: 680, behavior: 'smooth' });")
        time.sleep(6.5)
        page.evaluate("window.scrollTo({ top: 920, behavior: 'smooth' });")
        time.sleep(7.0)
        time.sleep(6.3)

        # =============================================================
        # SCENE 6: RIGOROUS EMPIRICAL EVALUATION (/benchmarks)
        # Duration: ~23.9s
        # =============================================================
        print("▶️ Recording Scene 6: Empirical Whitepaper & SVG Visualizations (/benchmarks)...")
        page.goto("http://localhost:8888/benchmarks", wait_until="networkidle")
        inject_director_tools(page)
        update_hud(page, STORYBOARD[5]["act_num"], STORYBOARD[5]["hud_title"], STORYBOARD[5]["hud_desc"], STORYBOARD[5]["hud_color"])
        
        # Focus on Figure 1: ROC-AUC 99.2% Curve
        page.evaluate("window.scrollTo({ top: 380, behavior: 'smooth' });")
        time.sleep(6.0)

        # Scroll to Figure 2: False Positive Reduction
        page.evaluate("window.scrollTo({ top: 920, behavior: 'smooth' });")
        time.sleep(6.0)

        # Click interactive syntax chip in benchmark sandbox
        page.evaluate("if (typeof loadSample === 'function') loadSample(0);")
        time.sleep(4.0)

        # Scroll to Figure 3: 1.76ms CPU Latency Distribution
        page.evaluate("window.scrollTo({ top: 1480, behavior: 'smooth' });")
        time.sleep(6.0)
        time.sleep(1.9)

        # =============================================================
        # SCENE 7: AUTONOMOUS PITCH DECK & SOVEREIGN FUTURE (/deck)
        # Duration: ~17.9s
        # =============================================================
        print("▶️ Recording Scene 7: Autonomous Master Pitch Deck (/deck)...")
        page.goto("http://localhost:8888/deck", wait_until="networkidle")
        inject_director_tools(page)
        update_hud(page, STORYBOARD[6]["act_num"], STORYBOARD[6]["hud_title"], STORYBOARD[6]["hud_desc"], STORYBOARD[6]["hud_color"])
        
        # Slide 1: Drop-In Infrastructure
        time.sleep(4.0)

        # Advance to Slide 4: Quantized CPU Engine vs Cloud LLM Inflation
        page.evaluate("if (typeof goToSlide === 'function') goToSlide(3); else if (typeof nextSlide === 'function') { nextSlide(); nextSlide(); nextSlide(); }")
        time.sleep(5.0)

        # Advance to Slide 12: Activate 30-Day Sandbox
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

    # Generate thumbnail poster frame at 14s
    poster_jpg = target_mp4.parent / "demo_video_poster.jpg"
    subprocess.run([
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-ss", "00:00:16",
        "-i", str(target_mp4),
        "-frames:v", "1",
        "-q:v", "2",
        str(poster_jpg)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    file_size_mb = target_mp4.stat().st_size / 1024 / 1024
    print(f"✨ Master Video Created: {target_mp4} ({file_size_mb:.2f} MB)")
    print(f"🖼️ Poster Thumbnail Created: {poster_jpg}")

    # Mirror to Google Drive workspace directory
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
    print("🎥 NORMATIVE INTELLIGENCE — STORYBOARD DEMO WALKTHROUGH PRODUCER")
    print("   Deep Male Narration • Zero Side Margins • Full Screen 1080p")
    print("=" * 70)

    # Step 1: Synthesize deep, subtle male voiceover
    master_audio, audio_duration = synthesize_male_narration()

    # Step 2: Record synchronized browser choreography with Director HUD & Zoom
    playwright_video_dir = TEMP_DIR / "playwright_recordings"
    recorded_webm = choreograph_synchronized_video(playwright_video_dir)

    # Step 3: Multiplex into master MP4
    final_mp4 = OUTPUT_DIR / "Normative_Intelligence_Demo_Walkthrough.mp4"
    multiplex_broadcast_video(recorded_webm, master_audio, final_mp4)

    print("\n" + "=" * 70)
    print("🎉 HIGH-IMPACT DEMO VIDEO PRODUCTION COMPLETE")
    print(f"Output File: {final_mp4}")
    print("=" * 70)

if __name__ == "__main__":
    main()
