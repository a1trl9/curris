from curris.test.base import compare_json

def test_emphasis():
    compare_json('curris/test/resource/block_quotes.md', 'curris/test/resource/block_quotes.json')
