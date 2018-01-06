""" cli support for this module
"""

import argparse
import json

from curris.parser import parse
from curris.render.html import build_html
from curris.render.render_to_file import render_to_file

def _build_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-html', action='store_true', help='render to html')
    parser.add_argument('-css', help='add css source file')
    parser.add_argument('-o', help='output file path')
    parser.add_argument('-s', help='source file path')
    return parser


def main():
    """ cli entry
    """
    arg_parser = _build_arg_parser()
    args = arg_parser.parse_args()

    if not args.s:
        return

    parsed = ''
    with open(args.s) as reader:
        target = reader.read()
        parsed = parse(target)

    if args.html:
        file_type = 'html'
        css_source = args.css if args.css else None
        rendered = build_html(parsed, css_source)
    else:
        file_type = 'json'
        rendered = json.dumps(parsed)

    if args.o:
        render_to_file(rendered, args.o)
    else:
        file_path = 'output.' + file_type
        render_to_file(rendered, file_path)
