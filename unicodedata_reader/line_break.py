#!/usr/bin/env python3
import unicodedata

from unicodedata_reader import *


def dump_line_break():
    lb = UnicodeDataReader.default.line_break().to_dict()
    columns = {
        'LB': lambda code, ch: lb.get(code),
        'GC': lambda code, ch: unicodedata.category(ch),
        'EAW': lambda code, ch: unicodedata.east_asian_width(ch),
        'Name': lambda code, ch: u_name_or_empty(ch),
    }
    dump = UnicodeDataDump(columns)
    dump.print(default=lb.keys())


if __name__ == '__main__':
    dump_line_break()
