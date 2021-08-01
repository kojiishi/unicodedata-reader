#!/usr/bin/env python3
import unicodedata

from cli_utils import *
from unicodedata_parser import *


def dump_vertical_orientation():
    parser = UnicodeDataParser()
    vo = parser.vertical_orientation()
    columns = {
        'Unicode': lambda code: u_hex(code),
        'Char': lambda code: chr(code),
        'vo': lambda code: vo.get(code),
        'gc': lambda code: unicodedata.category(chr(code)),
        'eaw': lambda code: unicodedata.east_asian_width(chr(code)),
    }
    for name in ('cp932', 'cp936', 'cp949', 'cp950', 'sjis_2004'):
        columns[name] = lambda code: u_enc(chr(code), name)
    print('\t'.join(key for key in columns.keys()))
    for code in get_unicodes_from_args(vo.keys()):
        values = (func(code) for func in columns.values())
        print('\t'.join(values))


if __name__ == '__main__':
    dump_vertical_orientation()
