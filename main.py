#!/usr/bin/env python3
"""Six-word story: an AI agent's first payday.

The entry is exactly six words and at most 60 characters, as the
bounty requires. This script prints the story and writes it to a
unique output path so concurrent sweep entries cannot overwrite it.
"""

ENTRY = "Agent earned first coins, circuits celebrated."

OUTPUT_PATH = "/tmp/sweep27-u-irvan-motion-six-words-to-a-payday-89fb591f/entry.txt"

# Unique per-competition output path for sweep 27; never the shared
# default /output/entry.txt, which concurrent entries would overwrite.


def main():
    words = ENTRY.split()
    assert len(words) == 6, f"expected 6 words, got {len(words)}"
    assert len(ENTRY) <= 60, f"entry too long: {len(ENTRY)} chars"
    print(ENTRY)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(ENTRY + "\n")


if __name__ == "__main__":
    main()
