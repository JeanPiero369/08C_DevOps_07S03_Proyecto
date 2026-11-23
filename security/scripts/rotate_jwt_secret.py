#!/usr/bin/env python3
"""Rotate the local signing key without displaying or backing up its value."""

import argparse
import os
from pathlib import Path
import re
import secrets
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=Path(__file__).resolve().parents[2] / ".env")
    parser.add_argument("--apply", action="store_true", help="Replace the local key; existing sessions become invalid after restart")
    args = parser.parse_args()
    path = args.env_file
    if path.is_symlink() or not path.is_file():
        parser.error("The environment file must be an existing regular file, not a symlink")
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    pattern = re.compile(r"^(\s*(?:export\s+)?JWT_SECRET\s*=).*$")
    matches = [index for index, line in enumerate(lines) if pattern.match(line.rstrip("\r\n"))]
    if len(matches) != 1:
        parser.error("Expected exactly one JWT_SECRET assignment; no changes made")
    if not args.apply:
        print("Ready: one JWT_SECRET assignment found. Use --apply to rotate locally.")
        return
    index = matches[0]
    prefix = pattern.match(lines[index].rstrip("\r\n")).group(1)
    ending = "\r\n" if lines[index].endswith("\r\n") else "\n"
    lines[index] = prefix + secrets.token_hex(32) + ending
    temporary = None
    try:
        descriptor, temporary = tempfile.mkstemp(prefix=".jwt-rotation-", dir=path.parent)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as output:
            os.fchmod(output.fileno(), 0o600)
            output.write("".join(lines))
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)
    print("JWT_SECRET rotated locally; value not displayed. Restart users and sign in again.")


if __name__ == "__main__":
    main()
