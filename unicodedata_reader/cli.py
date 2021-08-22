import argparse
import itertools
import re
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import Optional
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


class UnicodeDataCli(object):
    def __init__(self):
        self.text = None

    def _columns(self) -> Dict[str, Callable[[int, str], Any]]:
        columns = self._core_columns()
        columns = dict(
            itertools.chain({
                'Code': lambda code, ch: u_hex(code),
                'Char': lambda code, ch: u_printable_chr(ch),
            }.items(), columns.items(), {
                'Name': lambda code, ch: u_name_or_empty(ch),
            }.items()))
        return columns

    def _core_columns(self) -> Dict[str, Callable[[int, str], Any]]:
        raise NotImplementedError()

    def _unicodes(self) -> Optional[Iterable[int]]:
        if self.text:
            return to_unicodes(self.text)
        return self._default_unicodes()

    def _default_unicodes(self) -> Optional[Iterable[int]]:
        return None

    def print(self):
        columns = self._columns()
        print('\t'.join(key for key in columns.keys()))
        for code in self._unicodes():
            try:
                ch = chr(code)
                values = (func(code, ch) for func in columns.values())
                values = ('' if v is None else str(v) for v in values)
                print('\t'.join(values))
            except UnicodeEncodeError:
                continue

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'text', nargs='+' if self._default_unicodes() is None else '*')
        parser.parse_args(namespace=self)
        self.print()
