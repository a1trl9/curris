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

## Basic Syntax

You might find the [introduction of Markdown](https://en.wikipedia.org/wiki/Markdown) is helpful, as well as the [cheatsheet](https://guides.github.com/pdfs/markdown-cheatsheet-online.pdf) by Github (It defines differently, but popular).

### 1. Header

Use hash symbol to indicate headers. For example:

```markdown
# Header1
## Header2
### Header3
```

Rendered HTML will be like:

# Header1

## Header2

### Header3

### 2. Code Block

Use \`\`\` to start a code block, followed by the language. Use \`\`\` to end the block as well. For example:

```python
def test(param):
    print(param)
```

[Prism](http://prismjs.com) is used to highlight codes in HTML.

### 3. List

#### Unordered List:

Nested list is supported. Use tab or 4 spaces to indicate indentations.

```markdown
- item1
- item2
- item3
    - subitem1
    - subitem2
        - subsubitem1
        - subsubitem2
- item4
```

Rendered as:
- item1
- item2
- item3
    - subitem1
    - subitem2
        - subsubitem1
        - subsubitem2
- item4


#### Ordered List:
```markdown
1. item1
2. item2
3. item3
    1. subitem1
    2. subitem2
4. item4
```

Rendered as:
1. item1
2. item2
3. item3
    1. subitem1
    2. subitem2
4. item4

### 5. Table

```markdown
|Tables|Are|Cool|
|:---|:---:|---:|
|item1|item2|item3|
|item4|item5|item6|
```

Rendered as:

|Tables|Are|Cool|
|:---|:---:|---:|
|item1|item2|item3|
|item4|item5|item6|

### 6. Link

```markdown
[shown content](www.google.com "optional title")
```

[shown content](https://www.google.com "optional title")


### 7. Image

```markdown
![Image](https://scontent-nrt1-1.cdninstagram.com/t51.2885-15/s640x64…1080.1080/23823593_1751381835163782_208122965429059584_n.jpg)
```

![Image](https://scontent-nrt1-1.cdninstagram.com/t51.2885-15/s640x64…1080.1080/23823593_1751381835163782_208122965429059584_n.jpg)

### 8. emphasis
```markdown
**bold**
*italic*
```

Rendered as:

**bold**

*italic*

### 9. quoteblock

> Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo.
    > This is a nested quotes block.
