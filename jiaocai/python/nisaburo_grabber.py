import requests
import time
import pathlib
from bs4 import BeautifulSoup


def fetch_html(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    content_type = resp.headers.get("Content-Type", "").lower()

    if "charset=" in content_type:
        charset = content_type.split("charset=")[-1].split(";")[0].strip()
    else:
        charset = resp.apparent_encoding

    if charset.lower() in ["euc-jp", "euc_jp", "eucjp"]:
        text = resp.content.decode("euc_jp", errors="replace")
    else:
        resp.encoding = charset
        text = resp.text

    return text


def html_to_text(url, out_file):
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    # remove junk
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # preserve <br>
    for br in soup.find_all("br"):
        br.replace_with("\n")

    text = soup.get_text("\n")

    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    # directory where the current script is located
    script_dir = pathlib.Path(__file__).resolve().parent

    # add 'output' subdirectory
    output_dir = script_dir / "output"

    # create it if it doesn't exist
    output_dir.mkdir(exist_ok=True)

    start = 201
    end = 488 #488
    for page in range(start, end+1):
        url = f'https://web.archive.org/web/20240217092306fw_/http://viethuong.web.fc2.com/MONDAI/{page:03}.html'
    
        html_to_text(url, output_dir / f"{page:03}.txt")
        time.sleep(5)