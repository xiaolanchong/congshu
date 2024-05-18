import jinja2
import dataclasses as dc


template_str = """
<!DOCTYPE html>
<head lang="zh-Hans">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{{title}}</title>
    <link rel="stylesheet" href="../../style.css">
    <style>
        body { font-family: Verdana, Arial, sans-serif; }
        table { border-width: 0 }
        td { padding-right: 2em }
        section { margin: 1em 1em }
        .pinyin { color: lightgray; }
    </style>
    <body>
        {% for lesson in lessons %}
            <section>
                <h3>{{ lesson.name }}</h3>
                <table>
                <tbody>
                {% for word in lesson.definitions %}
                  <tr>
                    <td>{{word.hanzi}}</td>
                    <td class="pinyin">{{word.pinyin}}</td>
                    <td>{{word.definition}}</td>
                  </tr>
                {% endfor %}
                </tbody>
                </table>
            </section>
        {% endfor %}
    </body>
</head>
"""


@dc.dataclass
class WordDefinition:
    hanzi: str
    pinyin: str
    definition: str


@dc.dataclass
class Lesson:
    name: str
    definitions: [WordDefinition]


def convert():
    environment = jinja2.Environment()
    template = environment.from_string(template_str)
    filename = '../zhongwenboke/zhong0000words.txt'
    title = '中级1-200生词'
    lessons = []
    with open(filename, encoding='utf8') as file:
        delimiter = '\t\t'
        for line in file.readlines():
            line = line.strip()
            if len(line) == 0:
                pass
            elif delimiter not in line:
                lessons.append(Lesson(name=line, definitions=[]))
            else:
                parts = line.split(delimiter)
                if len(parts) == 3:
                    hanzi, pinyin, definition = parts
                else:
                    print(f'skipped {parts}')
                lessons[-1].definitions.append(WordDefinition(hanzi, pinyin, definition))
    html = template.render(title=title, lessons=lessons)
    with open(filename + '.html', 'w', encoding='utf8') as outfile:
        outfile.write(html)
    print(len(lessons))


convert()
