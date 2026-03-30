#!/usr/bin/env python3
"""
process_anki.py

Post-processes Anki TSV output from Gemini:
  - Replaces {{word}} markers with underscores, preserving spaces and punctuation
  - Validates exactly one tab per line (front\tback)
  - Reports any issues found

Usage:
    python process_anki.py input.tsv
    python process_anki.py input.tsv output.tsv
    python process_anki.py input.tsv --clipboard   # copy result to clipboard

If no output path is given, writes to input_processed.tsv.
You can also paste TSV content directly via stdin:
    echo 'front {{Wort}} here \t back' | python process_anki.py -
"""

import re
import sys


def replace_markers(text: str) -> str:
    """Replace {{phrase}} with underscores, preserving spaces and punctuation."""
    return re.sub(r"\{\{(.+?)\}\}", lambda m: re.sub(r"\w", "_", m.group(1)), text)


def validate_line(line: str, line_num: int) -> list[str]:
    """Check a single TSV line for common issues. Returns list of warnings."""
    warnings = []
    stripped = line.strip()
    if not stripped:
        return warnings

    tabs = stripped.count("\t")
    if tabs != 1:
        warnings.append(
            f"Line {line_num}: expected 1 tab, found {tabs}"
        )

    remaining_markers = re.findall(r"\{\{.+?\}\}", stripped)
    if remaining_markers:
        warnings.append(
            f"Line {line_num}: unprocessed markers remain: {remaining_markers}"
        )

    return warnings


def process(input_text: str) -> tuple[str, list[str]]:
    """Process TSV text. Returns (processed_text, warnings)."""
    lines = input_text.splitlines(keepends=True)
    all_warnings = []

    processed_lines = []
    for i, line in enumerate(lines, start=1):
        processed = replace_markers(line)
        processed_lines.append(processed)
        all_warnings.extend(validate_line(processed, i))

    return "".join(processed_lines), all_warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python process_anki.py <input.tsv | -> [output.tsv | --clipboard]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_arg = sys.argv[2] if len(sys.argv) > 2 else None

    # Read input
    if input_path == "-":
        input_text = sys.stdin.read()
    else:
        with open(input_path, "r", encoding="utf-8") as f:
            input_text = f.read()

    result, warnings = process(input_text)

    # Print warnings
    for w in warnings:
        print(f"  ⚠ {w}", file=sys.stderr)

    # Write output
    if output_arg == "--clipboard":
        try:
            import subprocess
            subprocess.run(
                ["xclip", "-selection", "clipboard"],
                input=result.encode("utf-8"),
                check=True,
            )
            print(f"Copied to clipboard ({len(result.splitlines())} lines)")
        except FileNotFoundError:
            print("xclip not found. Install it: sudo apt install xclip", file=sys.stderr)
            sys.exit(1)
    elif input_path == "-" and output_arg is None:
        sys.stdout.write(result)
    else:
        if output_arg and output_arg != "--clipboard":
            output_path = output_arg
        else:
            output_path = input_path.rsplit(".", 1)[0] + "_processed.tsv"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Processed {len(result.splitlines())} lines → {output_path}")

    if warnings:
        print(f"\n{len(warnings)} warning(s) found — review the lines above.", file=sys.stderr)


if __name__ == "__main__":
    main()
