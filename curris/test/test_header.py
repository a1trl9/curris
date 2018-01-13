from curris.test.base import compare

def test_header():
    compare('curris/test/resource/header.md', 'curris/test/resource/header.json')
