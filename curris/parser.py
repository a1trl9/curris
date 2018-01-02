""" parse module
"""

from curris.block import parse_block

def _proc_key(target, key):
    content = target[key]
    if isinstance(content, list) and all([isinstance(i, str) for i in content]):
        target[key] = ''.join(content)
    else:
        target[key] = _suf_process(content)


def _suf_process(target):
    if isinstance(target, dict):
        for key in target:
            _proc_key(target, key)
    elif isinstance(target, list):
        for index, line in enumerate(target):
            target[index] = _suf_process(line)
    return target


def parse(source):
    """ parse entry
    """
    target = []
    attrs = {'code_block': False}
    for line in source:
        parse_block(line, target, attrs)
    _suf_process(target)
    return target
