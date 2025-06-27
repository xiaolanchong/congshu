def text_to_html(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        content = infile.read()

    # Split into sections by double newlines
    sections = [section.strip() for section in content.strip().split('\n\n') if section.strip()]

    html_output = ['<html>', '<body>']

    for section in sections:
        html_output.append('  <section>')
        lines = section.split('\n')
        for line in lines:
            html_output.append(f'    <div>{line.strip()}</div>')
        html_output.append('  </section>')

    html_output.extend(['</body>', '</html>'])

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write('\n'.join(html_output))

    print(f"HTML output written to {output_file}")

# Example usage
if __name__ == '__main__':
    text_to_html('assimil_jp.txt', 'assimil_jp.html')