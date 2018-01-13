from curris.test.base import compare

def test_strike_out():
    compare('curris/test/resource/strike_out.md', 'curris/test/resource/strike_out.json')
