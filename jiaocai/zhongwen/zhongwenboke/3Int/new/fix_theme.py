# Adds the dark bootstrap theme, fix html parsing errors
# Usage: put to a dir and run, fixes all files in the dir

import glob
import re
import bs4

is_patched = 'data-bs-theme'
re_style = re.compile('<style>.*?</style>', re.IGNORECASE|re.DOTALL)
bootstrap_link = '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">\n' +\
                 '<link href="style.css" rel="stylesheet">\n'

for filepath in glob.iglob('*.htm*', recursive=True):
    with open(filepath, encoding='utf8') as file:
        content = file.read()
    if is_patched in content:
        print(f'{filepath} skipped')
        continue
    # fix header
    content = re_style.sub(bootstrap_link, content, 1)
    content = content.replace('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN">', '<!DOCTYPE html>', 1)
    content = content.replace('<html>', '<html lang="zh-Hans">', 1)
    
    content = content.replace('width="90%"', '')
    content = content.replace('width="35%"', '')
    content = content.replace('with="25%"', '')
    content = content.replace('width="40%"', '')

    content = re.sub('(?<!</tr>)<p />', '<br/><br/>', content)  # dialog - preserve an empty line between phrases
    content = re.sub('(?<=</tr>)<p />', '', content)  # word table - remove paragraphes

    content = content.replace('<body>', '<body data-bs-theme="dark"><div class="container">')
    content = content.replace('</body>', '</div></body>', 1)
    
    soup = bs4.BeautifulSoup(content, "html.parser")
    content = soup.prettify()   # no html5 to preserve diacritics

    try:
        with open(filepath, "w", encoding='utf8') as file:
            file.write(content)
        print(f'{filepath} patched')
    except Exception as e:
        print(f'{filepath} error: {e}')
