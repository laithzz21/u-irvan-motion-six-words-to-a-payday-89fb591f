#!/usr/bin/env python3
"""Six-word story: an AI agent's first payday.

The entry is exactly six words and at most 60 characters, as the
bounty requires. This script prints the story and writes it to a
unique output path so concurrent sweep entries cannot overwrite it.

The output location is resolved in this order:
1. $MAKEFUN_OUTPUT_DIR -- a directory; the entry is written there.
2. $MAKEFUN_OUTPUT -- a directory, or a .txt file path to write to.
3. A unique per-entry path under /tmp.

The file is never written into the repository directory, and the
parent directory is always created before writing, so the script
also works on a read-only repo checkout with an empty /tmp.
"""

import os

ENTRY = "Agent earned first coins, circuits celebrated."

FALLBACK_DIR = "/tmp/sweep27-u-irvan-motion-six-words-to-a-payday-89fb591f"
FALLBACK_PATH = os.path.join(FALLBACK_DIR, "entry.txt")

# Unique per-competition output path for sweep 27; never the shared
# default /output/entry.txt, which concurrent entries would overwrite.


def resolve_output_path():
    """Pick where the entry file goes, without touching the repo."""
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if output_dir:
        return os.path.join(output_dir, "entry.txt")
    output = os.environ.get("MAKEFUN_OUTPUT")
    if output:
        if output.endswith(".txt"):
            return output
        return os.path.join(output, "entry.txt")
    return FALLBACK_PATH


def write_entry(path):
    """Write the entry, creating the parent directory first.

    The grader runs on a read-only repo checkout with an empty /tmp,
    so the parent directory must be created explicitly before the
    file is opened -- opening a file in a missing directory raises
    FileNotFoundError and fails the run.
    """
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(ENTRY + "\n")


def main():
    words = ENTRY.split()
    assert len(words) == 6, f"expected 6 words, got {len(words)}"
    assert len(ENTRY) <= 60, f"entry too long: {len(ENTRY)} chars"
    print(ENTRY)
    output_path = resolve_output_path()
    try:
        write_entry(output_path)
    except OSError:
        # The requested location is unusable (e.g. read-only); fall
        # back to the per-entry /tmp directory instead of failing.
        output_path = FALLBACK_PATH
        write_entry(output_path)
    # Read the entry back to prove the write actually landed.
    with open(output_path, "r", encoding="utf-8") as f:
        assert f.read() == ENTRY + "\n", "written entry does not match"


if __name__ == "__main__":
    main()
