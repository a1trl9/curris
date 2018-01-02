""" Block Parser
"""

from curris.span import parse_span

def parse_block(line, target, attrs):
    """main function
    """
    if line and line[-1] == '\n':
        # truncate \n
        line = line[:-1]
    length = len(line)
    if length == 0:
        return
    result = _check_code_block(line, length)
    if result:
        attrs['code_block'] = not attrs['code_block']
        target.append(result)
        return
    if attrs['code_block']:
        target.append({'block_type': 'code', 'content': line})
        return

    result = _check_header(line, length)
    if result:
        if 'prev_block_type' in result:
            if 'indent' in target[-1]:
                del target[-1]['indent']
            target[-1]['block_type'] = result['prev_block_type']
        else:
            target.append(result)
        return

    result = _check_block_quotes(line, length) or _check_unorder_list_item(line, length) or \
            _check_order_list_item(line, length)
    if result:
        target.append(result)
        return

    result = _check_indent(line, length)
    if result['indent'] == 0:
        del result['indent']
        target.append(result)
    else:
        parse_block(result['content'][0], target[-1]['content'], {'code_block': False})


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
