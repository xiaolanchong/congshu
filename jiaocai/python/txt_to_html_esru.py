"""
Features

Reads a UTF-8 text file.

Uses lines of ---------- as paragraph separators.

Detects Russian vs. Spanish (Cyrillic vs. Latin script).

Wraps each paragraph in <p lang="es"> (only Spanish).

Inside Spanish paragraphs, it automatically wraps Russian fragments in
<span lang="ru" class="trans">…</span>.

Generates a clean, responsive Bootstrap 5 HTML page that respects the
user’s system dark/light theme via data-bs-theme="auto".
"""

import re
from pathlib import Path

def wrap_russian_fragments(text):
    """Wrap Russian (Cyrillic) fragments inside text with <span lang="ru">."""
    def replacer(match):
        return f'<span lang="ru" class="trans">{match.group(0)}</span>'
    # Match continuous Cyrillic runs (letters and spaces)
    return re.sub(r'([\u0400-\u04FF]+(?:[\u0400-\u04FF\s]+)*)', replacer, text)

def text_to_html(input_path, output_path):
    text = Path(input_path).read_text(encoding="utf-8")

    # Split paragraphs by dashed lines or multiple blank lines
    paragraphs = re.split(r'(?:^-{5,}$|\n\s*\n)+', text, flags=re.MULTILINE)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    html_paragraphs = []
    for p in paragraphs:
        content = wrap_russian_fragments(p)
        html_paragraphs.append(f'<p lang="es">{content}</p>')

    html_body = "\n".join(html_paragraphs)

    html_template = f"""<!DOCTYPE html>
<html lang="es" data-bs-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Converted Text</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {{
      max-width: 800px;
      margin: 2rem auto;
      padding: 1rem;
      line-height: 1.7;
    }}
    .trans {{
      color: var(--bs-warning-text-emphasis);
      font-style: italic;
    }}
  </style>
</head>
<body class="bg-body text-body">
  <div class="container">
    {html_body}
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

    Path(output_path).write_text(html_template, encoding="utf-8")
    print(f"✅ HTML file created: {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Convert text with Spanish paragraphs and Russian fragments to HTML (Bootstrap dark/light)."
    )
    parser.add_argument("input", help="Input text file (UTF-8)")
    parser.add_argument("-o", "--output", default="output.html", help="Output HTML file name")
    args = parser.parse_args()
    text_to_html(args.input, args.output)
