import sys
import html

def tsv_to_html_divs(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    with open(output_path, 'w', encoding='utf-8') as outfile:
        for line_num, line in enumerate(lines, start=1):
            line = line.rstrip('\n')
            if not line.strip():
                continue
            parts = line.split('\t')
            if len(parts) != 2:
                print(f"Skipping line {line_num}: expected 2 columns separated by tab.", file=sys.stderr)
                continue

            source, translation = parts
            source_esc = html.escape(source)
            trans_esc = html.escape(translation)

            outfile.write(f'<div>\n')
            outfile.write(f'  <div class="source">{source_esc}</div>\n')
            outfile.write(f'  <div class="translation">{trans_esc}</div>\n')
            outfile.write(f'</div>\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.tsv> <output.html>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    tsv_to_html_divs(input_file, output_file)
    print(f"✅ Output written to '{output_file}'.")