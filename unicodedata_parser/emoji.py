#!/usr/bin/env python3
from cli_utils import *
from unicodedata_parser import *


def dump_emoji():
    parser = UnicodeDataParser()
    emoji = parser.emoji()
    for code in get_unicodes_from_args(emoji.keys()):
        values = [u_hex(code), str(emoji.get(code))]
        print('\t'.join(values))


if __name__ == '__main__':
    dump_emoji()
