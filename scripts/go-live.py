#!/usr/bin/env python3
"""Launch step: remove the staging noindex block from every HTML page.

Deletes everything between (and including) the marker comments
    <!-- STAGING-NOINDEX-START -->  ...  <!-- STAGING-NOINDEX-END -->
on every *.html page in the site root, then prints how many pages changed.
Run it once, on the day the site is deployed to https://www.hotelbluebells.com/.
Standard library only; preserves each file's line endings.

Usage:  python scripts/go-live.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BLOCK = re.compile(
    r"[ \t]*<!-- STAGING-NOINDEX-START -->.*?<!-- STAGING-NOINDEX-END -->[ \t]*(?:\r\n|\n)?",
    re.DOTALL,
)

changed = 0
pages = sorted(ROOT.glob("*.html"))
for page in pages:
    text = page.read_bytes().decode("utf-8")  # bytes: keep CRLF
    new, n = BLOCK.subn("", text)
    if n:
        page.write_bytes(new.encode("utf-8"))
        changed += 1
        print(f"  cleaned {page.name}")

print(f"\n{changed} of {len(pages)} pages changed.")
leftover = [p.name for p in pages if b"noindex" in p.read_bytes().lower()]
if leftover:
    print("WARNING: 'noindex' still present in: " + ", ".join(leftover))
    sys.exit(1)
