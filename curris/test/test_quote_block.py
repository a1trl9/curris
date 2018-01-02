from curris.block import _check_block_quotes

def quote_block():
    return '> test'

def test_code_block():
    content = [[{'content': [i for i in 'test'], 'span_type': 'text'}]]
    assert _check_block_quotes(quote_block(), len(quote_block()))\
            == {'block_type': 'block_quotes', 'content': content}
