from curris.block import _check_header

def header(level):
    return '#' * level + 'Header'


def test_header():
    for i in range(1, 20):
        content = [i for i in 'Header']
        result = {'block_type': 'h{}'.format(min(6, i)),
                  'content': [[{'span_type': 'text', 'content': content}]]}
        assert _check_header(header(i), len(header(i))) == result
