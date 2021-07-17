#!/usr/bin/env python3
import argparse

from unicodedata_parser import *


def dump_encoding():
    parser = argparse.ArgumentParser()
    parser.add_argument('text')
    args = parser.parse_args()
    encs = ['cp932', 'cp936', 'cp949', 'cp950']
    header = ['Unicode'] + encs
    print('\t'.join(header))
    for code in to_unicodes(args.text):
        values = [u_hex(code)]
        ch = chr(code)
        values.extend(u_enc(ch, enc) for enc in encs)
        print('\t'.join(values))


if __name__ == '__main__':
    dump_encoding()
