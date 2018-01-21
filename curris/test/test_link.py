from curris.test.base import compare_json

def test_link():
    compare_json('curris/test/resource/link.md', 'curris/test/resource/link.json')
