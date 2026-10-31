#!/usr/bin/env python3
"""
Continuous Conversation & Solution History Sync Daemon
======================================================
Automatically extracts conversation transcripts, user instructions,
technical reasoning, and milestones every 600 seconds (10 minutes),
persisting all conversation transcripts and summaries into `docs/conversations/`,
updating `docs/CONVERSATION_HISTORY.md`, `CONVERSATION_LOGS.md`, and `AGENT.md`,
and synchronizing the entire venture workspace to Google Drive.

Usage:
  # One-shot sync:
  python3 tools/continuous_sync_daemon.py --once

  # Continuous 10-minute daemon:
  python3 tools/continuous_sync_daemon.py --daemon --interval 600
"""

import os
import sys
import json
import time
import argparse
import subprocess
import shutil
import re
from datetime import datetime
from typing import List, Dict, Any, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED_GDRIVE_DIR = "/home/ayush-pandey/GoogleDrive/RESEARCH_TO_PRODUCT_VENTURE"
APP_DATA_DIR = os.path.expanduser("~/.gemini/antigravity-cli")
LOG_FILE = os.path.join(BASE_DIR, "storage", "sync_daemon.log")

TARGET_DOC = os.path.join(BASE_DIR, "docs", "CONVERSATION_HISTORY.md")
CONVOS_DIR = os.path.join(BASE_DIR, "docs", "conversations")
TARGET_CONVO_LOG = os.path.join(BASE_DIR, "CONVERSATION_LOGS.md")
TARGET_AGENT_MD = os.path.join(BASE_DIR, "AGENT.md")
TARGET_PROJECT_MEMORY = os.path.join(BASE_DIR, "PROJECT_MEMORY.md")

VENTURE_KEYWORDS = [
    "RESEARCH_TO_PRODUCT_VENTURE",
    "Beyond Likes",
    "EECS-2025-55",
    "Perspective",
    "deberta-v3-large",
    "Ayush Pandey",
    "bhaskarauthor@gmail.com"
]

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
    line = f"[{timestamp}] {msg}"
    print(line)
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def clean_tags(text: str) -> str:
    """Strips internal system XML-style tags for clean readable documentation."""
    if not text:
        return ""
    text = re.sub(r"<USER_REQUEST>", "", text)
    text = re.sub(r"</USER_REQUEST>", "", text)
    text = re.sub(r"<ADDITIONAL_METADATA>[\s\S]*?</ADDITIONAL_METADATA>", "", text)
    text = re.sub(r"<USER_SETTINGS_CHANGE>[\s\S]*?</USER_SETTINGS_CHANGE>", "", text)
    text = re.sub(r"<SYSTEM_MESSAGE>[\s\S]*?</SYSTEM_MESSAGE>", "", text)
    text = re.sub(r"<CONTEXT_SUMMARY>[\s\S]*?</CONTEXT_SUMMARY>", "", text)
    return text.strip()

def find_all_venture_conversations() -> List[Tuple[str, str, float]]:
    """
    Scans APP_DATA_DIR/brain for all conversations that belong to this venture.
    Returns list of tuples: (convo_id, transcript_path, mtime), sorted newest first.
    """
    brain_dir = os.path.join(APP_DATA_DIR, "brain")
    if not os.path.exists(brain_dir):
        return []

    venture_convos = []
    for d in os.listdir(brain_dir):
        tpath = os.path.join(brain_dir, d, ".system_generated", "logs", "transcript.jsonl")
        if os.path.exists(tpath):
            try:
                # Sample first 20KB to check venture relevance
                with open(tpath, "r", encoding="utf-8", errors="ignore") as f:
                    sample = f.read(25000)
                is_venture = any(k in sample for k in VENTURE_KEYWORDS)
                if is_venture:
                    mtime = os.path.getmtime(tpath)
                    venture_convos.append((d, tpath, mtime))
            except Exception:
                continue

    venture_convos.sort(key=lambda x: x[2], reverse=True)
    return venture_convos

def parse_transcript(transcript_path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(transcript_path):
        return []

    records = []
    with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                records.append(data)
            except Exception:
                continue
    return records

def format_conversation_turns(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    user_turns = []
    current_turn = None

    for r in records:
        rtype = r.get("type", "")
        source = r.get("source", "")
        content = r.get("content", "") or ""
        created_at = r.get("created_at", "")
        step_idx = r.get("step_index", 0)

        if source == "USER_EXPLICIT" or rtype == "USER_INPUT":
            clean_prompt = clean_tags(content)
            if clean_prompt:
                if current_turn:
                    user_turns.append(current_turn)
                current_turn = {
                    "step": step_idx,
                    "timestamp": created_at,
                    "prompt": clean_prompt,
                    "actions": [],
                    "model_responses": []
                }
        elif current_turn:
            tool_calls = r.get("tool_calls", [])
            for tc in tool_calls:
                tname = tc.get("name", "")
                args = tc.get("args", {})
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception:
                        args = {}
                summary = args.get("toolSummary", tname)
                current_turn["actions"].append({
                    "tool": tname,
                    "summary": summary,
                    "timestamp": created_at
                })
            if rtype == "PLANNER_RESPONSE" and content:
                clean_resp = clean_tags(content)
                if clean_resp:
                    current_turn["model_responses"].append(clean_resp)

    if current_turn:
        user_turns.append(current_turn)

    return user_turns

def format_single_conversation_md(convo_id: str, turns: List[Dict[str, Any]], mtime: float) -> str:
    mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S IST")
    md = []
    md.append(f"# Conversation Session Archive: `{convo_id}`")
    md.append(f"*Session Timestamp: {mtime_str} | Turns Logged: {len(turns)}*\n")
    md.append("This document records the turn-by-turn dialogue, tool executions, and technical milestones for this session.\n")
    md.append("---\n")

    for idx, turn in enumerate(turns, start=1):
        ts = turn.get("timestamp", "N/A")
        prompt = turn.get("prompt", "").replace("\n", "\n> ")
        md.append(f"### Turn {idx}: [{ts}] User Directive")
        md.append(f"> {prompt}\n")

        actions = turn.get("actions", [])
        if actions:
            md.append("#### Engineering Actions & Tool Implementations:")
            seen_actions = set()
            for act in actions:
                summary = act.get("summary") or act.get("tool")
                if summary not in seen_actions:
                    md.append(f"- `[{act.get('tool')}]` {summary}")
                    seen_actions.add(summary)
            md.append("")

        responses = turn.get("model_responses", [])
        if responses:
            md.append("#### Solution Synthesis & Key Deliverables:")
            for resp in responses:
                lines = resp.strip().split("\n")
                snippet = "\n".join(lines[:25])
                md.append(f"{snippet}\n")

        md.append("---\n")

    return "\n".join(md)

def sync_all_conversations(venture_convos: List[Tuple[str, str, float]]):
    """
    Archives every conversation transcript and generates individual markdown summaries.
    """
    os.makedirs(CONVOS_DIR, exist_ok=True)
    archived_meta = []

    for convo_id, tpath, mtime in venture_convos:
        # 1. Copy raw JSONL transcript
        dest_jsonl = os.path.join(CONVOS_DIR, f"{convo_id}_transcript.jsonl")
        try:
            shutil.copy2(tpath, dest_jsonl)
        except Exception as e:
            log(f"Warning copying {tpath} -> {dest_jsonl}: {e}")

        # 2. Parse and generate summary markdown
        records = parse_transcript(tpath)
        turns = format_conversation_turns(records)
        summary_md = format_single_conversation_md(convo_id, turns, mtime)
        dest_md = os.path.join(CONVOS_DIR, f"{convo_id}_summary.md")
        try:
            with open(dest_md, "w", encoding="utf-8") as f:
                f.write(summary_md)
        except Exception as e:
            log(f"Warning writing {dest_md}: {e}")

        archived_meta.append({
            "convo_id": convo_id,
            "turns": len(turns),
            "events": len(records),
            "mtime": mtime,
            "mtime_str": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S IST"),
            "relative_md": f"conversations/{convo_id}_summary.md",
            "relative_jsonl": f"conversations/{convo_id}_transcript.jsonl"
        })

    # 3. Generate Master Index in docs/CONVERSATION_HISTORY.md
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
    master_md = []
    master_md.append("# Project Conversation & Solution Evolution Master Chronicle")
    master_md.append(f"*Automated Sync Timestamp: {now_str} | Total Sessions Archived: `{len(archived_meta)}`*\n")
    master_md.append("This document tracks all recorded dialogue sessions, architectural decisions, and tool executions for the **Beyond Likes Venture (BL-001)**.\n")
    master_md.append("---\n")

    master_md.append("## 1. Archived Sessions Master Registry\n")
    master_md.append("| # | Session / Conversation ID | Last Active (IST) | User Turns | Total Events | Documentation Link | Raw Transcript |")
    master_md.append("| :-: | :--- | :---: | :---: | :---: | :--- | :--- |")

    for idx, m in enumerate(archived_meta, 1):
        status_tag = " **(Active)**" if idx == 1 else ""
        master_md.append(f"| {idx} | `{m['convo_id']}`{status_tag} | {m['mtime_str']} | `{m['turns']}` turns | `{m['events']}` events | [View Summary]({m['relative_md']}) | [Download JSONL]({m['relative_jsonl']}) |")

    master_md.append("\n---\n")

    # Include detailed turn breakdown of the currently active session
    if archived_meta:
        active = archived_meta[0]
        master_md.append(f"## 2. Active Session Turn Breakdown (`{active['convo_id']}`)\n")
        active_tpath = os.path.join(CONVOS_DIR, f"{active['convo_id']}_summary.md")
        if os.path.exists(active_tpath):
            with open(active_tpath, "r", encoding="utf-8") as f:
                content = f.read()
            # strip title
            lines = content.splitlines()
            body = "\n".join(lines[4:])
            master_md.append(body)

    with open(TARGET_DOC, "w", encoding="utf-8") as f:
        f.write("\n".join(master_md))

    log(f"Updated {TARGET_DOC} and archived {len(archived_meta)} conversation sessions in {CONVOS_DIR}")
    return archived_meta

def update_agent_md(archived_count: int, active_convo_id: str):
    """Updates the Last Synced timestamp and conversation count in AGENT.md."""
    if not os.path.exists(TARGET_AGENT_MD):
        return
    try:
        with open(TARGET_AGENT_MD, "r", encoding="utf-8") as f:
            content = f.read()
        now_str = datetime.now().strftime("%B %d, %Y at %I:%M:%S %p IST")
        new_content = re.sub(
            r"\*\*Last Updated:\*\*.*",
            f"**Last Updated:** {now_str} (Automated 600s Daemon Sync | {archived_count} Sessions Preserved | Active: `{active_convo_id}`)",
            content
        )
        with open(TARGET_AGENT_MD, "w", encoding="utf-8") as f:
            f.write(new_content)
        log(f"Updated {TARGET_AGENT_MD} timestamp and session metadata.")
    except Exception as e:
        log(f"Warning updating AGENT.md: {e}")

def run_cloud_sync():
    """
    Executes synchronization to BOTH:
    1. Local Google Drive mirror: /home/ayush-pandey/GoogleDrive/RESEARCH_TO_PRODUCT_VENTURE
    2. Original Shared Folder from Bhaskar Pandey (bhaskarauthor@gmail.com):
       'Independent Research-to-Product Venture'
    """
    # 1. Local GDrive mirror rsync
    if not os.path.exists(SHARED_GDRIVE_DIR):
        os.makedirs(SHARED_GDRIVE_DIR, exist_ok=True)

    cmd_local = [
        "rsync",
        "-avh",
        "--delete",
        "--exclude", ".venv",
        "--exclude", ".venv_py312",
        "--exclude", "__pycache__",
        "--exclude", "*.pyc",
        "--exclude", ".git",
        f"{BASE_DIR}/",
        f"{SHARED_GDRIVE_DIR}/"
    ]
    try:
        res = subprocess.run(cmd_local, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        out_line = res.stdout.splitlines()[-1] if res.stdout else "OK"
        log(f"✅ Local Google Drive mirror rsync complete: {out_line}")
    except subprocess.CalledProcessError as e:
        log(f"❌ Error during local rsync: {e.stderr}")

    # 2. Sync to Original Shared Folder (bhaskarauthor@gmail.com) via rclone
    remote_shared_base = "gdrive:Independent Research-to-Product Venture"
    remote_venture_dir = f"{remote_shared_base}/RESEARCH_TO_PRODUCT_VENTURE"
    
    # 2a. Sync codebase & docs (excluding venvs, pycache, models)
    rclone_cmd = [
        "rclone", "copy",
        f"{BASE_DIR}/",
        remote_venture_dir,
        "--drive-shared-with-me",
        "--exclude", ".venv/**",
        "--exclude", ".venv_py312/**",
        "--exclude", "__pycache__/**",
        "--exclude", "*.pyc",
        "--exclude", ".git/**",
        "--exclude", "models/**",
        "--fast-list",
        "--transfers", "4",
        "--checkers", "8"
    ]
    try:
        subprocess.run(rclone_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=180)
        log(f"✅ Synced codebase & docs to shared folder: {remote_venture_dir}")
    except Exception as e:
        log(f"⚠️ Warning syncing to shared folder {remote_venture_dir}: {e}")

    # 2b. Sync executive summary deliverables into numbered folders
    try:
        # 01 - Beyond Likes Case
        rclone_c1 = [
            "rclone", "copy", f"{BASE_DIR}/",
            f"{remote_shared_base}/01 - Beyond Likes Case",
            "--drive-shared-with-me",
            "--include", "AGENT.md",
            "--include", "PROJECT_MEMORY.md",
            "--include", "CONVERSATION_LOGS.md",
            "--include", "docs/CONVERSATION_HISTORY.md",
            "--fast-list"
        ]
        subprocess.run(rclone_c1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)

        # 02 - Market and Customers
        rclone_c2 = [
            "rclone", "copy", f"{BASE_DIR}/validation",
            f"{remote_shared_base}/02 - Market and Customers",
            "--drive-shared-with-me",
            "--include", "social_launch_campaign.md",
            "--include", "social_campaign_status.md",
            "--include", "social_expansion_campaign.md",
            "--include", "buyer_shortlist.md",
            "--fast-list"
        ]
        subprocess.run(rclone_c2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)

        # 03 - Pipeline and Decision Records
        rclone_c3 = [
            "rclone", "copy", f"{BASE_DIR}/validation",
            f"{remote_shared_base}/03 - Pipeline and Decision Records",
            "--drive-shared-with-me",
            "--include", "campaign_status_report.md",
            "--fast-list"
        ]
        subprocess.run(rclone_c3, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)

        rclone_proposals = [
            "rclone", "copy", f"{BASE_DIR}/proposals",
            f"{remote_shared_base}/03 - Pipeline and Decision Records/proposals",
            "--drive-shared-with-me",
            "--include", "*.md",
            "--fast-list"
        ]
        subprocess.run(rclone_proposals, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
        log(f"✅ Mirrored executive deliverables into 01, 02, and 03 folders in {remote_shared_base}")
    except Exception as e:
        log(f"⚠️ Warning mirroring executive deliverables: {e}")

    return True

def sync_all():
    """Performs full sync cycle: all conversations, docs, agent.md, and cloud mirror."""
    venture_convos = find_all_venture_conversations()
    active_id = venture_convos[0][0] if venture_convos else "none"
    log(f"Starting 600-second sync cycle across {len(venture_convos)} venture sessions (active: {active_id})...")

    archived_meta = sync_all_conversations(venture_convos)
    update_agent_md(len(archived_meta), active_id)
    run_cloud_sync()
    log("🏁 Full 600-second sync cycle completed successfully.")

def run_daemon(interval_sec: int = 600):
    log(f"🚀 Starting Continuous Sync Daemon (interval: {interval_sec}s / {interval_sec//60} mins)...")
    sync_all()
    while True:
        try:
            time.sleep(interval_sec)
            sync_all()
        except KeyboardInterrupt:
            log("🛑 Continuous Sync Daemon stopped by user.")
            break
        except Exception as e:
            log(f"⚠️ Exception during sync cycle: {e}")
            time.sleep(10)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize conversation history and mirror to Google Drive every 600 seconds.")
    parser.add_argument("--once", action="store_true", help="Run a single sync cycle and exit")
    parser.add_argument("--daemon", action="store_true", help="Run continuously in the background")
    parser.add_argument("--interval", type=int, default=600, help="Sync interval in seconds (default: 600)")
    args = parser.parse_args()

    if args.once or not args.daemon:
        sync_all()
    else:
        run_daemon(args.interval)
