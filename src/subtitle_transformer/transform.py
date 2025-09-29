"""Functions to transform timestamped subtitle text into minute-indexed paragraphs.

Algorithm (explicit):
- Parse each subtitle line of the form:
  [MM:SS.mmm --> MM:SS.mmm]  text...
- Group lines by the integer minute of the start timestamp (MM).
- For each group, concatenate the `text` pieces in original order.

"""
from __future__ import annotations

import re
from typing import Dict, List

LINE_RE = re.compile(r"^\s*\[(\d{2}):(\d{2}\.\d{3})\s*-->\s*(\d{2}):(\d{2}\.\d{3})\]\s*(.*)$")
SENT_END = ('.', '!', '?', '…', ':')


# Whisper-style single-line timestamps
RE_WHISPER = re.compile(
    r"^\s*\[(\d{2}):(\d{2})[.,](\d{3})\s*-->\s*(\d{2}):(\d{2})[.,](\d{3})\]\s*(.*)$"
)

# Standard SRT timestamp (HH:MM:SS,mmm --> HH:MM:SS,mmm)
RE_SRT = re.compile(
    r"^(\d{2}):(\d{2}):(\d{2})[.,](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[.,](\d{3})$"
)

def parse_subtitle_lines(text: str) -> List[Dict]:
    items: List[Dict] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Whisper style
        m = RE_WHISPER.match(line)
        if m:
            minute = int(m.group(1))
            payload = m.group(7).strip()
            items.append({"minute": minute, "text": payload})
            i += 1
            continue
        # SRT block
        m = RE_SRT.match(line)
        if m:
            hh = int(m.group(1))
            mm = int(m.group(2))
            minute = hh * 60 + mm
            i += 1
            # collect subtitle text lines until blank or end
            text_lines = []
            while i < len(lines) and lines[i].strip() != "":
                text_lines.append(lines[i].strip())
                i += 1
            payload = " ".join(text_lines)
            items.append({"minute": minute, "text": payload})
            i += 1  # skip blank line
            continue
        i += 1  # skip unrecognized line
    return items


def group_by_minute(items: List[Dict]) -> Dict[int, List[str]]:
    groups: Dict[int, List[str]] = {}
    for it in items:
        groups.setdefault(it["minute"], []).append(it["text"])
    return groups


def build_minute_paragraph(lines: List[str]) -> str:
    """Concatenate lines into a single paragraph, no internal newlines."""
    return " ".join(line.strip() for line in lines)


def transform_subtitles(text: str) -> str:
    """Transform full subtitle text into minute blocks.

    Output format:

    [MM]
    paragraph text

    [NN]
    next paragraph

    Minutes are zero-padded to 2 digits.
    """
    items = parse_subtitle_lines(text)
    groups = group_by_minute(items)
    if not groups:
        return ""
    out_lines: List[str] = []
    for minute in sorted(groups.keys()):
        paragraph = build_minute_paragraph(groups[minute])
        out_lines.append(f"[{minute:02d}]")
        out_lines.append(paragraph)
        out_lines.append("")
    # remove trailing blank line
    if out_lines and out_lines[-1] == "":
        out_lines.pop()
    return "\n".join(out_lines)


def main(argv=None) -> int:
    """Console entry point.

    Usage:
        python -m subtitle_transformer [files...]
        python -m subtitle_transformer file1.srt file2.srt > out.txt
        cat file.srt | python -m subtitle_transformer -   # read from stdin with "-"
    """
    import argparse
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(
        prog="subtitle_transformer",
        description="Group subtitle lines by start-minute and print minute-indexed paragraphs.",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Subtitle files to process. If empty, reads stdin. Use '-' to read stdin explicitly.",
    )
    args = parser.parse_args(argv)

    # Helper to read a file or stdin
    def read_source(path_str: str) -> str:
        if path_str == "-" or not path_str:
            return sys.stdin.read()
        p = Path(path_str)
        return p.read_text(encoding="utf-8")

    # If no files provided, read stdin
    if not args.files:
        text = sys.stdin.read()
        output = transform_subtitles(text)
        print(output)
        return 0

    # Otherwise process every file and print outputs sequentially
    for path in args.files:
        text = read_source(path)
        output = transform_subtitles(text)
        print(output)
        # separate multiple files with a blank line for readability
        if path != args.files[-1]:
            print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())