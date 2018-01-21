from curris.test.base import compare_json

def test_strike_out():
    compare_json('curris/test/resource/strike_out.md', 'curris/test/resource/strike_out.json')
