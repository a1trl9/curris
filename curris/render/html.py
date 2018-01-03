"""render to html module
"""

def build_html(target, css_source):
    """ render to html
    """
    style = _add_style(css_source)
    output = _render_to_html(target)
    code_script = '<script src="\
            https://cdnjs.cloudflare.com/ajax/libs/prism/1.9.0/prism.min.js"></script>\
            <script src="\
            https://cdnjs.cloudflare.com/ajax/libs/prism/1.9.0/components/prism-python.min.js"></script>\
            <script src="https://cdnjs.cloudflare.com/ajax/libs/prism\
/1.9.0/components/prism-markdown.min.js"></script>'
    code_style = '<link rel="stylesheet" \
            href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.9.0/themes/prism.min.css" />'
    return '<html><head>{}\n{}</head>\n<body>{}\n{}</body></html>'\
            .format(code_style, style, output, code_script)


def _render_to_html(target, attrs=None):
    if isinstance(target, list):
        output = []
        attrs = {'in_list': '', 'in_code': False}
        for sub_target in target:
            output.append(_render_to_html(sub_target, attrs))
        if attrs['in_list']:
            suffix = '</ul>' if attrs['in_list'] == 'unorder_list_item' else '</ol>'
            output.append(suffix)
        if attrs['in_code']:
            output.append('</code></pre>')
        return ''.join(output)
    return _render_block(target, attrs)


def _add_style(source):
    style = '<style>{}</style>'
    with open(source) as source_file:
        style = style.format(source_file.read())
    return style


def _render_block(target, attrs):
    if 'block_type' not in target:
        return _render_span(target)
    block_type = target['block_type']
    if block_type == 'blank':
        return ''
    if block_type == 'code_block':
        return _render_code_block(target, attrs)
    block_type, content = target['block_type'], target['content']
    if block_type in ['order_list_item', 'unorder_list_item']:
        return _render_list_item(block_type, content, attrs)
    prefix = ''
    if attrs['in_list']:
        prefix = '</ul>\n' if attrs['in_list'] == 'unorder_list_item' else '</ol>\n'
        attrs['in_list'] = ''
    if block_type == 'block_quotes':
        return '<blockquote>{}</blockquote>'.format(_render_to_html(content, attrs))
    if block_type[0] == 'h':
        return '{}<{}>{}</{}>\n'.format(prefix, block_type, _render_span(content), block_type)
    if block_type == 'code':
        return content + '\n'
    if block_type == 'table':
        return _render_table(content)
    return '<p>{}{}</p>\n'.format(prefix, _render_span(content))


def _render_code_block(target, attrs):
    if attrs['in_code']:
        attrs['in_code'] = False
        return '</code></pre>\n'
    attrs['in_code'] = True
    return '<pre><code class="language-{}">'.format(target['language'])


def _render_list_item(block_type, content, attrs):
    prefix = ''
    if attrs['in_list'] == '':
        prefix = '<ul>\n' if block_type == 'unorder_list_item' else '<ol>'
        attrs['in_list'] = block_type
    elif block_type != attrs['in_list']:
        end = '</ul>' if attrs['in_list'] == 'unorder_list_item' else '</ol>'
        start = '<ul>' if block_type == 'unorder_list_item' else '<ol>'
        prefix = end + '\n' + start + '\n'
        attrs['in_list'] = block_type
    return prefix + '<li>{}</li>\n'.format(_render_to_html(content))


def _render_span(target):
    if isinstance(target, list):
        output = []
        for unit in target:
            output.append(_render_span(unit))
        return ''.join(output)
    return _inner_render_span(target)


def _inner_render_span(target):
    if isinstance(target, str):
        return target
    span_type = target['span_type']
    if span_type in ['bold', 'italic', 'inline_code']:
        symbol = 'strong' if span_type == 'bold' else 'em' if span_type == 'italic'\
                else 'code'
        return '<{}>{}</{}>'.format(symbol, _render_span(target['content']), symbol)
    if span_type == 'inline_link':
        content, title, inner, is_img = target['content'], target['title'],\
                target['inner'], target['is_img']
        if is_img:
            return '<img src="{}" title="{}" />'.format(_render_span(content),
                                                        _render_span(inner))
        return '<a href="{}" title="{}">{}</a>'.format(_render_span(content),
                                                       _render_span(title),
                                                       _render_span(inner))
    return _render_span(target['content'])


def _render_table(target):
    header = _render_table_row(target['header'])
    body = _render_table_rows(target['body'])
    return '<table><thead>{}</thead><tbody>{}</tbody></table>'.format(header, body)


def _render_table_rows(rows):
    return '\n'.join([_render_table_row(i) for i in rows])


def _render_table_row(row):
    return '<tr>{}</tr>'.format('\n'.join([_render_table_unit(i) for i in row['content']]))


def _render_table_unit(target):
    block_type, content = target['block_type'], target['content']
    align = ['left', 'center', 'right'][target['align']]
    return '<{} align="{}">{}</{}>'.format(block_type, align, _render_span(content), block_type)
