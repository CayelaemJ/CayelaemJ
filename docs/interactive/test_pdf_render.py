"""Detect visually blank OmniMaster book PDFs (requires poppler-utils).

The previous PDF had a valid header and extractable text but referenced its
*page* object as /F1 instead of a font. It therefore rendered as blank.
Visual rasterisation is the release gate, not just PDF byte signatures.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "docs/interactive/.static-publish/downloads/omnimaster-fullstack.pdf"


def run(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30
    )


def inspect_pgm(data: bytes) -> tuple[int, int, int]:
    # Poppler creates a P5 binary PGM image. Preserve binary after the header.
    match = re.match(rb"^P5\s+(\d+)\s+(\d+)\s+255\s", data)
    if not match:
        raise AssertionError("Unexpected Poppler PGM raster header")
    width, height = int(match.group(1)), int(match.group(2))
    pixels = data[match.end():]
    assert len(pixels) == width * height, "PGM payload size mismatch"
    visible = sum(value < 235 for value in pixels)
    return width, height, visible


def main() -> None:
    assert PDF.is_file(), f"PDF export is missing: {PDF}"
    for program in ("pdfinfo", "pdftoppm", "pdftotext"):
        assert shutil.which(program), f"Missing PDF rasteriser: {program}"
    source = PDF.read_bytes()
    assert source.startswith(b"%PDF-1."), "Invalid PDF header"
    assert len(source) > 12000, "Expected a multi-page textbook"
    # Explicitly catch the original incorrect resource reference.
    assert b"/F1 4 0 R" not in source, "PDF uses the page object as a font"
    assert b"/F1 3 0 R" in source, "PDF Helvetica resource missing"
    info = run("pdfinfo", str(PDF)).stdout.decode("utf-8", errors="replace")
    page_match = re.search(r"^Pages:\s+(\d+)\s*$", info, re.MULTILINE)
    assert page_match, "Could not read PDF page count"
    pages = int(page_match.group(1))
    assert pages >= 3, f"Unexpected textbook pagination: {pages}"

    extracted = run("pdftotext", "-layout", str(PDF), "-").stdout.decode(
        "utf-8", errors="replace"
    )
    for fragment in ("OMNIMASTER", "Frontend", "Backend", "data"):
        assert fragment.lower() in extracted.lower(), f"Missing rendered topic: {fragment}"

    with tempfile.TemporaryDirectory() as tmp:
        for page in sorted({1, max(2, pages // 2), pages}):
            destination = Path(tmp) / f"page-{page}"
            run(
                "pdftoppm", "-f", str(page), "-l", str(page),
                "-gray", "-scale-to", "650", "-singlefile",
                str(PDF), str(destination)
            )
            width, height, visible = inspect_pgm(
                destination.with_suffix(".pgm").read_bytes()
            )
            # An unreferenced font yields zero visible ink on every page.
            assert visible > 120, (
                f"Page {page}/{pages} visually blank: {visible} ink pixels "
                f"in {width}x{height} image"
            )
            print(f"PDF page {page}/{pages}: {visible} visible pixels ({width}x{height})")
    print(f"PDF VISUAL PASS: {pages} readable pages, text extraction and rendering verified.")


if __name__ == "__main__":
    main()
