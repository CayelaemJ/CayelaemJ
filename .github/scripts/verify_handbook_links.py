"""Offline integrity checks for both OmniMaster textbook volumes.

Only validates local Markdown paths, navigation completeness and chapter structure.
External URLs, historical companion-doc links and GitHub-rendered anchors are not
certified by this checker.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
COVER = ROOT / "README.md"
VOLUME_ONE = ROOT / "docs" / "OMNIMASTER_HANDBOOK.md"
VOLUME_TWO = ROOT / "docs" / "OMNIMASTER_FIELD_GUIDE.md"
CHAPTERS = ROOT / "docs" / "handbook"
FIELD_GUIDE = ROOT / "docs" / "field-guide"
MARKDOWN_LINK = re.compile(r'(?<!!)\[[^\]]+\]\(([^)]+)\)')
CHAPTER_HEADING = re.compile(r"^# Chapter (\d\d) \| ", re.MULTILINE)
GUIDE_HEADING = re.compile(r"^# Field Guide (\d\d) \| ", re.MULTILINE)


def numbered_files(directory: Path, expected: int, label: str, issues: list[str]) -> list[Path]:
    files = sorted(directory.glob("[0-9][0-9]_*.md"))
    if len(files) != expected:
        issues.append(f"{label}: expected {expected} files, found {len(files)}")
    for expected_number, file in enumerate(files, start=1):
        if not file.name.startswith(f"{expected_number:02d}_"):
            issues.append(f"{label}: sequence mismatch at {file.name}")
    return files


def validate_local_links(document: Path, issues: list[str]) -> None:
    source = document.read_text(encoding="utf-8")
    for match in MARKDOWN_LINK.finditer(source):
        raw = match.group(1).strip()
        if raw.startswith("<") and raw.endswith(">"):
            raw = raw[1:-1]
        parsed = urlsplit(raw)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = (document.parent / unquote(parsed.path)).resolve()
        if not target.is_relative_to(ROOT):
            issues.append(f"{document.relative_to(ROOT)}: path outside repo: {raw}")
        elif not target.exists():
            issues.append(f"{document.relative_to(ROOT)}: broken link: {raw}")


def verify() -> list[str]:
    issues: list[str] = []
    for required in (COVER, VOLUME_ONE, VOLUME_TWO):
        if not required.is_file():
            issues.append(f"Required index missing: {required.relative_to(ROOT)}")
    if issues:
        return issues

    cover = COVER.read_text(encoding="utf-8")
    main = VOLUME_ONE.read_text(encoding="utf-8")
    field = VOLUME_TWO.read_text(encoding="utf-8")
    for target in ("docs/OMNIMASTER_HANDBOOK.md", "docs/OMNIMASTER_FIELD_GUIDE.md"):
        if target not in cover:
            issues.append(f"GitHub profile cover must link to {target}")
    if "OMNIMASTER_FIELD_GUIDE.md" not in main:
        issues.append("Volume I must link to Volume II")
    if "OMNIMASTER_HANDBOOK.md" not in field:
        issues.append("Volume II must link to Volume I")

    chapters = numbered_files(CHAPTERS, 10, "Volume I", issues)
    guide_files = numbered_files(FIELD_GUIDE, 5, "Volume II", issues)

    for file in chapters:
        content = file.read_text(encoding="utf-8")
        if f"handbook/{file.name}" not in main or f"docs/handbook/{file.name}" not in cover:
            issues.append(f"Chapter not discoverable from both indexes: {file.name}")
        if CHAPTER_HEADING.findall(content) != [file.name[:2]]:
            issues.append(f"Chapter heading does not match filename: {file.name}")

    for file in guide_files:
        content = file.read_text(encoding="utf-8")
        if f"field-guide/{file.name}" not in field or f"docs/field-guide/{file.name}" not in cover:
            issues.append(f"Field guide not discoverable from both indexes: {file.name}")
        if GUIDE_HEADING.findall(content) != [file.name[:2]]:
            issues.append(f"Field guide heading does not match filename: {file.name}")

    for document in (COVER, VOLUME_ONE, VOLUME_TWO, *chapters, *guide_files):
        validate_local_links(document, issues)

    return issues


if __name__ == "__main__":
    errors = verify()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
    print("Textbook checks passed: 2 volumes, 10 chapters, 5 field guides, local links.")
