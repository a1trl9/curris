from curris.test.base import compare

def test_emphasis():
    compare('curris/test/resource/block_quotes.md', 'curris/test/resource/block_quotes.json')
