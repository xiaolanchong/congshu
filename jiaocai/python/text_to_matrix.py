"""
read a text file where lines come in pairs (Chinese / English), 
with the English one marked by an indent, and output an HTML page with <div><span>…</span></div> blocks.
like:
Line1 Chinese
    Line2 English
Line3 Chinese
    Line4 English
...
"""

import sys
from pathlib import Path
import html


def format_error(line_num: int, line: str, msg: str) -> str:
    """
    Pretty-print an error message with line number, line content,
    and a caret under the first character.
    """
    caret_line = " " * 4 + " " * (len(str(line_num)) + 2) + "^"
    return (
        f"❌ {msg}\n"
        f"Line {line_num}: {repr(line)}\n"
        f"{caret_line}"
    )


def txt_to_html(input_file: str, output_file: str):
    lines = Path(input_file).read_text(encoding="utf-8").splitlines()

    # Check for even number of lines
    if len(lines) % 2 != 0:
        raise ValueError(
            f"❌ Input file has {len(lines)} lines, which is not even. "
            "Each Chinese line must have a matching English line."
        )

    html_blocks = []
    for i in range(0, len(lines), 2):
        chinese_line = lines[i]
        english_line = lines[i + 1]

        # Loose check: Chinese lines must not start with whitespace
        if chinese_line and chinese_line[0].isspace():
            raise ValueError(
                format_error(i + 1, chinese_line, "Chinese line should not start with whitespace")
            )

        # Loose check: English lines must start with whitespace
        if not english_line or not english_line[0].isspace():
            raise ValueError(
                format_error(i + 2, english_line, "English line must start with at least one space/tab")
            )

        # Strip properly
        chinese_line = chinese_line.strip()
        english_line = english_line.lstrip()

        # Escape HTML special chars
        chinese_line = html.escape(chinese_line)
        english_line = html.escape(english_line)

        block = f"""<div>
  <span class="chinese">{chinese_line}</span><br>
  <span class="english">{english_line}</span>
</div>"""
        html_blocks.append(block)

    # Wrap in full HTML page
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Text Conversion</title>
</head>
<body>
{chr(10).join(html_blocks)}
</body>
</html>"""

    Path(output_file).write_text(html_content, encoding="utf-8")
    print(f"✅ Converted {input_file} -> {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert.py input.txt output.html")
    else:
        try:
            txt_to_html(sys.argv[1], sys.argv[2])
        except ValueError as e:
            print(e)
            sys.exit(1)