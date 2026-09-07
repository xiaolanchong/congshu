# Bilingual TSV viewer

Open `bilingual-text.html` with the TSV file supplied by the `file` URL
parameter:

```text
bilingual-text.html?file=../../path/to/text.tsv
```

The file parameter may be a relative path (resolved from the viewer page) or
an absolute URL. `tsv` and `src` are accepted aliases for `file`. Use a web
server rather than opening the HTML with `file://`, because browsers normally
block `fetch()` requests from local files.

Each non-empty, non-comment line of the TSV contains a source sentence, its
translation, and optionally a correspondence rate:

```tsv
你好。\tHello.\t0.98
你叫什么名字？\tWhat is your name?
```

The reader shows the source sentences only. Click, tap, or focus a sentence
and press Enter/Space to open its translation panel. Escape, the × button, or
clicking outside the panel closes it. The panel opens below the selected
sentence and opens above it when there is insufficient space below. The
popup displays only the translation. Its ↑ and ↓ buttons on the right show the
translations from the preceding and following TSV rows. The optional third
column is accepted but not displayed. Lines beginning with `#` are comments
and are not displayed.
Lines with fewer than two tab-separated columns are skipped and reported below
the text. The viewer uses the dark theme in `bilingual-text.css`.
