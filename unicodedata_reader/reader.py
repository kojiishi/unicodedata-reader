import logging
import pathlib
from typing import Iterable
import urllib.request

from unicodedata_reader.entry import *

_logger = logging.getLogger('UnicodeDataReader')


class UnicodeDataReader(object):
    """Read [Unicode character database] data files.

    This class parses data in the [Unicode character database].

    By default, it downloads the data files from
    <https://www.unicode.org/Public/UNIDATA/>.
    Custom loader can be used by the constructor argument.

    [Unicode character database]: https://unicode.org/reports/tr44/
    """

    default = None

    def bidi_brackets(self) -> UnicodeDataEntries:
        entries = self.read_entries('BidiBrackets',
                                    converter=BidiBrackets.from_values)
        return UnicodeDataEntries(entries)

    def blocks(self) -> UnicodeDataEntries:
        entries = self.read_entries('Blocks')
        return UnicodeDataEntries(entries)

    def emoji(self) -> UnicodeDataEntries:
        entries = self.read_entries('emoji/emoji-data',
                                    converter=lambda v: EmojiType[v])
        return UnicodeEmojiDataEntries(entries)

    def line_break(self) -> UnicodeDataEntries:
        entries = self.read_entries('LineBreak')
        return UnicodeLineBreakDataEntries(entries)

    def scripts(self) -> UnicodeDataEntries:
        entries = self.read_entries('Scripts')
        return UnicodeDataEntries(entries)

    def script_extensions(self) -> UnicodeDataEntries:
        entries = self.read_entries('ScriptExtensions',
                                    converter=lambda v: v.split())
        return UnicodeDataEntries(entries)

    def vertical_orientation(self) -> UnicodeDataEntries:
        entries = self.read_entries('VerticalOrientation')
        return UnicodeDataEntries(entries)

    def read_entries(self, name: str, converter=None):
        lines = self.read_lines(name)
        return UnicodeDataEntry.from_lines(lines, converter=converter)

    def read_lines(self, name: str) -> Iterable[str]:
        url = f'https://www.unicode.org/Public/UNIDATA/{name}.txt'
        with urllib.request.urlopen(url) as response:
            body = response.read().decode('utf-8')
        return body.splitlines()


class UnicodeDataCachedReader(UnicodeDataReader):
    try:
        import platformdirs
        _cache_dir = pathlib.Path(platformdirs.user_cache_dir('UNIDATA'))
        _logger.debug('cache_dir: %s', _cache_dir)
    except ModuleNotFoundError:
        _cache_dir = None

    def __init__(self, reader: UnicodeDataReader = UnicodeDataReader()):
        self._reader = reader

    def read_lines(self, name: str) -> Iterable[str]:
        cache_dir = UnicodeDataCachedReader._cache_dir
        if not cache_dir:
            return self._reader.read_lines(name)

        cache = UnicodeDataCachedReader._cache_dir / name
        if cache.exists():
            return cache.read_text().splitlines()

        lines = self._reader.read_lines(name)

        cache.parent.mkdir(parents=True, exist_ok=True)
        with cache.open('w') as file:
            for line in lines:
                print(line, file=file)

        return lines


UnicodeDataReader.default = UnicodeDataCachedReader()
