#!/usr/bin/env python3
import unicodedata

from cli_utils import *
from unicodedata_parser import *


def dump_vertical_orientation():
    parser = UnicodeDataParser()
    vo = parser.vertical_orientation()
    for code in get_unicodes_from_args(vo.keys()):
        ch = chr(code)
        values = [u_hex(code), vo.get(code), unicodedata.east_asian_width(ch)]
        print('\t'.join(values))


if __name__ == '__main__':
    dump_vertical_orientation()
