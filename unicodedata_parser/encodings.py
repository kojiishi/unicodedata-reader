#!/usr/bin/env python3
import argparse
import re

from unicodedata_parser import *


def parse_unicode_list(text):
    while text:
        match = re.match(r'([0-9a-fA-F]+)', text)
        if match:
            hex = match.group(1)
            yield int(hex, 16)
            text = text[match.end():]
            continue
        yield ord(text)
        text = text[1:]


def u_enc(c, encoding):
    code = 0
    for byte in c.encode(encoding, 'ignore'):
        code = code * 256 + byte
    return u_hex(code) if code else ''


def dump_encoding():
    parser = argparse.ArgumentParser()
    parser.add_argument('text')
    args = parser.parse_args()
    encs = ['cp932', 'cp936', 'cp949', 'cp950']
    for code in parse_unicode_list(args.text):
        values = [u_hex(code)]
        ch = chr(code)
        values.extend(u_enc(ch, enc) for enc in encs)
        print('\t'.join(values))


if __name__ == '__main__':
    dump_encoding()
