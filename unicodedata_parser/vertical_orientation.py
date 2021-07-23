#!/usr/bin/env python3
import argparse
import unicodedata

from unicodedata_parser import *


def dump_vertical_orientation():
    parser = argparse.ArgumentParser()
    parser.add_argument('text', nargs='*')
    args = parser.parse_args()

    parser = UnicodeDataParser()
    vo = parser.vertical_orientation()
    if args.text:
        unicodes = to_unicodes(args.text)
    else:
        unicodes = vo.keys()
    for code in unicodes:
        ch = chr(code)
        values = [u_hex(code), vo.get(code), unicodedata.east_asian_width(ch)]
        print('\t'.join(values))


if __name__ == '__main__':
    dump_vertical_orientation()
