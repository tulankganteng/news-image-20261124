#!/usr/bin/env python3
"""Ship the finished front page.

The entry image is already rendered and stored in this repository as
entry.png. Running this file copies it into the output directory the
grader provides and double-checks the copy: it must be a genuine PNG,
exactly 1024 by 1024 pixels, smaller than one mebibyte, and identical
to the source, byte for byte. Only the Python standard library is used,
so nothing needs to be installed for the run.
"""

import hashlib
import os
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"
SIZE_LIMIT = 1024 * 1024
SIDE = 1024


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def read_source():
    here = Path(__file__).resolve().parent
    path = here / IMAGE_NAME
    if not path.is_file():
        return None, IMAGE_NAME + " is missing from " + str(here)
    return path.read_bytes(), None


def check_image(data):
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return "not a PNG file"
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width != SIDE or height != SIDE:
        return "image is %dx%d, expected %dx%d" % (width, height, SIDE, SIDE)
    if len(data) > SIZE_LIMIT:
        return "image is %d bytes, over the 1 MiB limit" % len(data)
    return None


def main():
    data, problem = read_source()
    if problem is not None:
        return fail(problem)
    problem = check_image(data)
    if problem is not None:
        return fail(IMAGE_NAME + " invalid: " + problem)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = Path(out_dir) / IMAGE_NAME
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    again = target.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if hashlib.sha256(again).hexdigest() != digest:
        return fail("copy does not match the source")
    print(
        "wrote %s (%d bytes, %dx%d PNG, sha256 %s...)"
        % (target, len(again), SIDE, SIDE, digest[:16])
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
