#!/usr/bin/env python3
import argparse

from unicodedata_parser import *


def dump_vertical_orientation():
    parser = argparse.ArgumentParser()
    parser.add_argument('text')
    args = parser.parse_args()

    parser = UnicodeDataParser()
    vo = parser.vertical_orientation()
    for code in to_unicodes(args.text):
        values = [u_hex(code), vo.get(code)]
        print(*values)


if __name__ == '__main__':
    dump_vertical_orientation()
