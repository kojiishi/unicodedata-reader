#!/usr/bin/env python3
import argparse

from unicodedata_parser import *


def dump_emoji():
    parser = argparse.ArgumentParser()
    parser.add_argument('text', nargs='+')
    args = parser.parse_args()

    parser = UnicodeDataParser()
    emoji = parser.emoji()
    for code in to_unicodes(args.text):
        values = [u_hex(code), str(emoji.get(code))]
        print('\t'.join(values))


if __name__ == '__main__':
    dump_emoji()
