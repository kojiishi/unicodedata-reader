import argparse
import itertools
import logging
import pathlib
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
        match = re.match(
            r'([uU]\+?)?([0-9a-fA-F]{4,5})(-([0-9a-fA-F]{4,5}))?,?\s*', text)
        if match:
            prefix = match.group(1)
            hex = match.group(2)
            if prefix or (len(hex) >= 2 and len(hex) <= 5):
                code = int(hex, 16)
                hex_end = match.group(4)
                if hex_end:
                    yield from range(code, int(hex_end, 16) + 1)
                else:
                    yield code
                text = text[match.end():]
                continue
        code = ord(text[0])
        yield code
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


def _init_logging(verbose):
    if verbose <= 0:
        return
    if verbose <= 1:
        logging.basicConfig(level=logging.INFO)
        return
    logging.basicConfig(level=logging.DEBUG)


class UnicodeDataCli(object):

    def __init__(self):
        self._parse_args()

    def _columns(self) -> Dict[str, Callable[[int, str], Any]]:
        columns = self._core_columns()
        columns = dict(
            itertools.chain({
                'Code': lambda code, ch: 'U' + u_hex(code),
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
        return self._entries.unicodes()

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

    def substitute_template(self, template: pathlib.Path,
                            output: pathlib.Path):
        entries = self._entries
        entries.fill_missing_values()
        entries.map_values_to_int()
        output = output if output else template.parent
        compressor = UnicodeDataCompressor(entries)
        compressor.substitute_template(template, name=self.name, output=output)

    def _parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('text',
                            nargs='*',
                            help='show properties for the text')
        parser.add_argument('-f', '--clear-cache', action='store_true')
        parser.add_argument('-F', '--no-cache', action='store_true')
        parser.add_argument('--name', help='$NAME in the template')
        parser.add_argument('-t',
                            '--template',
                            type=pathlib.Path,
                            help='generate a file from the template')
        parser.add_argument('-o', '--output', type=pathlib.Path)
        parser.add_argument('-v',
                            '--verbose',
                            help='increase output verbosity',
                            action='count',
                            default=0)
        parser.parse_args(namespace=self)
        _init_logging(self.verbose)  # pytype: disable=attribute-error
        if self.clear_cache:
            UnicodeDataCachedReader.clear_cache()
        if self.no_cache:
            UnicodeDataReader.default = UnicodeDataReader()

    def main(self):
        if self.template:
            self.substitute_template(self.template, self.output)
            return
        self.print()
