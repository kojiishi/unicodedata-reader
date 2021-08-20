#!/usr/bin/env python3
from unicodedata_reader import *


def dump_emoji():
    emoji = UnicodeDataReader.default.emoji().to_dict()
    for code in get_unicodes_from_args(emoji.keys()):
        values = [u_hex(code), str(emoji.get(code))]
        print('\t'.join(values))


if __name__ == '__main__':
    dump_emoji()
