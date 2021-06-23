#!/usr/bin/env python3
import re
import urllib.request


def _read_unicode_data_lines(name):
    url = f'https://www.unicode.org/Public/UNIDATA/{name}.txt'
    with urllib.request.urlopen(url) as response:
        body = response.read().decode('utf-8')
    return body.splitlines()


class UnicodeDataParser(object):
    """Parse [Unicode character database] data files.

    This class parses data in the [Unicode character database].

    By default, it downloads the data files from <https://www.unicode.org/Public/UNIDATA/>.
    Custom loader can be used by the constructor argument.

    [Unicode character database]: https://unicode.org/reports/tr44/
    """
    def __init__(self, read_lines=_read_unicode_data_lines):
        self._read_lines = read_lines

    def bidi_brackets(self):
        def convert_bidi_brackets_value(value):
            assert len(value) == 2
            return {"type": value[1], "pair": int(value[0], 16)}

        return self.parse('BidiBrackets', convert_bidi_brackets_value)

    def blocks(self):
        return self.parse('Blocks')

    def scripts(self):
        return self.parse('Scripts')

    def script_extensions(self):
        return self.parse('ScriptExtensions', lambda v: v.split())

    def parse(self, name, converter=None):
        lines = self._read_lines(name)
        return self.dict_from_lines(lines, converter)

    @staticmethod
    def dict_from_lines(lines, converter=None):
        dict = {}
        for line in lines:
            # Skip comments.
            line = re.sub(r'\s*#.*', '', line)
            if not line:
                continue
            # Data columns are separated by ';'.
            columns = re.split(r'\s*;\s*', line)
            assert len(columns) >= 2
            value = columns[1] if len(columns) == 2 else columns[1:]
            if converter:
                value = converter(value)
            # `columns[0]` is a code point or a range of code points.
            code = columns[0]
            codeRange = code.split('..')
            if len(codeRange) == 1:
                dict[int(code, 16)] = value
            elif len(codeRange) == 2:
                min = int(codeRange[0], 16)
                max = int(codeRange[1], 16)
                for code in range(min, max + 1):
                    dict[code] = value
            else:
                assert False
        return dict

    @staticmethod
    def hex(value):
        hexstr = hex(value)[2:].upper()
        return ('000' + hexstr)[-4:]
