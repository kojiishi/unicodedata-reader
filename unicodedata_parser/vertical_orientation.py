#!/usr/bin/env python3
import unicodedata

from cli_utils import *
from unicodedata_parser import *


def dump_vertical_orientation():
    parser = UnicodeDataParser()
    vo = parser.vertical_orientation()
    columns = {
        'VO': lambda code, ch: vo.get(code),
        'GC': lambda code, ch: unicodedata.category(ch),
        'EAW': lambda code, ch: unicodedata.east_asian_width(ch),
        'cp932': lambda code, ch: u_enc(ch, 'cp932'),
        'sjis04': lambda code, ch: u_enc(ch, 'sjis_2004'),
        'cp936': lambda code, ch: u_enc(ch, 'cp936'),
        'cp949': lambda code, ch: u_enc(ch, 'cp949'),
        'cp950': lambda code, ch: u_enc(ch, 'cp950'),
    }
    dump = UnicodeDataDump(columns)
    dump.print(default=vo.keys())


if __name__ == '__main__':
    dump_vertical_orientation()
