import json
from curris.parser import parse
from curris.render.html import build_html

def output(content, file_name):
    with open(file_name, 'w') as writer:
        writer.write(content)

def test_table():
    with open('curris/test/resource/table.md') as reader:
        content = reader.read()
        result = parse(content)
        output(json.dumps(result), 'curris/test/resource/table.json')
        html = build_html(result, 'curris/test/resource/test.css')
        output(html, 'curris/test/resource/table.html')

test_table()
