#!/usr/bin/env python3
import argparse

from unicodedata_reader import *


def dump_encoding():
    parser = argparse.ArgumentParser()
    parser.add_argument('text', nargs='+')
    args = parser.parse_args()
    # https://docs.python.org/3/library/codecs.html#standard-encodings
    encs = ['cp932', 'cp936', 'cp949', 'cp950', 'sjis_2004']
    columns = {enc: lambda code, ch: u_enc(ch, enc) for enc in encs}
    dump = UnicodeDataDump(columns)
    dump.print()


if __name__ == '__main__':
    dump_encoding()
