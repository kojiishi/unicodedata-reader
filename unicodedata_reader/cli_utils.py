import argparse
import itertools
import re
import unicodedata

from unicodedata_reader import *


def _to_unicodes_from_str(text):
    while text:
        match = re.match(r'([uU]\+?)?([0-9a-fA-F]{4,5}),?\s*', text)
        if match:
            prefix = match.group(1)
            hex = match.group(2)
            if prefix or (len(hex) >= 2 and len(hex) <= 5):
                yield int(hex, 16)
                text = text[match.end():]
                continue
        yield ord(text[0])
        text = text[1:]


def to_unicodes(text):
    if isinstance(text, str):
        return _to_unicodes_from_str(text)
    return itertools.chain(*(_to_unicodes_from_str(item) for item in text))


def get_unicodes_from_args(default=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('text', nargs='+' if default is None else '*')
    args = parser.parse_args()
    if args.text:
        return to_unicodes(args.text)
    return default


def u_printable_chr(ch):
    gc = unicodedata.category(ch)
    if gc == 'Cc':
        return ''
    return ch


def u_name_or_empty(ch):
    try:
        return unicodedata.name(ch)
    except ValueError:
        return ''


class UnicodeDataDump(object):
    def __init__(self, columns=None):
        self._columns = {
            'Code': lambda code, ch: u_hex(code),
            'Char': lambda code, ch: u_printable_chr(ch),
        }
        if columns:
            self.add_columns(columns)

    def add_columns(self, columns):
        self._columns.update(columns)

    def print(self, default=None):
        columns = self._columns
        print('\t'.join(key for key in columns.keys()))
        for code in get_unicodes_from_args(default):
            try:
                ch = chr(code)
                values = (func(code, ch) for func in columns.values())
                print('\t'.join(values))
            except UnicodeEncodeError:
                continue
