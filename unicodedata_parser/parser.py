#!/usr/bin/env python3
import collections
import enum
import logging
import pathlib
import re
import urllib.request

_logger = logging.getLogger('UnicodeDataParser')


def u_hex(value):
    return f'{value:04X}'


def u_enc(c, encoding):
    code = 0
    for byte in c.encode(encoding, 'ignore'):
        code = code * 256 + byte
    return u_hex(code) if code else ''


BidiBrackets = collections.namedtuple('BidiBrackets', ['pair', 'type'])


class EmojiType(enum.Flag):
    Emoji = enum.auto()
    Emoji_Presentation = enum.auto()
    Emoji_Modifier = enum.auto()
    Emoji_Modifier_Base = enum.auto()
    Emoji_Component = enum.auto()
    Extended_Pictographic = enum.auto()


class UnicodeDataReader(object):
    default = None  # type: UnicodeDataReader

    try:
        import platformdirs
        _cache_dir = pathlib.Path(platformdirs.user_cache_dir('UNIDATA'))
        _logger.debug('cache_dir: %s', _cache_dir)
    except ModuleNotFoundError:
        _cache_dir = None

    def readlines(self, name: str):
        cache = None
        if UnicodeDataReader._cache_dir:
            cache = UnicodeDataReader._cache_dir / name
            if cache.exists():
                return cache.read_text().splitlines()

        url = f'https://www.unicode.org/Public/UNIDATA/{name}.txt'
        with urllib.request.urlopen(url) as response:
            body = response.read().decode('utf-8')

        if cache:
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(body)

        return body.splitlines()


UnicodeDataReader.default = UnicodeDataReader()


class UnicodeDataParser(object):
    """Parse [Unicode character database] data files.

    This class parses data in the [Unicode character database].

    By default, it downloads the data files from
    <https://www.unicode.org/Public/UNIDATA/>.
    Custom loader can be used by the constructor argument.

    [Unicode character database]: https://unicode.org/reports/tr44/
    """
    def __init__(self, reader: UnicodeDataReader = None):
        self._reader = reader

    def bidi_brackets(self):
        def convert_bidi_brackets_value(value):
            assert len(value) == 2
            return BidiBrackets(int(value[0], 16), value[1])

        return self.parse('BidiBrackets', convert_bidi_brackets_value)

    def blocks(self):
        return self.parse('Blocks')

    def emoji(self):
        dict = {}

        def setter(code, value):
            value |= dict.get(code, EmojiType(0))
            dict[code] = value

        lines = self._readlines('emoji/emoji-data')
        self.parse_lines(lines, setter, converter=lambda v: EmojiType[v])
        return dict

    def line_break(self):
        return self.parse('LineBreak')

    def scripts(self):
        return self.parse('Scripts')

    def script_extensions(self):
        return self.parse('ScriptExtensions', lambda v: v.split())

    def vertical_orientation(self):
        return self.parse('VerticalOrientation')

    def parse(self, name, converter=None):
        lines = self._readlines(name)
        return self.dict_from_lines(lines, converter)

    def _readlines(self, name):
        reader = self._reader or UnicodeDataReader.default
        return reader.readlines(name)

    @staticmethod
    def dict_from_lines(lines, converter=None):
        dict = {}

        def setter(code, value):
            dict[code] = value

        UnicodeDataParser.parse_lines(lines, setter, converter=converter)
        return dict

    @staticmethod
    def parse_lines(lines, setter, converter=None):
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
                code = int(code, 16)
                setter(code, value)
            elif len(codeRange) == 2:
                min = int(codeRange[0], 16)
                max = int(codeRange[1], 16)
                for code in range(min, max + 1):
                    setter(code, value)
            else:
                assert False

    @staticmethod
    def hex(value):
        return u_hex(value)
