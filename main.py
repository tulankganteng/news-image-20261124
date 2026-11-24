#!/usr/bin/env python3
"""Write the entry image to the output directory.

Copies the repository's ``entry.png`` to ``/output/entry.png`` (or
to ``$MAKEFUN_OUTPUT_DIR`` for local runs), validates it is a
1024x1024 PNG, then reads the copy back and checks it matches the
source byte for byte (SHA-256). No network, no clock, no randomness.

The image itself ("The World Today", Tuesday 24 November 2026:
40 dated stories across 8 regions, timeline strip, world map with
pins, 12 pictured stories, day-in-numbers box, "left out" box) is
pre-rendered and shipped as ``entry.png``. This script uses only
the standard library so it runs in the grader's pinned image.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = Path("/output")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1024 * 1024


def output_path() -> Path:
    """Where the finished image goes for this run."""
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    directory = Path(override) if override else DEFAULT_OUTPUT_DIR
    return directory / SOURCE_NAME


def sha256_hex(data: bytes) -> str:
    """Hex digest of a byte string."""
    return hashlib.sha256(data).hexdigest()


def check_png(data: bytes) -> tuple[int, int]:
    """Confirm the bytes are a 1024x1024 PNG under the size limit.

    Returns the image dimensions. Raises ValueError with a plain
    explanation when the check fails.
    """
    if data[:8] != PNG_SIGNATURE:
        raise ValueError("not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(
            f"image is {width}x{height}, expected "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )
    if len(data) > MAX_BYTES:
        raise ValueError(f"image is {len(data)} bytes, over the 1 MiB limit")
    return width, height


def main() -> int:
    source = Path(__file__).resolve().parent / SOURCE_NAME
    if not source.is_file():
        print(f"error: {source} not found", file=sys.stderr)
        return 1

    original = source.read_bytes()
    try:
        width, height = check_png(original)
    except ValueError as exc:
        print(f"error: {SOURCE_NAME} invalid: {exc}", file=sys.stderr)
        return 1
    digest = sha256_hex(original)

    destination = output_path()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(original)

    written = destination.read_bytes()
    if sha256_hex(written) != digest:
        print("error: copy does not match the source", file=sys.stderr)
        return 1

    print(
        f"wrote {destination} ({len(written)} bytes, "
        f"{width}x{height} PNG, sha256 {digest[:16]}...)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
