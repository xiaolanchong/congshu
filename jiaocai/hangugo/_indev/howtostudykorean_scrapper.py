import sys
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def get_html(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; bs4-scraper/1.0)"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    if not resp.encoding:
        resp.encoding = resp.apparent_encoding
    return resp.text


def scrape(url: str = None, file_name: str = None):
    assert url or file_name
    html = get_html(url) if url else open(file_name, encoding='utf8').read()
    soup = BeautifulSoup(html, "html.parser")

    results = []
    for p in soup.find_all("p"):
        if p.find('p'):
            continue
        # Replace <br> with a newline so we can split cleanly
        for br in p.find_all("br"):
            br.replace_with("\n")
        # Now split into "sentences" by line
        tt = p.get_text(" ")
        added = False
        for line in p.get_text().split("\n"):
            line = line.strip()
            if "=" in line:
                results.append(line)
                added = True
        if added:
            results.append('-' * 10)

    return results

   
def run(url):
    parsed = urlparse(url)
    if not (parsed.scheme and parsed.netloc):
        print("Please provide a valid absolute URL (e.g., https://example.com)")
        sys.exit(1)

    try:
        url = None
        file_name = 'lesson8.html'
        matches = scrape(url=url, file_name=file_name)
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        sys.exit(2)

    if matches:
        with open('out.txt', mode='w', encoding='utf8') as f:
            for i, line in enumerate(matches, 1):
                f.write(f"{i:02d}: {line}\n")
    else:
        print("No <p> lines with '=' found.")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python scraper.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    run(url)


if __name__ == "__main__":
    main()
