from curris.test.base import compare

def test_script():
    compare('curris/test/resource/script.md', 'curris/test/resource/script.json')
