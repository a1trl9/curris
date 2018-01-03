# Minimal Markdown Parser in Python3

This is the first minimal project in 2018, which provides minimal parsing and rendering functions of Markdown. Specifically, it supports most common Markdown syntax, and could parse source file into Python `dict`, as well as render to html.

Some extended functions of Markdown are not supported yet, but are under implementation.

## Usage
```python
from curris.parser import parse
from curris.render.html import build_html

parsed_result = parse(markdown_string)
built_html = build_html(parsed_result, output_file_path)
```

[More Introduction](www.a1trl936.me/curris)