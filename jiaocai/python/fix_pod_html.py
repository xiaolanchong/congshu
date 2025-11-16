"""
✅ Reads all .html files in the current directory
✅ Ensures <meta name="viewport"> exists
✅ Adds Bootstrap 5.3 + auto dark/light theme
✅ Wraps all <body> contents inside <div class="container">
✅ Outputs processed files into output/
✅ Prettifies the HTML using BeautifulSoup (html5lib recommended)

Uses html5lib, which preserves structure better than lxml.

Avoids duplicated Bootstrap tags.

Preserves everything else in the document.

Adds proper responsive <meta> tag.

Auto-dark mode via data-bs-theme="auto" on <html>.

Wraps all body content into .container.
"""

import os
from bs4 import BeautifulSoup

INPUT_EXT = ".html"
OUTPUT_DIR = "output"


# ---------------------------------------------------------------------------
# 1. Ensure viewport meta tag
# ---------------------------------------------------------------------------
def ensure_viewport(soup):
    head = soup.head
    if not head:
        return

    # Already present?
    if head.find("meta", attrs={"name": "viewport"}):
        return

    meta = soup.new_tag(
        "meta",
        attrs={
            "name": "viewport",
            "content": "width=device-width, initial-scale=1"
        }
    )
    head.append(meta)


# ---------------------------------------------------------------------------
# 2. Ensure Bootstrap 5.3 with auto color mode
# ---------------------------------------------------------------------------
def ensure_bootstrap(soup):
    head = soup.head
    if not head:
        return

    # Remove old bootstrap links to avoid duplicates
    for bs in head.find_all("link"):
        if bs.get("href", "").lower().find("bootstrap") != -1:
            bs.decompose()

    # Remove old bootstrap scripts
    for bs in soup.find_all("script"):
        if bs.get("src", "").lower().find("bootstrap") != -1:
            bs.decompose()

    # Add new Bootstrap 5.3.3 (dark-theme)
    link = soup.new_tag(
        "link",
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css",
        integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH",
        crossorigin="anonymous"
    )
    head.append(link)

    script = soup.new_tag(
        "script",
        src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js",
        integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz",
        crossorigin="anonymous"
    )
    head.append(script)

    # Add dark dark/light mode
    # <html data-bs-theme="dark">
    html = soup.html
    if html and "data-bs-theme" not in html.attrs:
        html["data-bs-theme"] = "dark"


# ---------------------------------------------------------------------------
# 3. Wrap <body> contents into <div class="container">
# ---------------------------------------------------------------------------
def ensure_container(soup):
    body = soup.body
    if not body:
        return

    # Already a single container?
    if len(body.contents) == 1:
        only = body.contents[0]
        if getattr(only, "name", None) == "div" and "container" in only.get("class", []):
            return

    # Create container
    container = soup.new_tag("div", attrs={"class": "container"})

    # Move all children of body into container
    for child in list(body.contents):
        container.append(child.extract())

    body.append(container)


# ---------------------------------------------------------------------------
# 4. Process a single HTML file
# ---------------------------------------------------------------------------
def process_file(path, out_path):
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html5lib")

    ensure_viewport(soup)
    ensure_bootstrap(soup)
    ensure_container(soup)

    # Prettify and save
    html = soup.prettify()

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)


# ---------------------------------------------------------------------------
# 5. Main
# ---------------------------------------------------------------------------
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir("."):
        if filename.lower().endswith(INPUT_EXT):
            in_path = filename
            out_path = os.path.join(OUTPUT_DIR, filename)

            print(f"Processing {filename} → {out_path}")
            process_file(in_path, out_path)

    print("✔ Done!")


if __name__ == "__main__":
    main()
