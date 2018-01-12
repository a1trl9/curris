""" test base module
"""

import json

from curris.parser import parse

def compare(target_file, compare_file):
    """ entry function
    """
    with open(target_file) as target_reader:
        target = target_reader.read()
        parsed = parse(target)
        with open(compare_file) as compare_reader:
            compare_dict = json.loads(compare_reader.read())
            assert parsed == compare_dict
