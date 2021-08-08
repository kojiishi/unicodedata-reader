#!/usr/bin/env python3
import unicodedata

from cli_utils import *
from unicodedata_parser import *


def dump_bidi_brackets():
    parser = UnicodeDataParser()
    blocks = parser.blocks()
    bidi_brackets = parser.bidi_brackets()
    scripts = parser.scripts()
    script_extensions = parser.script_extensions()

    def bidi_brackets_type(code):
        bracket = bidi_brackets.get(code)
        return bracket.type if bracket else 'x'

    columns = {
        'Code': lambda code, ch: u_hex(code),
        'Char': lambda code, ch: chr(code),
        'Bidi_Paired_Bracket_Type': lambda code, ch: bidi_brackets_type(code),
        'EAW': lambda code, ch: unicodedata.east_asian_width(ch),
        'Script': lambda code, ch: scripts.get(code),
        'ScriptExt': lambda code, ch: str(script_extensions.get(code, [])),
    }
    print(f'# {" ".join(columns.keys())}')
    last_block = None
    for code in get_unicodes_from_args(bidi_brackets.keys()):
        block = blocks[code]
        if block != last_block:
            print(f'# {block}')
            last_block = block
        ch = chr(code)
        values = (func(code, ch) for func in columns.values())
        print(f'{" ".join(values)} # {unicodedata.name(chr(code))}')


if __name__ == '__main__':
    dump_bidi_brackets()
