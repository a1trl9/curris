from curris.test.base import compare_json

def test_emphasis():
    compare_json('curris/test/resource/emphasis.md', 'curris/test/resource/emphasis.json')
