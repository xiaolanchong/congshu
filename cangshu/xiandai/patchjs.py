import glob

from_str = 'elx + shift - tip.offsetWidth'
to_str = 'Math.max(elx + shift - tip.offsetWidth, 0)'

for filepath in glob.iglob('./**/*.htm', recursive=True):
    with open(filepath, encoding='utf8') as file:
        content = file.read()
    if to_str in content:
        break
    content = content.replace(from_str, to_str)
    with open(filepath, "w", encoding='utf8') as file:
        file.write(content)
