#!/usr/bin/env python3
import unicodedata

from unicodedata_parser import UnicodeDataParser


def dump_bidi_brackets():
    parser = UnicodeDataParser()
    blocks = parser.blocks()
    bidi_brackets = parser.bidi_brackets()
    scripts = parser.scripts()
    script_extensions = parser.script_extensions()
    print(
        '# Code Bidi_Paired_Bracket_Type East_Asian_Width Script Script_Extensions'
    )
    last_block = None
    for code in bidi_brackets.keys():
        block = blocks[code]
        if block != last_block:
            print(f'# {block}')
            last_block = block
        row = [
            UnicodeDataParser.hex(code),
            bidi_brackets[code].type,
            unicodedata.east_asian_width(chr(code)),
            scripts.get(code),
            str(script_extensions.get(code, [])),
        ]
        print(f'{" ".join(row)} # {unicodedata.name(chr(code))}')


if __name__ == '__main__':
    dump_bidi_brackets()
