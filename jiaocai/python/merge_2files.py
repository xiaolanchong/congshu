"""
Script to merge language course texts in 2 languages.
Reads each file, splitting into sections by empty lines.
Each section: first line = header, rest = content.
Validates both files: same number of sections and same number of lines inside each.
Generates <section> ... </section> blocks in HTML.
"""
import sys
from pathlib import Path


def read_sections(file_path: str) -> list[list[str]]:
    """
    Reads a file and splits its contents into sections.
    Each section is separated by one or more empty lines.
    Returns a list of sections, where each section is a list of lines.
    """
    text = Path(file_path).read_text(encoding="utf-8")
    sections = []
    current = []
    for line in text.splitlines():
        if line.strip() == "":
            if current:
                sections.append(current)
                current = []
        else:
            current.append(line.strip())
    if current:
        sections.append(current)
    return sections


def merge_sections(sections1: list[list[str]], sections2: list[list[str]]) -> str:
    """
    Merge two lists of sections into an HTML string.
    Checks that both have same number of sections and lines.
    """
    if len(sections1) != len(sections2):
        raise ValueError(f"Files have different number of sections: {len(sections1)} vs {len(sections2)}")

    html_output = []

    for i, (sec1, sec2) in enumerate(zip(sections1, sections2), start=1):
        if len(sec1) != len(sec2):
            raise ValueError(f"Section {i} has different number of lines: {len(sec1)} vs {len(sec2)}")

        header1, *lines1 = sec1
        header2, *lines2 = sec2

        section_html = [f'<section>']
        section_html.append(
            f'\t<h2>\n'
            f'\t  <span class="chinese">{header1}</span>\n'
            f'\t  <span class="english">{header2}</span>\n'
            f'\t</h2>\n'
        )

        for l1, l2 in zip(lines1, lines2):
            section_html.append(
                f'\t<div>\n'
                f'\t  <span class="chinese">{l1}</span><br>\n'
                f'\t  <span class="english">{l2}</span>\n'
                f'\t</div>\n'
            )

        section_html.append('</section>\n')
        html_output.append("\n".join(section_html))

    return "\n".join(html_output)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} file1.txt file2.txt")
        sys.exit(1)

    file1, file2 = sys.argv[1], sys.argv[2]

    sections1 = read_sections(file1)
    sections2 = read_sections(file2)

    html = merge_sections(sections1, sections2)
    print(html)
