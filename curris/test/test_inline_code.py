from curris.test.base import compare

def test_inline_code():
    compare('curris/test/resource/inline_code.md', 'curris/test/resource/inline_code.json')
