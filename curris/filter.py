""" process secure check for html
"""

from urllib.parse import quote_plus

def html_encode(chars):
    """ html encode
    """
    output = []
    for char in chars:
        if char == '&':
            output.append('&amp;')
        elif char == '<':
            output.append('&lt;')
        elif char == '>':
            output.append('&gt;')
        elif char == '"':
            output.append('&quot;')
        elif char == '\'':
            output.append('&#x27;')
        elif char == '/':
            output.append('&#x2F;')
        else:
            output.append(char)
    return ''.join(output)


def process_link(link):
    """ handle link check
    """
    comps = link.split('://', 1)
    comps[-1] = quote_plus(comps[-1])
    if comps[0] not in ['http', 'https']:
        comps[0] = 'http://' + comps[0]
    return '://'.join(comps)
