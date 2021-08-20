#!/usr/bin/env python3
import unicodedata

from unicodedata_reader import *


def dump_vertical_orientation():
    vo = UnicodeDataReader.default.vertical_orientation().to_dict()
    columns = {
        'VO': lambda code, ch: vo.get(code),
        'GC': lambda code, ch: unicodedata.category(ch),
        'EAW': lambda code, ch: unicodedata.east_asian_width(ch),
        'cp932': lambda code, ch: u_enc(ch, 'cp932'),
        'sjis04': lambda code, ch: u_enc(ch, 'sjis_2004'),
        'cp936': lambda code, ch: u_enc(ch, 'cp936'),
        'cp949': lambda code, ch: u_enc(ch, 'cp949'),
        'cp950': lambda code, ch: u_enc(ch, 'cp950'),
        'Name': lambda code, ch: u_name_or_empty(ch),
    }
    dump = UnicodeDataDump(columns)
    dump.print(default=vo.keys())


if __name__ == '__main__':
    dump_vertical_orientation()
