from curris.test.base import compare_json

def test_header():
    compare_json('curris/test/resource/header.md', 'curris/test/resource/header.json')
