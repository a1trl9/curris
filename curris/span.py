""" Span Parser
"""

import re

def parse_span(source, target):
    """ parse span
    """
    index, length = 0, len(source)
    while index < length:
        new_index = _check_link(source, target, length, index)
        if new_index > index:
            index = new_index
            continue
        new_index = _check_emphasis(source, target, length, index)
        if new_index > index:
            index = new_index
            continue
        new_index = _check_code(source, target, length, index)
        if new_index > index:
            index = new_index
            continue
        if source[index] == '\\':
            index += 1
            if index >= length:
                break
        if target and target[-1]['span_type'] == 'text':
            target[-1]['content'].append(source[index])
        else:
            target.append({'span_type': 'text', 'content': [source[index]]})
        index += 1
    return target


def _check_link(source, target, length, start):
    """ check inline link, link reference or link definition
    """
    index, is_img = start, False
    if source[index] == '!':
        is_img = True
        index += 1
    if index >= length or source[index] != '[':
        return start
    brackets = []
    index += 1
    while index < length and source[index] != ']':
        if source[index] == '\\':
            index += 2
            continue
        brackets.append(source[index])
        index += 1
    index += 1
    if source[index:index + 2] == ' [':
        index += 1
    elif index >= length or source[index] not in ':[(':
        return start
    if source[index] == ':':
        index = _split_link_definition(source, target, length, index + 1, brackets)
    else:
        index = _split_link(source, target, length, index, (brackets, is_img))
    return index

def _split_link_definition(source, target, length, start, brackets):
    index = start
    comp = re.compile('[ \t]+')
    splits = comp.split(source[index:], 2)
    if splits[0] != '':
        return index
    splits = splits[1:]
    content = splits[0]
    title = ''
    if len(splits) > 1:
        index += source[index:].index(splits[1])
        if source[index] in '"\'(':
            end = source[index] if source[index] in '\'"' else ')'
            index += 1
            tmp_start = index
            while index < length and source[index] != end:
                if source[index] == '\\':
                    index += 2
                else:
                    index += 1
            if index < length and (index + 1 == length or source[index + 1] in ' \t'):
                title = source[tmp_start:index]
                index += 2
            else:
                index = start + len(content)
        else:
            index = start + len(content)
    else:
        index = length
    target.append({'span_type': 'link_definition',
                   'title': parse_span(title, []), 'content': content,
                   'id': ''.join(brackets)})
    return index

def _split_link(source, target, length, start, prev_info):
    index = start
    brackets, is_img = prev_info
    next_part = []
    link_type = 'inline' if source[index] == '(' else 'refer'
    end = ')' if link_type == 'inline' else ']'
    index += 1
    while index < length and source[index] != end:
        if source[index] == '\\':
            index += 2
            continue
        next_part.append(source[index])
        index += 1
    if index >= length:
        return start
    inner, content = ''.join(brackets), ''.join(next_part)
    if link_type == 'inline':
        _check_inline_link(target, content, inner, is_img)
    else:
        target.append({'span_type': 'ref_link',
                       'inner': parse_span(inner, []), 'content': content,
                       'is_img': is_img})
    return index + 1


def _check_inline_link(target, content, inner, is_img):
    title = ''
    comp = re.compile('[ \t]+')
    splits = comp.split(content, 1)
    if len(splits) > 1:
        title = splits[1]
        if len(title) > 1 and title[0] + title[-1] in ['""', '\'\'']:
            content = splits[0]
            title = title[1:-1]
    target.append({'span_type': 'inline_link',
                   'inner': parse_span(inner, []), 'content': content,
                   'title': parse_span(title, []), 'is_img': is_img})


def _check_emphasis(source, target, length, start):
    if source[start] not in '_*':
        return start
    symbol = source[start]
    index, emp_type, content = start, 'italic', []
    if index + 1 < length and source[index + 1] == symbol:
        index += 1
        emp_type = 'bold'
    index += 1
    while index < length and source[index] != symbol:
        if source[index] == '\\':
            index += 2
            continue
        content.append(source[index])
        index += 1
    if index >= length:
        return start
    if emp_type == 'bold' and (index + 1 >= length or source[index + 1] != symbol):
        target.append({'span_type': 'text', 'content': [symbol]})
        emp_type = 'italic'
    target.append({'span_type': emp_type, 'content': parse_span(''.join(content), [])})
    if emp_type == 'italic':
        index += 1
    else:
        index += 2
    return index

def _check_code(source, target, length, start):
    index = start
    if source[index] != '`':
        return index
    index += 1
    double_back = True if index < length and source[index] == '`' else False
    if double_back:
        index += 1
    if double_back and index >= length:
        target.append({'span_type': 'inline_code', 'content': ''})
        return index
    while index < length and source[index] != '`':
        if source[index] == '\\':
            index += 2
            continue
        index += 1
    if index >= length:
        return start
    if double_back:
        return _check_double_back(source, target, start, index, length)
    return _check_single_back(source, target, start, index, length)


def _check_double_back(source, target, start, index, length):
    if index + 1 >= length:
        target.append({'span_type': 'inline_code',
                       'content': source[start + 1:index]})
        return index + 1
    if source[index + 1] == '`':
        target.append({'span_type': 'inline_code',
                       'content': source[start + 2:index]})
        return index + 2
    else:
        tmp_index = index
    index += 1
    while index + 1 < length and source[index:index + 2] != '``':
        if source[index] == '\\':
            index += 2
            continue
        index += 1
    if index + 1 >= length:
        target.append({'span_type': 'inline_code',
                       'content': source[start + 1:tmp_index]})
        return tmp_index + 1
    target.append({'span_type': 'inline_code', 'content': source[start + 2:index]})
    return index + 2


def _check_single_back(source, target, start, index, length):
    while index < length and source[index] != '`':
        if source[index] == '\\':
            index += 2
            continue
        index += 1
    if index >= length:
        return start
    target.append({'span_type': 'inline_code', 'content': source[start + 1:index]})
    return index + 1
