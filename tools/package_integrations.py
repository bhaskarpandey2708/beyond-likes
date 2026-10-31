#!/usr/bin/env python3
"""
Integration Packager for Beyond Likes Distribution Suite
Packages Chrome Extension, WordPress Plugin, Discourse Plugin, and Universal Widget
into production-ready zip bundles for enterprise download.
"""

import os
import sys
import zipfile
from typing import Dict, Any, List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
DISTRIBUTION_DIR = os.path.join(BASE_DIR, "distribution")
VERSION = "2.8.0"


PACKAGES = {
    "chrome-extension": {
        "name": "Beyond Likes In-Composer Chrome Extension",
        "filename": f"beyond-likes-chrome-extension-v{VERSION}.zip",
        "source_dir": os.path.join(DISTRIBUTION_DIR, "chrome_extension"),
        "description": "Manifest V3 floating prosocial feedback composer assistant for Chrome, Brave, and Edge.",
        "install_guide": "Extract zip, open chrome://extensions, enable 'Developer Mode', and click 'Load unpacked'."
    },
    "wordpress-plugin": {
        "name": "Beyond Likes WordPress Moderation Plugin",
        "filename": f"beyond-likes-wordpress-plugin-v{VERSION}.zip",
        "source_dir": os.path.join(DISTRIBUTION_DIR, "wordpress_plugin"),
        "description": "Native WordPress comment pre-moderation filter with instant webhook dispatch.",
        "install_guide": "Upload zip file directly into WordPress Admin > Plugins > Add New > Upload Plugin."
    },
    "discourse-plugin": {
        "name": "Beyond Likes Discourse AI Plugin",
        "filename": f"beyond-likes-discourse-plugin-v{VERSION}.zip",
        "source_dir": os.path.join(DISTRIBUTION_DIR, "discourse_plugin"),
        "description": "Official Discourse forum plugin connecting new post events to automated normative triage.",
        "install_guide": "Add git repository or extract zip into discourse/plugins/beyond-likes and rebuild container."
    },
    "widget": {
        "name": "Beyond Likes Universal Script Widget",
        "filename": f"beyond-likes-widget-v{VERSION}.zip",
        "source_dir": os.path.join(DISTRIBUTION_DIR, "widget"),
        "description": "Zero-dependency vanilla JavaScript drop-in widget for custom blogs, React, Next.js, and static sites.",
        "install_guide": "Include <script src='https://api.beyondlikes.io/widget/beyond-likes.js'></script> in page footer."
    }
}


def package_directory(source_dir: str, output_zip: str):
    """Recursively zip a directory preserving relative paths."""
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                z.write(file_path, arcname)


def build_all_packages() -> List[Dict[str, Any]]:
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    results = []

    for pkg_id, meta in PACKAGES.items():
        out_path = os.path.join(DOWNLOADS_DIR, meta["filename"])
        package_directory(meta["source_dir"], out_path)
        size_bytes = os.path.getsize(out_path)
        results.append({
            "id": pkg_id,
            "name": meta["name"],
            "filename": meta["filename"],
            "path": out_path,
            "size_kb": round(size_bytes / 1024, 2),
            "description": meta["description"],
            "install_guide": meta["install_guide"],
            "download_url": f"/v1/downloads/{pkg_id}"
        })

    return results


def main():
    print("\n" + "="*80)
    print("📦 BEYOND LIKES: INTEGRATION DISTRIBUTION PACKAGER")
    print("="*80 + "\n")

    pkgs = build_all_packages()
    for p in pkgs:
        print(f"✅ Packaged: {p['name']}")
        print(f"   - File: {p['filename']} ({p['size_kb']} KB)")
        print(f"   - URL: {p['download_url']}\n")

    print("="*80)
    print(f"🎉 All {len(pkgs)} distribution packages compiled in {DOWNLOADS_DIR}")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
