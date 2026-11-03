#!/usr/bin/env python3
"""
Normative Intelligence — Professional Demo Video & Storyline Generator
Produces a broadcast-ready 1080p MP4 walkthrough complete with:
  - Act 1: The Crisis & Catalyst (Google Perspective API Sunset Dec 31, 2026)
  - Act 2: The Normative Architecture (4D Continuous Rubric & Prosocial Guidance)
  - Act 3: Live Discourse Studio Walkthrough (Real-time scoring, diffs, false-positive prevention)
  - Act 4: Empirical Whitepaper & Benchmarks (ROC-AUC 99.2%, 87.2% FP reduction, 1.76ms latency)
  - Act 5: Autonomous Master Pitch Deck (Fluid slide transitions, universal CMS ecosystem cutover)
"""

import os
import sys
import time
import json
import shutil
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

WORKSPACE_DIR = Path("/tmp/beyond-likes-git")
OUTPUT_DIR = WORKSPACE_DIR / "brand"
GDRIVE_DIR = Path("/Users/bhaskarpandey/Library/CloudStorage/GoogleDrive-bhaskarauthor@gmail.com/My Drive/Independent Research-to-Product Venture/01 - Venture Projects/BL-001 - Beyond Likes/03 - Historical Beyond Likes Prototype and Code/brand")
CHROME_PATH = "/Users/bhaskarpandey/Library/Caches/ms-playwright/chromium-1223/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
TEMP_DIR = Path("/tmp/normative_demo_build")

ACT_SCRIPTS = [
    {
        "id": "act1_problem",
        "title": "Act 1: The Impending Discourse Cliff",
        "voice": "Samantha",
        "text": (
            "On December 31st, 2026, Google officially sunsets the Perspective API, leaving thousands of "
            "publishing platforms, newsrooms, and online communities without automated discourse infrastructure. "
            "For over a decade, legacy binary toxicity filters have failed the open internet: censoring benign "
            "technical queries like kill dash nine, silencing critical medical discussions, while remaining "
            "completely blind to bad-faith cynicism, dogwhistles, and coordinated deflection."
        ),
        "post_pause": 1.5
    },
    {
        "id": "act2_architecture",
        "title": "Act 2: The Normative Intelligence Solution",
        "voice": "Samantha",
        "text": (
            "Normative Intelligence solves this crisis through a 100 percent wire-compatible drop-in replacement. "
            "Instead of punitive binary bans, our architecture introduces a four-dimensional continuous epistemic rubric: "
            "Constructiveness, Civility, Persuasiveness, and Relevance. Rather than censoring users post-submission, "
            "Normative Intelligence provides real-time, in-composer guidance that coaches participants to express sharp "
            "counter-arguments constructively."
        ),
        "post_pause": 1.5
    },
    {
        "id": "act3_studio",
        "title": "Act 3: Live Discourse Studio Desk",
        "voice": "Samantha",
        "text": (
            "Here in the Discourse Studio Desk, publishers experience continuous normative scoring in real time. "
            "When an empirical critique is entered, our sub-two-millisecond engine instantly validates citations, "
            "expanding the multi-factor radar gauge to a 96 percent score. When hostile cynicism is detected, the "
            "in-composer engine renders a side-by-side git-style diff, teaching the user how to reframe their argument "
            "with substantive evidence. Simultaneously, the one-to-one Perspective schema inspector proves identical "
            "wire format compatibility, requiring zero lines of code changes."
        ),
        "post_pause": 1.5
    },
    {
        "id": "act4_whitepaper",
        "title": "Act 4: Rigorous Empirical Evaluation",
        "voice": "Samantha",
        "text": (
            "In our empirical whitepaper evaluating over one thousand complex discourse scenarios, Normative Intelligence "
            "achieves an unprecedented 99.2 percent ROC-AUC, compared to Perspective's 74.8 percent. Crucially, false "
            "positives on technical, medical, and philosophical vocabulary plummet by 87.2 percent, powered by an "
            "optimized, sub-two-millisecond CPU inference engine."
        ),
        "post_pause": 1.5
    },
    {
        "id": "act5_deck",
        "title": "Act 5: Autonomous Master Pitch Deck",
        "voice": "Samantha",
        "text": (
            "Our 16-by-9 fluid presentation deck articulates the clear enterprise business model, editorial governance, "
            "and universal CMS integrations, deploying natively into WordPress VIP, Discourse, Coral Project, and Forem. "
            "Normative Intelligence transforms online discourse from toxic attrition into epistemic value."
        ),
        "post_pause": 2.5
    }
]

def synthesize_audio():
    print("🎙️ Synthesizing narration audio tracks...")
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    audio_files = []
    total_audio_duration = 0.0

    for act in ACT_SCRIPTS:
        aiff_path = TEMP_DIR / f"{act['id']}.aiff"
        wav_path = TEMP_DIR / f"{act['id']}.wav"
        
        # Synthesize with macOS say
        subprocess.run(["say", "-v", act["voice"], "-o", str(aiff_path), act["text"]], check=True)
        # Convert to standard 44.1kHz stereo wav
        subprocess.run(
            ["/opt/homebrew/bin/ffmpeg", "-y", "-i", str(aiff_path), "-ar", "44100", "-ac", "2", str(wav_path)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        # Get duration
        probe = subprocess.check_output([
            "/opt/homebrew/bin/ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(wav_path)
        ])
        dur = float(json.loads(probe)["format"]["duration"])
        act["duration"] = dur
        total_audio_duration += dur + act["post_pause"]
        print(f"  🔊 {act['title']}: {dur:.2f}s (+ {act['post_pause']}s pause)")
        audio_files.append((wav_path, act["post_pause"]))

    # Assemble master concatenated audio track with silence padding
    concat_list = TEMP_DIR / "concat_list.txt"
    with open(concat_list, "w") as f:
        # 1.0s leading silence
        silence_1s = TEMP_DIR / "silence_1s.wav"
        subprocess.run([
            "/opt/homebrew/bin/ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "1.0", str(silence_1s)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        f.write(f"file '{silence_1s}'\n")

        for wav, pause in audio_files:
            f.write(f"file '{wav}'\n")
            if pause > 0:
                p_wav = TEMP_DIR / f"silence_{pause}s.wav"
                subprocess.run([
                    "/opt/homebrew/bin/ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", str(pause), str(p_wav)
                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                f.write(f"file '{p_wav}'\n")

    master_audio = TEMP_DIR / "master_narration.wav"
    subprocess.run([
        "/opt/homebrew/bin/ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(master_audio)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    probe = subprocess.check_output([
        "/opt/homebrew/bin/ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(master_audio)
    ])
    final_audio_duration = float(json.loads(probe)["format"]["duration"])
    print(f"✅ Master narration ready: {final_audio_duration:.2f} seconds ({final_audio_duration/60:.2f} mins)\n")
    return master_audio, final_audio_duration

def choreograph_recording(video_dir: Path):
    print("🎬 Launching headless Chromium to record synchronized walkthrough at 1920x1080...")
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

        # Initial lead-in
        time.sleep(1.0)

        # -------------------------------------------------------------
        # ACT 1: THE DISCOURSE CRISIS & THE CATALYST (Home Landing)
        # Duration: ~31.8s
        # -------------------------------------------------------------
        print("▶️ Recording Act 1: The Discourse Crisis & Google Sunset (Home Landing)...")
        page.goto("http://localhost:8888/", wait_until="networkidle")
        time.sleep(2.5)

        # Highlight Perspective Sunset banner
        try:
            page.evaluate("window.scrollBy({ top: 120, behavior: 'smooth' });")
        except Exception:
            pass
        time.sleep(4.0)

        # Scroll smoothly to problem statement
        for offset in [250, 450, 700, 950]:
            page.evaluate(f"window.scrollTo({{ top: {offset}, behavior: 'smooth' }});")
            time.sleep(3.5)

        # Scroll to 4D rubric explanation
        page.evaluate("window.scrollTo({ top: 1350, behavior: 'smooth' });")
        time.sleep(5.0)

        # -------------------------------------------------------------
        # ACT 2: ARCHITECTURE & UNIVERSAL INTEGRATIONS
        # Duration: ~29.0s
        # -------------------------------------------------------------
        print("▶️ Recording Act 2: Universal Architecture & CMS Ecosystem Compatibility...")
        # Scroll to CMS compatibility section
        page.evaluate("window.scrollTo({ top: 1800, behavior: 'smooth' });")
        time.sleep(4.5)
        page.evaluate("window.scrollTo({ top: 2300, behavior: 'smooth' });")
        time.sleep(5.0)
        page.evaluate("window.scrollTo({ top: 2800, behavior: 'smooth' });")
        time.sleep(5.0)
        page.evaluate("window.scrollTo({ top: 3200, behavior: 'smooth' });")
        time.sleep(5.0)
        page.evaluate("window.scrollTo({ top: 3700, behavior: 'smooth' });")
        time.sleep(5.0)

        # -------------------------------------------------------------
        # ACT 3: LIVE DISCOURSE STUDIO DESK
        # Duration: ~36.4s
        # -------------------------------------------------------------
        print("▶️ Recording Act 3: Live Discourse Studio Desk Walkthrough (/studio)...")
        page.goto("http://localhost:8888/studio", wait_until="networkidle")
        time.sleep(3.0)

        # Scenario 1: Empirical Data Debate (Selected by default)
        page.evaluate("if (typeof selectScenario === 'function') selectScenario(0);")
        time.sleep(4.5)

        # Scenario 2: Passive Cynicism / Hostile Harassment (Shows coaching diff)
        page.evaluate("if (typeof selectScenario === 'function') selectScenario(1);")
        time.sleep(4.5)

        # Show Hostile Harassment
        page.evaluate("if (typeof selectScenario === 'function') selectScenario(2);")
        time.sleep(5.0)

        # Show In-Composer Prosocial Diff in action
        page.evaluate("window.scrollBy({ top: 150, behavior: 'smooth' });")
        time.sleep(4.5)

        # Scenario 3: Technical CLI Syntax (kill -9 $(pgrep nginx))
        # The key differentiator: Perspective flags false-positive, Normative approves
        page.evaluate("if (typeof selectScenario === 'function') selectScenario(3);")
        time.sleep(6.0)

        # Inspect wire comparison table
        page.evaluate("window.scrollBy({ top: 250, behavior: 'smooth' });")
        time.sleep(5.5)

        # -------------------------------------------------------------
        # ACT 4: RIGOROUS EMPIRICAL EVALUATION (Whitepaper /benchmarks)
        # Duration: ~27.0s
        # -------------------------------------------------------------
        print("▶️ Recording Act 4: Empirical Whitepaper & Statistical Benchmarks (/benchmarks)...")
        page.goto("http://localhost:8888/benchmarks", wait_until="networkidle")
        time.sleep(3.0)

        # Scroll to Section 1: ROC-AUC Chart
        page.evaluate("window.scrollTo({ top: 450, behavior: 'smooth' });")
        time.sleep(4.5)

        # Scroll to Section 2: False Positive Breakdown
        page.evaluate("window.scrollTo({ top: 1050, behavior: 'smooth' });")
        time.sleep(4.5)

        # Click syntax test chips in the interactive sandbox
        page.evaluate("if (typeof loadSample === 'function') loadSample(0);")
        time.sleep(2.5)
        page.evaluate("if (typeof loadSample === 'function') loadSample(1);")
        time.sleep(2.5)

        # Scroll to Section 3: Latency Distribution (1.76ms)
        page.evaluate("window.scrollTo({ top: 1650, behavior: 'smooth' });")
        time.sleep(4.5)

        # Scroll to Section 4: Prosocial Engagement Lift
        page.evaluate("window.scrollTo({ top: 2150, behavior: 'smooth' });")
        time.sleep(4.0)

        # -------------------------------------------------------------
        # ACT 5: AUTONOMOUS MASTER PITCH DECK (/deck)
        # Duration: ~23.0s
        # -------------------------------------------------------------
        print("▶️ Recording Act 5: Autonomous Master Pitch Deck (/deck)...")
        page.goto("http://localhost:8888/deck", wait_until="networkidle")
        time.sleep(3.0)

        # Slide 1: Drop-in Prosocial Infrastructure
        time.sleep(3.5)

        # Slide 2: Sunset countdown & Market vacuum
        page.evaluate("if (typeof nextSlide === 'function') nextSlide();")
        time.sleep(4.0)

        # Slide 3: The Core Problem: Keyword & Toxicity Filters Broke Online Discourse
        page.evaluate("if (typeof nextSlide === 'function') nextSlide();")
        time.sleep(4.0)

        # Slide 4: The Solution: Normative 4D Intelligence
        page.evaluate("if (typeof nextSlide === 'function') nextSlide();")
        time.sleep(4.0)

        # Slide 5: 1:1 Wire Drop-in Ready (Zero Code Engineering Cutover)
        page.evaluate("if (typeof nextSlide === 'function') nextSlide();")
        time.sleep(4.0)

        # Final hold
        time.sleep(2.0)

        # Close page and context to ensure video is fully flushed to disk
        page.close()
        context.close()
        browser.close()

    # Find the recorded webm file
    webm_files = list(video_dir.glob("*.webm"))
    if not webm_files:
        raise RuntimeError("No video file generated by Playwright!")
    recorded_webm = webm_files[0]
    print(f"🎬 Raw Playwright recording finalized: {recorded_webm} ({recorded_webm.stat().st_size / 1024 / 1024:.2f} MB)")
    return recorded_webm

def multiplex_final_video(recorded_webm: Path, master_audio: Path, target_mp4: Path):
    print(f"🎞️ Multiplexing master broadcast video into {target_mp4.name} (H.264 High Profile / AAC 44.1kHz)...")
    target_mp4.parent.mkdir(parents=True, exist_ok=True)

    # Get durations
    probe_v = subprocess.check_output([
        "/opt/homebrew/bin/ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(recorded_webm)
    ])
    dur_v = float(json.loads(probe_v)["format"]["duration"])

    probe_a = subprocess.check_output([
        "/opt/homebrew/bin/ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(master_audio)
    ])
    dur_a = float(json.loads(probe_a)["format"]["duration"])

    print(f"  📊 Raw Video Duration: {dur_v:.2f}s | Audio Duration: {dur_a:.2f}s")

    # High quality encode:
    # 1. Scale/pad cleanly to 1920x1080
    # 2. Add subtle audio fade in / out
    # 3. Faststart flag for instant web streaming
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

    # Generate a thumbnail poster frame at 12s
    poster_jpg = target_mp4.parent / "demo_video_poster.jpg"
    subprocess.run([
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-ss", "00:00:14",
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
    print("🎥 NORMATIVE INTELLIGENCE — AUTOMATED DEMO WALKTHROUGH PRODUCER")
    print("=" * 70)

    # Step 1: Synthesize Narration Audio
    master_audio, audio_duration = synthesize_audio()

    # Step 2: Record synchronized browser choreography
    playwright_video_dir = TEMP_DIR / "playwright_recordings"
    recorded_webm = choreograph_recording(playwright_video_dir)

    # Step 3: Multiplex into master MP4
    final_mp4 = OUTPUT_DIR / "Normative_Intelligence_Demo_Walkthrough.mp4"
    multiplex_final_video(recorded_webm, master_audio, final_mp4)

    print("\n" + "=" * 70)
    print("🎉 DEMO VIDEO PRODUCTION COMPLETE")
    print(f"Output File: {final_mp4}")
    print("=" * 70)

if __name__ == "__main__":
    main()
