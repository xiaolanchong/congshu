#!/usr/bin/env python3
import html

INPUT_FILE = "1000words.txt"
OUTPUT_FILE = "output.html"

BOOTSTRAP_DARK = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
    body { background-color: #121212; color: #e0e0e0; }
    table { background-color: #1e1e1e; }
    th, td { color: #e0e0e0 !important; }
</style>
"""

def parse_line(line):
    # Split on tabs or multiple spaces
    parts = line.strip().split()
    return parts if len(parts) >= 3 else None

def main():
    rows = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip() == "":
                continue
            parts = parse_line(line)
            if parts:
                rows.append(parts)

    # Build HTML
    html_out = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "<meta charset='utf-8'>",
        "<title>Converted Table</title>",
        BOOTSTRAP_DARK,
        "</head>",
        "<body class='p-4'>",
        "<h2 class='mb-4'>Converted Table</h2>",
        "<table class='table table-bordered table-striped table-dark'>",
        "<thead><tr><th>#</th><th>Word</th><th>Translation</th></tr></thead>",
        "<tbody>"
    ]

    for row in rows:
        n, word, trans = row[:3]
        html_out.append(
            f"<tr><td>{html.escape(n)}</td>"
            f"<td>{html.escape(word)}</td>"
            f"<td>{html.escape(trans)}</td></tr>"
        )

    html_out += [
        "</tbody></table>",
        "</body></html>"
    ]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(html_out))

    print(f"Done! Written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()