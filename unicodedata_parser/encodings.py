#!/usr/bin/env python3
import argparse

from cli_utils import *
from unicodedata_parser import *


def dump_encoding():
    parser = argparse.ArgumentParser()
    parser.add_argument('text', nargs='+')
    args = parser.parse_args()
    # https://docs.python.org/3/library/codecs.html#standard-encodings
    encs = ['cp932', 'cp936', 'cp949', 'cp950', 'sjis_2004']
    header = ['Unicode'] + encs
    print('\t'.join(header))
    for code in to_unicodes(args.text):
        values = [u_hex(code)]
        ch = chr(code)
        values.extend(u_enc(ch, enc) for enc in encs)
        print('\t'.join(values))


if __name__ == '__main__':
    dump_encoding()
