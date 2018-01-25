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
    paq = comps[-1].split('?', 1)
    pathname, query = '', ''
    if paq:
        pathname = '/'.join([quote_plus(c) for c in paq[0].split('/')])
    if len(paq) > 1:
        query = quote_plus(paq[1])
        comps[-1] = pathname + '?' + query
    else:
        comps[-1] = pathname + query
    if comps[0] not in ['http', 'https']:
        comps[0] = 'http://' + comps[0]
    return '://'.join(comps)
