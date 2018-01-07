"""render to html module
"""

def build_html(target, css_source=None, css_string=''):
    """ render to html
    """
    style = _add_style(css_source, css_string) if css_source or css_string else ''
    attrs = {'in_list': '', 'in_code': False, 'code_langs': [], 'has_math': False}
    output = _render_to_html(target, attrs)

    code_script = _build_code_script(attrs['code_langs']) if attrs['code_langs'] else ''
    code_style = '<link rel="stylesheet" \
href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.9.0/themes/prism.min.css"\
/>' if attrs['code_langs'] else ''

    math_style = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com\
/ajax/libs/KaTeX/0.9.0-alpha2/katex.min.css"\
integrity="sha384-exe4Ak6B0EoJI0ogGxjJ8rn+RN3ftPnEQrGwX59KTCl5ybGzvHGKjhPKk/KC3abb"\
crossorigin="anonymous">' if attrs['has_math'] else ''
    math_script = _build_math_script() if attrs['has_math'] else ''

    return '<!DOCTYPE html>\n<html>\n<head>\n{}\n{}\n{}\n</head>\n<body>\
\n{}\n{}\n{}\n</body>\n</html>'\
            .format(code_style, math_style, style, output, code_script, math_script)


def _build_math_script():
    """ Thx Katex for rendering Latex
    """
    math_prefix = '<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX\
/0.9.0-alpha2/katex.min.js" \
integrity="sha384-OMvkZ24ANLwviZR2lVq8ujbE/bUO8IR1FdBrKLQBI14Gq5Xp/lksIccGkmKL8m+h" crossorigin="anonymous"></script>\
<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.9.0-alpha2/contrib/auto-render.min.js" \
integrity="sha384-cXpztMJlr2xFXyDSIfRWYSMVCXZ9HeGXvzyKTYrn03rsMAlOtIQVzjty5ULbaP8L"\
crossorigin="anonymous"></script>'
    render_script = '<script>renderMathInElement(document.body,\
{delimiters:[{left: "$$", right: "$$", display: true}, \
{left: "$", right: "$", display: false}]})</script>'
    return math_prefix + '\n' + render_script


def _build_code_script(langs):
    """ Thx Prism for rendering Latex
    """
    lang_prefix = '<script src="https://cdnjs.cloudflare.com/ajax/libs/prism\
/1.9.0/prism.min.js"></script>'
    lang_temp = '<script src="https://cdnjs.cloudflare.com/ajax/libs/prism\
/1.9.0/components/prism-{}.min.js"></script>'
    lang_scripts = [lang_prefix]
    for lang in langs:
        lang_scripts.append(lang_temp.format(lang))
    return '\n'.join(lang_scripts)


def _render_to_html(target, attrs):
    if isinstance(target, list):
        output = []
        for sub_target in target:
            output.append(_render_to_html(sub_target, attrs))
        if attrs['in_list']:
            suffix = '</ul>' if attrs['in_list'] == 'unorder_list_item' else '</ol>'
            output.append(suffix)
        if attrs['in_code']:
            output.append('</code></pre>')
        return ''.join(output)
    return _render_block(target, attrs)


def _add_style(source, string):
    if string and string[0] in '\'"':
        string = string[1:]
    if string and string[-1] in '\'"':
        string = string[:-1]
    if source:
        with open(source) as source_file:
            style = '<style>{}\n{}</style>'.format(source_file.read(), string)
    else:
        style = '<style>{}</style>'.format(string)
    return style


def _merge_attrs(attrs, new_attrs):
    for lang in new_attrs['code_langs']:
        if lang not in attrs:
            attrs.append(lang)
    if new_attrs['has_math']:
        attrs['has_math'] = True


def _render_block(target, attrs):
    if 'block_type' not in target:
        return _render_span(target, attrs)
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
        new_attrs = {'in_list': '', 'in_code': False, 'code_langs': [], 'has_math': False}
        rendered = '<blockquote>{}</blockquote>'.format(_render_to_html(content, new_attrs))
        _merge_attrs(attrs, new_attrs)
        return rendered
    if block_type[0] == 'h':
        return '{}<{}>{}</{}>\n'.format(prefix, block_type,
                                        _render_span(content, attrs), block_type)
    if block_type == 'code':
        return content + '\n'
    if block_type == 'table':
        return _render_table(content, attrs)
    return '<p>{}{}</p>\n'.format(prefix, _render_span(content, attrs))


def _render_code_block(target, attrs):
    if attrs['in_code']:
        attrs['in_code'] = False
        return '</code></pre>\n'
    attrs['in_code'] = True
    lang = target['language']
    if lang not in attrs['code_langs']:
        attrs['code_langs'].append(lang)
    return '<pre><code class="language-{}">'.format(lang)


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
    new_attrs = {'in_list': '', 'in_code': False, 'code_langs': [], 'has_math': False}
    rendered = prefix + '<li>{}</li>\n'.format(_render_to_html(content, new_attrs))
    _merge_attrs(attrs, new_attrs)
    return rendered


def _render_span(target, attrs):
    if isinstance(target, list):
        output = []
        for unit in target:
            output.append(_render_span(unit, attrs))
        return ''.join(output)
    return _inner_render_span(target, attrs)


def _inner_render_span(target, attrs):
    if isinstance(target, str):
        return target
    span_type = target['span_type']
    cands = {'bold': 'strong', 'italic': 'em', 'inline_code': 'code',
             'super_script': 'sup', 'sub_script': 'sub', 'strike_out': 'del'}
    if span_type in cands:
        symbol = cands[span_type]
        return '<{}>{}</{}>'.format(symbol, _render_span(target['content'], attrs), symbol)
    if span_type in ['math_block', 'math_inline']:
        if not attrs['has_math']:
            attrs['has_math'] = True
        symbol = '$$' if span_type == 'math_block' else '$'
        return symbol + _render_span(target['content'], attrs) + symbol
    if span_type == 'inline_link':
        content, title, inner, is_img = target['content'], target['title'],\
                target['inner'], target['is_img']
        if is_img:
            return '<img src="{}" title="{}" />'.format(_render_span(content, attrs),
                                                        _render_span(inner, attrs))
        return '<a href="{}" title="{}">{}</a>'.format(_render_span(content, attrs),
                                                       _render_span(title, attrs),
                                                       _render_span(inner, attrs))
    return _render_span(target['content'], attrs)


def _render_table(target, attrs):
    header = _render_table_row(target['header'], attrs)
    body = _render_table_rows(target['body'], attrs)
    return '<table><thead>{}</thead><tbody>{}</tbody></table>'.format(header, body)


def _render_table_rows(rows, attrs):
    return '\n'.join([_render_table_row(i, attrs) for i in rows])


def _render_table_row(row, attrs):
    return '<tr>{}</tr>'.format('\n'.join([_render_table_unit(i, attrs) for i in row['content']]))


def _render_table_unit(target, attrs):
    block_type, content = target['block_type'], target['content']
    align = ['left', 'center', 'right'][target['align']]
    return '<{} align="{}">{}</{}>'.format(block_type,
                                           align, _render_span(content, attrs), block_type)
