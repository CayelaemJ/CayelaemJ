"""Validate navigation for the OmniMaster library and synthetic learning projects.

Offline standard-library checker. Does NOT validate external URLs, CI outcomes
or GitHub-generated Markdown heading anchors.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
COVER = ROOT / "README.md"
VOLUMES = (
    ROOT / "docs/OMNIMASTER_HANDBOOK.md",
    ROOT / "docs/OMNIMASTER_FIELD_GUIDE.md",
    ROOT / "docs/OMNIMASTER_ACADEMY.md",
    ROOT / "docs/OMNIMASTER_OPERATING_MANUAL.md",
)
ARCADE = ROOT / "docs/OMNIMASTER_ARCADE.md"
STUDY_INDEX = ROOT / "projects/README.md"
GAME_README = ROOT / "projects/omnimaster-incident-academy/README.md"
GAME = ROOT / "projects/omnimaster-incident-academy/quest.py"
TEST = ROOT / "projects/omnimaster-incident-academy/test_quest.py"
GROUPS = (
    (ROOT / "docs/handbook", 10, "Chapter", VOLUMES[0], True),
    (ROOT / "docs/field-guide", 5, "Field Guide", VOLUMES[1], True),
    (ROOT / "docs/academy", 7, "Lesson", VOLUMES[2], False),
    (ROOT / "docs/personal", 4, "Personal Chapter", VOLUMES[3], False),
)
MARKDOWN_LINK = re.compile(r'(?<!!)\[[^\]]+\]\(([^)]+)\)')


def local_links(document: Path, errors: list[str]) -> None:
    for match in MARKDOWN_LINK.finditer(document.read_text(encoding="utf-8")):
        raw = match.group(1).strip()
        if raw.startswith("<") and raw.endswith(">"):
            raw = raw[1:-1]
        parsed = urlsplit(raw)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = (document.parent / unquote(parsed.path)).resolve()
        if not target.is_relative_to(ROOT):
            errors.append(f"{document.relative_to(ROOT)}: path escapes repository: {raw}")
        elif not target.exists():
            errors.append(f"{document.relative_to(ROOT)}: broken local link: {raw}")


def verify() -> list[str]:
    errors: list[str] = []
    required = (COVER, *VOLUMES, ARCADE, STUDY_INDEX, GAME_README, GAME, TEST)
    for document in required:
        if not document.is_file():
            errors.append(f"Missing required file: {document.relative_to(ROOT)}")
    if errors:
        return errors

    cover = COVER.read_text(encoding="utf-8")
    indexes = [doc.read_text(encoding="utf-8") for doc in VOLUMES]

    for index in VOLUMES:
        if f"docs/{index.name}" not in cover:
            errors.append(f"Profile cover does not advertise {index.name}")
    if "docs/OMNIMASTER_ARCADE.md" not in cover:
        errors.append("Profile cover does not advertise the Arcade")
    if "projects/omnimaster-incident-academy" not in cover:
        errors.append("Profile cover omits the playable game")
    if "omnimaster-incident-academy/" not in STUDY_INDEX.read_text(encoding="utf-8"):
        errors.append("Project index omits playable game")

    for i, content in enumerate(indexes):
        if i != 0 and "OMNIMASTER_HANDBOOK.md" not in content:
            errors.append(f"{VOLUMES[i].name} must link back to Volume I")
    if "OMNIMASTER_ACADEMY.md" not in indexes[0] or "OMNIMASTER_OPERATING_MANUAL.md" not in indexes[0]:
        errors.append("Volume I must link forward to the new volumes")

    all_sections: list[Path] = []
    for directory, count, title, index, require_cover_sections in GROUPS:
        files = sorted(directory.glob("[0-9][0-9]_*.md"))
        if len(files) != count:
            errors.append(f"{title}: expected {count} sections, found {len(files)}")
        index_text = index.read_text(encoding="utf-8")
        for number, file in enumerate(files, 1):
            expected_prefix = f"{number:02d}_"
            if not file.name.startswith(expected_prefix):
                errors.append(f"{title}: nonsequential filename {file.name}")
            body = file.read_text(encoding="utf-8")
            if not re.search(rf"^# {re.escape(title)} {number:02d} \| ", body, re.MULTILINE):
                errors.append(f"{title}: heading does not match {file.name}")
            short = f"{directory.name}/{file.name}"
            if short not in index_text:
                errors.append(f"{index.name}: does not link to {short}")
            if require_cover_sections and f"docs/{short}" not in cover:
                errors.append(f"Profile cover does not link to {short}")
        all_sections.extend(files)

    for document in (COVER, *VOLUMES, ARCADE, STUDY_INDEX, GAME_README, *all_sections):
        local_links(document, errors)
    return errors


if __name__ == "__main__":
    errors = verify()
    if errors:
        for problem in errors:
            print("ERROR:", problem, file=sys.stderr)
        sys.exit(1)
    print("OmniMaster navigation passed: 4 volumes, 10 handbook chapters, "
          "5 field guides, 7 academy lessons, 4 personal chapters, arcade and game.")
