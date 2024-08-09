import glob
import re

from_str = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
to_str = '<meta name="viewport" content="width=device-width, initial-scale=1" />'

for filepath in glob.iglob('*.htm', recursive=True):
    with open(filepath, encoding='utf8') as file:
        content = file.read()
    if to_str in content:
        continue
    content = content.replace(from_str, from_str + '\n' + to_str)
    try:
        with open(filepath, "w", encoding='utf8') as file:
            file.write(content)
        print(f'{filepath} patched')
    except Exception as e:
        print(f'{filepath} error: {e}')
     
    
