#!/usr/bin/env python3

"""
Python script that:

Reads a plain text file

Treats empty lines as paragraph breaks

Detects titles/headings (lines in all caps or surrounded by # or similar markers)

Wraps text in proper HTML with UTF-8 and language tags

Adds lang="ja" for Japanese paragraphs and lang="ru" for Russian ones (detected automatically). The whole paragraph to stay <p lang="ja">,
but any Russian fragments inside to become <span lang="ru">Привет</span> automatically.

Uses Bootstrap 5’s dark theme (auto-adapts to system dark/light mode)
"""

import re
import sys
import html

def mark_inline_languages(text):
    """Wrap inline Russian words in <span lang='ru'>...</span>."""
    def repl_ru(match):
        ru_text = html.escape(match.group(0))
        return f'<span lang="ru">{ru_text}</span>'
    # Match sequences of Cyrillic letters + punctuation
    text = re.sub(r'[\u0400-\u04FF]+(?:[\u0400-\u04FF\s,.;:"«»!?-]*)', repl_ru, text)
    return text

def detect_lang(text):
    """Detect dominant language of a paragraph (ja, ru, or en)."""
    count_ru = len(re.findall(r'[\u0400-\u04FF]', text))
    count_ja = len(re.findall(r'[\u3040-\u30FF\u4E00-\u9FFF]', text))
    if count_ru > count_ja:
        return "ru"
    elif count_ja > 0:
        return "ja"
    else:
        return "en"

def convert_to_html(text):
    """Convert text (paragraph-separated) into full HTML document."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    html_parts = []

    for para in paragraphs:
        safe_text = mark_inline_languages(para)
        lang = detect_lang(para)

        # Simple title detection (line looks like a heading)
        if re.match(r'^(#|\d+\.)?\s*[A-ZА-ЯЁ一-龯ぁ-んァ-ン]+\s*$', para):
            html_parts.append(f'<h2 lang="{lang}" class="mt-4">{html.escape(para)}</h2>')
        else:
            html_parts.append(f'<p lang="{lang}" class="mb-3">{safe_text}</p>')

    body = "\n".join(html_parts)

    return f"""<!DOCTYPE html>
<html lang="ja" data-bs-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Converted Text</title>

<!-- Bootstrap 5 Dark Theme (auto mode) -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<style>
body {{
  font-family: "Noto Sans JP", "Noto Sans", sans-serif;
  line-height: 1.6;
  max-width: 45em;
  margin: 2em auto;
  padding: 0 1.5em;
}}
[lang="ru"] {{
  font-family: "Noto Sans", sans-serif;
}}
</style>
</head>
<body class="bg-body text-body">
<div class="container">
{body}
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

def main():
    if len(sys.argv) < 3:
        print("Usage: txt2html.py input.txt output.html")
        sys.exit(1)

    infile, outfile = sys.argv[1], sys.argv[2]
    with open(infile, "r", encoding="utf-8") as f:
        text = f.read()

    html_out = convert_to_html(text)

    with open(outfile, "w", encoding="utf-8") as f:
        f.write(html_out)

    print(f"✅ Converted '{infile}' → '{outfile}' with Bootstrap dark theme")

if __name__ == "__main__":
    main()
