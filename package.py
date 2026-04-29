#!/usr/bin/env python3
"""
Build privacy-audit.skill from source.
Usage: python package.py
"""

import zipfile
import os
from pathlib import Path

SKILL_DIR = Path("privacy-audit")
OUTPUT_FILE = Path("privacy-audit.skill")

def package():
    files = []
    for path in SKILL_DIR.rglob("*"):
        if path.is_file():
            files.append(path)

    with zipfile.ZipFile(OUTPUT_FILE, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, f.relative_to(SKILL_DIR.parent))
            print(f"  Added: {f.relative_to(SKILL_DIR.parent)}")

    print(f"\n✅ Packaged → {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size // 1024}KB)")

if __name__ == "__main__":
    package()
