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


def parse_subtitle_lines(text: str) -> List[Dict]:
    """Parse lines and return list of dicts with start_minute and text.

    Lines that don't match are ignored.
    """
    items = []
    for raw in text.splitlines():
        m = LINE_RE.match(raw)
        if not m:
            continue
        minute = int(m.group(1))
        # seconds_str = m.group(2)  # not used here, but could be
        payload = m.group(5).strip()
        items.append({"minute": minute, "text": payload})
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


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        path = sys.argv[1]
        with open(path, "r", encoding="utf-8") as f:
            s = f.read()
    else:
        s = sys.stdin.read()
    print(transform_subtitles(s))