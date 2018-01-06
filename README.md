# Minimal Markdown Parser in Python3

This is the first minimal project in 2018, which provides minimal parsing and rendering functions of Markdown. Specifically, it supports most common Markdown syntax, and could parse source file into Python `dict`, as well as render to html.

Some extended functions of Markdown are not supported yet, but are under implementation.

## Usage
### Python
```python
from curris.parser import parse
from curris.render.html import build_html

parsed_result = parse(markdown_string)
built_html = build_html(parsed_result, optional_css_resource)
```

### Cli
```
curris -s=source_path -o=output_path [-html] [-css=css_source_path]
```

[More Introduction](http://www.a1trl936.me/curris)
