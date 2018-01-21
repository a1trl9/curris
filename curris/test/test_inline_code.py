from curris.test.base import compare_json

def test_inline_code():
    compare_json('curris/test/resource/inline_code.md', 'curris/test/resource/inline_code.json')
