import dataclasses
import enum
import re


class EntityType(enum.Enum):
    HEADER = 'H'
    DIALOG = 'DLG'
    PHRASES = 'PH'
    NEW_WORDS = 'NW'


class Entity:
    def add_line(self, line: str):
        raise NotImplementedError()

    def to_html(self):
        raise NotImplementedError()


class Header(Entity):
    def __init__(self, level: int, title: str):
        self.level = level
        self.title = title

    def add_line(self, line):
        pass

    def to_html(self):
        return f"""</section>
        <section class="my-3">
        <h{self.level}>{self.title}</h{self.level}>"""

    def __str__(self):
        return f'H{self.level} {self.title}'


class Dialog(Entity):
    def __init__(self):
        self.sentences: list[str] = []

    def add_line(self, line):
        if not line:
            return
        self.sentences.append(line)

    def to_html(self):
        return '\n'.join(
            f"""
        <div class="row my-2">
		<div class="col">
		  {sentence}
		</div>
		<div class="col">
		  &lt;pinyin&gt;
		</div>
		<div class="col">
		  &lt;rus&gt;
		</div>
	  </div>
            """ for sentence in self.sentences
        )

    def __str__(self):
        return f'DLG {len(self.sentences)} line(s)'


class Phrases(Entity):
    def __init__(self):
        self.sentences: list[str] = []

    def add_line(self, line):
        if not line:
            return
        self.sentences.append(line)

    def to_html(self):
        out = '<h4>Словосочетания</h4>\n'
        out += '<ul>\n'
        out += '\n'.join(
            f"""<li>{sentence}</li>"""
            for sentence in self.sentences
        )
        out += '\n</ul>'
        return out

    def __str__(self):
        return f'PH {len(self.sentences)} line(s)'


class NewWords(Entity):
    def __init__(self):
        self.zh_words = []
        self.ru_translations = []
        self.at_words = None

    def add_line(self, line):
        if not line:
            if self.at_words is None:
                self.at_words = True
            else:
                self.at_words = False
        else:
            (self.zh_words if self.at_words else self.ru_translations).append(line)

    def to_html(self):
        assert len(self.zh_words) == len(self.ru_translations)
        out = '<h4>Новые слова</h4>\n'
        out += '\n'.join(
                        f"""
                      <div class="row">
                        <div class="col-1">
                          {zh}
                        </div>
                        <div class="col-1">
                          &lt;pinyin&gt;
                        </div>
                        <div class="col-3">
                          {ru}
                        </div>
                      </div>
                       """
                        for zh, ru in zip(self.zh_words, self.ru_translations))
        return out

    def __str__(self):
        return f'NW {len(self.zh_words)} word(s)'


class Notes(Entity):
    def __init__(self):
        self.notes = []

    def add_line(self, line):
        if line:
            self.notes.append(line)

    def to_html(self):
        return f'<h4>Примечания</h4>\n<div>{"".join(self.notes)}</div>'

    def __str__(self):
        return f'NOTES {len(self.notes)} line(s)'


def run():
    re_entity = re.compile(r"""
    ^(?:
    (?P<header_level>\#{1,2})\s(?P<header_title>.+?)|
    (?P<dialog>\#\#\#\sDLG)|
    (?P<new_words>\#\#\#\sNW)|
    (?P<phrases>\#\#\#\sPH)|
    (?P<notes>\#\#\#\sNOTES)
    )$
    """, re.VERBOSE)
    entities = []
    with open('../zhongwen/counter_words/4.md', encoding='utf8') as f:
        cur_entity: typing.Optional[Entity] = None
        for line in f.readlines():
            line = line.strip()
            m = re_entity.match(line)
            if m is not None:
                gd = m.groupdict()
                if gd['header_level']:
                    if cur_entity:
                        entities.append(cur_entity)
                    level = int(len(gd['header_level'])) + 1
                    cur_entity = Header(level=level, title=gd['header_title'])
                elif gd['dialog']:
                    if cur_entity:
                        entities.append(cur_entity)
                    cur_entity = Dialog()
                elif gd['phrases']:
                    if cur_entity:
                        entities.append(cur_entity)
                    cur_entity = Phrases()
                elif gd['new_words']:
                    if cur_entity:
                        entities.append(cur_entity)
                    cur_entity = NewWords()
                elif gd['notes']:
                    if cur_entity:
                        entities.append(cur_entity)
                    cur_entity = Notes()
            elif cur_entity:
                cur_entity.add_line(line)
        if cur_entity:
            entities.append(cur_entity)
        #for ent in entities:
        #    print(str(ent))
        for ent in entities:
            print(ent.to_html())
            print('\n')


run()
