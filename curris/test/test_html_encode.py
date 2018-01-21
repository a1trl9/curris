from curris.test.base import compare_html

def test_html_encode():
    compare_html('curris/test/resource/html_encode.md', 'curris/test/resource/html_encode.html')
