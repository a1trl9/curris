""" Span Parser
"""

import re

from curris import helper

def parse_span(source, target):
    """ parse span
    TODO: simplify codes
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
        new_index = _check_strike_or_script(source, target, length, index)
        if new_index > index:
            index = new_index
            continue
        new_index = _check_math(source, target, length, index)
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
    link :: <!>?<lb><whitespace>*<link_name>whitespace*<rb>[link_definition|link_url]
    link_name :: span_element
    """
    index, is_img = start, False
    if source[index] == '!':
        is_img = True
        index += 1
    if index >= length or source[index] != '[':
        return start
    index += 1
    b_start = index
    while index < length and source[index] != ']':
        if source[index] == '\\':
            index += 2
            continue
        index += 1
    brackets = helper.elimate_whitespace_around(source[b_start:index])
    index += 1
    jumps = helper.elimate_leading_whitespace(source[index:], '[')
    index += jumps
    if index >= length or source[index] not in ':[(':
        return start
    if source[index] == ':':
        new_index = _split_link_definition(source, target, length, index + 1, brackets)
    else:
        new_index = _split_link(source, target, length, index, (brackets, is_img))
    return new_index if new_index > index else start


def _split_link_definition(source, target, length, start, brackets):
    """
    link_definition :: <colon><whitespace>+<text_element><link_title>*
    link_title :: <whitespace>*['|<lp>|"]<text_element>['|<rp>|"]
    """
    index = start
    index += helper.elimate_leading_whitespace(source[index:])
    if index >= length:
        return start
    splits = helper.split_first_whitespace(source[index:])
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
                   'title': title, 'content': content,
                   'id': brackets})
    return index


def _split_link(source, target, length, start, prev_info):
    """
    link_url :: [regular_link_url|reference_link_url]
    regular_link_url :: <lp><whitespace>*<url_and_title><whitespace>*<rp>
    reference_link_url :: <whitespace>*<lb><whitespace>*<url_and_title><whitespace>*<rb>
    url_and_title :: <text_element><whitespace>+<text_element>*
    """
    index = start
    inner, is_img = prev_info
    link_type = 'inline' if source[index] == '(' else 'refer'
    end = ')' if link_type == 'inline' else ']'
    index += 1
    next_start = index
    while index < length and source[index] != end:
        if source[index] == '\\':
            index += 2
            continue
        index += 1
    if index >= length:
        return start
    content = helper.elimate_whitespace_around(source[next_start:index])
    if link_type == 'inline':
        _check_inline_link(target, content, inner, is_img)
    else:
        target.append({'span_type': 'ref_link',
                       'inner': parse_span(inner, []), 'content': content,
                       'is_img': is_img})
    return index + 1


def _check_inline_link(target, content, inner, is_img):
    title = ''
    splits = helper.split_first_whitespace(content)
    if len(splits) > 1:
        title = splits[1]
        if len(title) > 1 and title[0] + title[-1] in ['""', '\'\'']:
            content = splits[0]
            title = title[1:-1]
    target.append({'span_type': 'inline_link',
                   'inner': parse_span(inner, []), 'content': content,
                   'title': parse_span(title, []), 'is_img': is_img})


def _check_emphasis(source, target, length, start):
    """ emphasis :: [bold_emphasis|italic_emphasis]
    bold_emphasis :: [*|_][2]<whitespace>*<span_element><whitespace>*[*|_][2]
    italic_emphasis :: [*|_]<whitespace>*<span_element><whitespace>*[*|_]
    """
    if source[start] not in '_*':
        return start
    symbol = source[start]
    index, emp_type, content = start, 'italic', []
    if index + 1 < length and source[index + 1] == symbol:
        index += 1
        emp_type = 'bold'
    index += 1
    content_start = index
    while index < length and source[index] != symbol:
        if source[index] == '\\':
            index += 2
            continue
        index += 1
    if index >= length:
        return start
    content = helper.elimate_whitespace_around(source[content_start:index])
    if emp_type == 'bold' and (index + 1 >= length or source[index + 1] != symbol):
        target.append({'span_type': 'text', 'content': [symbol]})
        emp_type = 'italic'
    target.append({'span_type': emp_type, 'content': parse_span(content, [])})
    if emp_type == 'italic':
        index += 1
    else:
        index += 2
    return index


def _check_strike_or_script(source, target, length, start):
    new_index = _check_strike_out(source, target, length, start)
    if new_index > start:
        return new_index
    new_index = _check_script(source, target, length, start)
    if new_index > start:
        return new_index
    return start


def _check_strike_out(source, target, length, start):
    if source[:2] != '~~':
        return start
    index = start + 2
    content = []
    while index + 1 < length and source[index:index + 2] != '~~':
        if source[index] == '\\':
            index += 2
            continue
        content.append(source[index])
        index += 1
    if index + 1 >= length:
        return start
    target.append({'span_type': 'strike_out', 'content': parse_span(''.join(content), [])})
    return index + 2


def _check_script(source, target, length, start):
    if source[start] not in '~^':
        return start
    symbol = source[start]
    index, content = start, []
    script_type = 'super_script' if source[start] == '^' else 'sub_script'
    index += 1
    while index < length and source[index] != symbol:
        if source[index] == '\\':
            index += 2
            continue
        content.append(source[index])
        index += 1
    if index >= length:
        return start
    target.append({'span_type': script_type, 'content': parse_span(''.join(content), [])})
    return index + 1


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


def _check_math(source, target, length, start):
    """ Although math block should be block type for HTML, we regard it as span
    to improve the robustness when parsing some text following '$$'.
    This function might require refactoring as it is almost the same as _check_emphasis.
    """
    if source[start] != '$':
        return start
    index, math_type, content = start, 'math_inline', []
    if index + 1 < length and source[index + 1] == '$':
        index += 1
        math_type = 'math_block'
    index += 1
    while index < length and source[index] != '$':
        content.append(source[index])
        index += 1
    if index >= length:
        return start
    if math_type == 'math_block' and (index + 1 >= length or source[index + 1] != '$'):
        target.append({'span_type': 'text', 'content': ['$']})
        math_type = 'math_inline'
    target.append({'span_type': math_type, 'content': ''.join(content)})
    if math_type == 'math_inline':
        index += 1
    else:
        index += 2
    return index
