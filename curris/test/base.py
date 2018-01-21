""" test base module
"""

import json

from curris.parser import parse
from curris.render.html import build_html

def compare_json(target_file, compare_file):
    """ entry function
    """
    with open(target_file) as target_reader:
        target = target_reader.read()
        parsed = parse(target)
        with open(compare_file) as compare_reader:
            compare_dict = json.loads(compare_reader.read())
            assert parsed == compare_dict


def compare_html(target_file, compare_file):
    """ entry function for html
    """
    with open(target_file) as target_reader:
        target = target_reader.read()
        parsed = parse(target)
        html = build_html(parsed)
        with open(compare_file) as compare_reader:
            compare_html = compare_reader.read()
            assert html == compare_html
