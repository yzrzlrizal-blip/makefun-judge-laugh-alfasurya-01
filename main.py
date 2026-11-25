"""Office joke entry for make.fun's "Make the AI Judge Laugh".

Reads the single joke line shipped in entry.txt, validates it against the
competition gate (one line, 1-200 characters, no control characters, not
only whitespace), and writes it verbatim to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt).

Pure standard library; reads nothing outside this repository.
"""

import os
import sys

MAX_CHARS = 200


def load_joke() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "entry.txt"), encoding="utf-8") as handle:
        text = handle.read()
    # A trailing newline in the shipped file is formatting, not part of the joke.
    if text.endswith("\n"):
        text = text[:-1]
    return text


def validate(text: str) -> None:
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} characters, over the 200 limit")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise ValueError("entry contains control characters")


def main() -> int:
    text = load_joke()
    validate(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    # Verify the write: re-read the output and confirm it is byte-identical.
    with open(out_path, encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        raise ValueError("verification failed: output differs from entry")
    print(f"wrote {len(text)} characters to {out_path}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
