from curris.test.base import compare_json

def test_script():
    compare_json('curris/test/resource/script.md', 'curris/test/resource/script.json')
