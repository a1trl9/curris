""" common helper module
"""

def elimate_whitespace_around(source):
    """ return contents surrounded by whitespaces.
    whitespace :: space | tab
    """
    if not source:
        return source
    start, length = 0, len(source)
    end, whitespace = length - 1, ' \t'
    while start < length:
        if source[start] not in whitespace:
            break
        start += 1
    while end >= 0:
        if source[end] not in whitespace:
            break
        end -= 1
    return source[start:end + 1]


def elimate_leading_whitespace(source, target=None):
    """ return the count of whitespaces before the first target
    if it is not the mode: <whitespace>*_target_, return 0
    """
    if not source:
        return 0
    i, length = 0, len(source)
    while i < length:
        if source[i] not in ' \t':
            if (target and source[i] == target) or target is None:
                return i
            return 0
        i += 1
    return 0


def split_first_whitespace(source):
    """ split source by first <whitespace>*
    """
    if not source:
        return [source]
    i, length = 0, len(source)
    while i < length:
        if source[i] in ' \t':
            temp = i
            i += 1
            while i < length and source[i] in ' \t':
                i += 1
            return [source[:temp], source[i:]]
        i += 1
    return [source]
