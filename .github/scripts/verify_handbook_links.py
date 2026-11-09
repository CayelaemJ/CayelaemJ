"""Check that the public OmniMaster handbook is complete and locally navigable.

Runs offline, using only the Python standard library. External URLs and anchors
inside already-existing documents are not validated here.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "docs" / "OMNIMASTER_HANDBOOK.md"
COVER = ROOT / "README.md"
CHAPTER_DIR = ROOT / "docs" / "handbook"
LINK = re.compile(r'(?<!!)\[[^\]]+\]\(([^)]+)\)')
CHAPTER_HEADING = re.compile(r"^# Chapter (\d\d) \| ", re.MULTILINE)


def verify() -> list[str]:
    problems: list[str] = []
    chapters = sorted(CHAPTER_DIR.glob("[0-9][0-9]_*.md"))
    if len(chapters) != 10:
        problems.append(f"Expected 10 chapters, found {len(chapters)}")
    for expected, chapter in enumerate(chapters, start=1):
        prefix = f"{expected:02d}_"
        if not chapter.name.startswith(prefix):
            problems.append(f"Missing chapter {expected:02d}: found {chapter.name}")

    if not INDEX.is_file() or not COVER.is_file():
        return problems + ["Handbook index or profile cover is missing"]

    index_content = INDEX.read_text(encoding="utf-8")
    cover_content = COVER.read_text(encoding="utf-8")
    if "docs/OMNIMASTER_HANDBOOK.md" not in cover_content:
        problems.append("Profile cover must link to the handbook index")

    for chapter in chapters:
        chapter_relative = f"handbook/{chapter.name}"
        cover_relative = f"docs/handbook/{chapter.name}"
        if chapter_relative not in index_content:
            problems.append(f"Handbook index omits {chapter_relative}")
        if cover_relative not in cover_content:
            problems.append(f"Profile cover omits {cover_relative}")
        actual_numbers = CHAPTER_HEADING.findall(chapter.read_text(encoding="utf-8"))
        if actual_numbers != [chapter.name[:2]]:
            problems.append(f"{chapter.name}: expected one matching Chapter heading")

    for document in [INDEX, *chapters]:
        content = document.read_text(encoding="utf-8")
        for match in LINK.finditer(content):
            raw = match.group(1).strip()
            if raw.startswith("<") and raw.endswith(">"):
                raw = raw[1:-1]
            # No spaces/titles in our internal handbook links.
            parsed = urlsplit(raw)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (document.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(ROOT):
                problems.append(f"{document.relative_to(ROOT)}: escaped repository: {raw}")
            elif not target.exists():
                problems.append(f"{document.relative_to(ROOT)}: broken link: {raw}")

    return problems


if __name__ == "__main__":
    failures = verify()
    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        sys.exit(1)
    print("Handbook validated: 10 chapters, cover/index navigation, and local links.")
