from curris.block import _check_code_block

def code_block(language=''):
    return '```' + language

def test_code_block():
    assert _check_code_block(code_block(), len(code_block()))\
            == {'block_type': 'code_block', 'language': ''}
    assert _check_code_block(code_block('python'), len(code_block('python'))) ==\
            {'block_type': 'code_block', 'language': 'python'}
