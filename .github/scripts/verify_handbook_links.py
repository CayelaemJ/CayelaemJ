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
    ROOT / "docs/OMNIMASTER_BUILD_WITH_ME.md",
    ROOT / "docs/OMNIMASTER_HUMAN_INTERFACE.md",
)
ARCADE = ROOT / "docs/OMNIMASTER_ARCADE.md"
STUDY_INDEX = ROOT / "projects/README.md"
GAME_README = ROOT / "projects/omnimaster-incident-academy/README.md"
GAME = ROOT / "projects/omnimaster-incident-academy/quest.py"
TEST = ROOT / "projects/omnimaster-incident-academy/test_quest.py"
CAPSTONE = ROOT / "projects/data-to-decision-platform/engine.py"
CAPSTONE_TEST = ROOT / "projects/data-to-decision-platform/test_engine.py"
CAPSTONE_README = ROOT / "projects/data-to-decision-platform/README.md"
EXPEDITION = ROOT / "docs/THIRTY_DAY_ENGINEERING_EXPEDITION.md"
STUDY_ROOM = ROOT / "docs/interactive/index.html"
STUDY_ROOM_TEST = ROOT / "docs/interactive/test_study_room.py"
STUDY_ROOM_README = ROOT / "docs/interactive/README.md"
GROUPS = (
    (ROOT / "docs/handbook", 10, "Chapter", VOLUMES[0], True),
    (ROOT / "docs/field-guide", 5, "Field Guide", VOLUMES[1], True),
    (ROOT / "docs/academy", 7, "Lesson", VOLUMES[2], False),
    (ROOT / "docs/personal", 4, "Personal Chapter", VOLUMES[3], False),
    (ROOT / "docs/build-with-me", 6, "Build With Me", VOLUMES[4], False),
    (ROOT / "docs/human-interface", 6, "Human Interface", VOLUMES[5], False),
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
    required = (COVER, *VOLUMES, ARCADE, STUDY_INDEX, GAME_README, GAME, TEST,
                CAPSTONE, CAPSTONE_TEST, CAPSTONE_README, EXPEDITION,
                STUDY_ROOM, STUDY_ROOM_TEST, STUDY_ROOM_README)
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
    project_index = STUDY_INDEX.read_text(encoding="utf-8")
    if "omnimaster-incident-academy/" not in project_index:
        errors.append("Project index omits playable game")
    if "data-to-decision-platform/" not in project_index:
        errors.append("Project index omits runnable end-to-end capstone")
    for target in ("docs/THIRTY_DAY_ENGINEERING_EXPEDITION.md",
                   "docs/interactive/index.html", "projects/data-to-decision-platform/"):
        if target not in cover:
            errors.append(f"Profile cover omits {target}")

    for i, content in enumerate(indexes):
        if i != 0 and "OMNIMASTER_HANDBOOK.md" not in content:
            errors.append(f"{VOLUMES[i].name} must link back to Volume I")
    if "OMNIMASTER_ACADEMY.md" not in indexes[0] or "OMNIMASTER_OPERATING_MANUAL.md" not in indexes[0] or "OMNIMASTER_BUILD_WITH_ME.md" not in indexes[0] or "OMNIMASTER_HUMAN_INTERFACE.md" not in indexes[0]:
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

    if "https://omnimaster-study-room.cabo-solutions-za.workers.dev/" not in cover:
        errors.append("Profile cover does not link to the deployed Study Room")
    if "docs/interactive/index.html" not in cover:
        errors.append("Profile cover must retain a labelled source link")
    if "OMNIMASTER_HUMAN_INTERFACE.md" not in STUDY_ROOM.read_text(encoding="utf-8"):
        errors.append("Interactive Study Room must link to Volume VI")

    for document in (COVER, *VOLUMES, ARCADE, STUDY_INDEX, GAME_README,
                     CAPSTONE_README, EXPEDITION, STUDY_ROOM_README, *all_sections):
        local_links(document, errors)
    return errors


if __name__ == "__main__":
    errors = verify()
    if errors:
        for problem in errors:
            print("ERROR:", problem, file=sys.stderr)
        sys.exit(1)
    print("OmniMaster navigation passed: 6 volumes, 10 handbook chapters, "
          "5 field guides, 7 academy lessons, 4 personal chapters, "
          "6 build-with-me lessons, 6 UX chapters, live Study Room link, and demos.")
