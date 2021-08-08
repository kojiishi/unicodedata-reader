#!/usr/bin/env python3
import unicodedata

from cli_utils import *
from unicodedata_parser import *


def dump_vertical_orientation():
    parser = UnicodeDataParser()
    vo = parser.vertical_orientation()
    columns = {
        'Code': lambda code, ch: u_hex(code),
        'Char': lambda code, ch: chr(code),
        'VO': lambda code, ch: vo.get(code),
        'GC': lambda code, ch: unicodedata.category(ch),
        'EAW': lambda code, ch: unicodedata.east_asian_width(ch),
        'cp932': lambda code, ch: u_enc(ch, 'cp932'),
        'sjis04': lambda code, ch: u_enc(ch, 'sjis_2004'),
        'cp936': lambda code, ch: u_enc(ch, 'cp936'),
        'cp949': lambda code, ch: u_enc(ch, 'cp949'),
        'cp950': lambda code, ch: u_enc(ch, 'cp950'),
    }
    print('\t'.join(key for key in columns.keys()))
    for code in get_unicodes_from_args(vo.keys()):
        ch = chr(code)
        values = (func(code, ch) for func in columns.values())
        print('\t'.join(values))


if __name__ == '__main__':
    dump_vertical_orientation()
