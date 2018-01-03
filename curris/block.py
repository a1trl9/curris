""" Block Parser
"""

from curris.span import parse_span

def parse_block(line, target, attrs):
    """main function
    """
    if line == -1:
        _try_finalize_table(target, attrs)
        return

    length = len(line)
    if length == 0:
        _try_finalize_table(target, attrs)
        target.append({'block_type': 'blank'})
        return

    result = _handle_code_block(line, length, target, attrs) or\
            _handle_table(line, length, target, attrs)
    if result:
        return

    _try_finalize_table(target, attrs)

    result = _handle_header(line, length, target)
    if result:
        return

    result = _check_block_quotes(line, length) or _check_unorder_list_item(line, length) or \
            _check_order_list_item(line, length)
    if result:
        target.append(result)
    else:
        _handle_indent(line, length, target, attrs)


def _handle_code_block(line, length, target, attrs):
    result = _check_code_block(line, length)
    if result:
        attrs['code_block'] = not attrs['code_block']
        target.append(result)
        return True

    if attrs['code_block']:
        target.append({'block_type': 'code', 'content': line})
        return True
    return False


def _handle_table(line, length, target, attrs):
    result = _check_table(line, length)
    if result:
        if not attrs['table_block']:
            attrs['table_block'] = True
        target.append(result)
        return True
    return False


def _handle_header(line, length, target):
    result = _check_header(line, length)
    if result:
        if 'prev_block_type' in result and target:
            if 'indent' in target[-1]:
                del target[-1]['indent']
            target[-1]['block_type'] = result['prev_block_type']
        else:
            target.append(result)
        return True
    return False


def _try_finalize_table(target, attrs):
    if attrs['table_block']:
        attrs['table_block'] = False
        _build_table(target)


def _handle_indent(line, length, target, attrs):
    result = _check_indent(line, length)
    if result['indent'] == 0:
        del result['indent']
        if target and ('block_type' not in target[-1] or target[-1]['block_type'] == 'normal'):
            target[-1]['content'].append({'span_type': 'text', 'content': '\n'})
            target[-1]['content'].append(result['content'])
        else:
            target.append(result)
    elif target and 'block_type' in target[-1] and target[-1]['block_type'] in\
            ['order_list_item', 'unorder_list_item']:
        parse_block(result['content'][0], target[-1]['content'], {'code_block': False,
                                                                  'table_block': False})
    else:
        parse_block(result['content'][0], target, attrs)


def _check_header(line, length):
    """check if headers
    """
    if length * '=' == line:
        return {'prev_block_type': 'h1'}
    if length * '-' == line:
        return {'prev_block_type': 'h2'}
    if length > 0 and line[0] == '#':
        level, index = 1, 1
        while index < length and line[index] == '#':
            index += 1
            level += 1
        level = min(6, level)
        # Ignore any ending '#'
        end_index = length - 1
        while end_index >= 0 and line[end_index] == '#':
            end_index -= 1
        return {'block_type': 'h{}'.format(level),
                'content': [parse_span(line[index:end_index + 1].lstrip(), [])]}


def _check_block_quotes(line, length):
    """check if blockquotes
    """
    if length > 0 and line[0] == '>':
        index = 1
        if length > 1 and line[index] == ' ':
            index += 1
        return {'block_type': 'block_quotes', 'content': [parse_span(line[index:], [])]}

def _check_unorder_list_item(line, length):
    """check if unorder lists
    """
    if length > 1 and line[0] in '-*+' and line[1] == ' ':
        return {'block_type': 'unorder_list_item', 'content':[parse_span(line[2:], [])]}


def _check_order_list_item(line, length):
    """check if order lists
    """
    index = 0
    while index < length and line[index].isdecimal():
        index += 1
    if index + 1 < length and line[index] == '.' and line[index + 1] == ' ':
        return {'block_type': 'order_list_item', 'content': [parse_span(line[index + 2:], [])]}


def _check_code_block(line, length):
    """check if code block
    """
    if length > 2 and line[:3] == '```':
        language = line[3:]
        return {'block_type': 'code_block', 'language': language}


def _check_indent(line, length):
    if length > 1 and line[0] == '\t':
        return {'indent': 1, 'content': [line[1:]]}
    elif line[:4] == ' ' * 4:
        return {'indent': 1, 'content': [line[4:]]}
    return {'indent': 0, 'content': [parse_span(line, [])], 'block_type': 'normal'}


def _build_table(target):
    table = []
    while target and target[-1]['block_type'] == 'potential_table':
        table.append(target.pop())
    table = table[::-1]
    length = len(table)
    if length < 2:
        _build_table_as_normal(target, table)
        return
    # check header
    sep_line = table[1]
    is_seps = _check_table_seps(sep_line['content'], sep_line['seps'])
    if not is_seps['is_seps']:
        _build_table_as_normal(target, table)
        return
    info = is_seps['content']
    header = _check_table_content(table[0]['content'], table[0]['seps'],
                                  info, True)
    content = [_check_table_content(i['content'], i['seps'], info)\
            for i in table[2:]]
    table = {'block_type': 'table', 'content': {
        'header': header,
        'body': content
        }}
    target.append(table)


def _build_table_as_normal(target, table):
    content = [parse_span(i['content'], []) for i in table]
    if target and target[-1]['block_type'] == 'normal':
        for unit in content:
            target[-1]['content'].append(unit)
    else:
        target.append({'block_type': 'normal', 'content': content})


def _check_table_seps(line, seps):
    index = 0
    length = len(line)
    content = []
    if seps and seps[0] == 0:
        index += 1
        seps = seps[1:]
    for sep in seps:
        content.append(line[index:sep])
        index = sep + 1
    if seps and seps[-1] + 1 < length:
        content.append(line[index:])
    for unit in content:
        if len(unit) < 3:
            break
        if '---' not in unit or unit[0] not in ':-' or unit[-1] not in ':-':
            break
    else:
        for index, unit in enumerate(content):
            if unit[-1] == ':' and unit[0] == ':':
                content[index] = 1
            elif unit[-1] == ':':
                content[index] = 2
            else:
                content[index] = 0
        return {'is_seps': True, 'content': content}
    return {'is_seps': False}


def _check_table_content(line, seps, info, is_header=False):
    symbol = 'th' if is_header else 'td'
    index = 0
    length = len(line)
    content = []
    required = len(info)
    if seps and seps[0] == 0:
        index += 1
        seps = seps[1:]
    for sep in seps:
        content.append(line[index:sep])
        index = sep + 1
    if seps and seps[-1] + 1 < length:
        content.append(line[index:])
    for index, unit in enumerate(content):
        content[index] = {'block_type': symbol, 'content': parse_span(unit, []),
                          'align': info[index]}
    c_length = len(content)
    while c_length < required:
        content.append({'block_type': symbol, 'content': parse_span('', []),
                        'align': info[c_length]})
        c_length += 1
    return {'block_type': 'tr', 'content': content}


def _check_table(line, length):
    index = 0
    if '|' in line:
        seps = []
        while index < length:
            if line[index] == '\\':
                index += 2
                continue
            if line[index] == '|':
                seps.append(index)
            index += 1
        return {'block_type': 'potential_table', 'seps': seps,
                'content': line}
