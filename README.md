# Minimal Markdown Parser in Python3

## Installation
```
python setup.py install
```

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
curris -s=source_path -o=output_path [-html] [-css=css_source_path] [-style=style_string]
```
