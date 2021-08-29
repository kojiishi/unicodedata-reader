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
    is_caching_allowed = True

    def bidi_brackets(self) -> UnicodeDataEntries:
        name = 'BidiBrackets'
        lines = self.read_lines(name)
        return UnicodeBidiBracketsDataEntries(name=name, lines=lines)

    def blocks(self) -> UnicodeDataEntries:
        name = 'Blocks'
        lines = self.read_lines(name)
        return UnicodeDataEntries(name=name, lines=lines)

    def emoji(self) -> UnicodeDataEntries:
        lines = self.read_lines('emoji/emoji-data')
        return UnicodeEmojiDataEntries(name='Emoji', lines=lines)

    def general_category(self) -> UnicodeDataEntries:
        lines = self.read_lines('extracted/DerivedGeneralCategory')
        entries = UnicodeDataEntries(name='GeneralCategory', lines=lines)
        # `extracted/DerivedGeneralCategory` is not sorted.
        entries.sort()
        return entries

    def line_break(self) -> UnicodeDataEntries:
        name = 'LineBreak'
        lines = self.read_lines(name)
        return UnicodeLineBreakDataEntries(name=name, lines=lines)

    def scripts(self) -> UnicodeDataEntries:
        name = 'Scripts'
        lines = self.read_lines(name)
        return UnicodeDataEntries(name=name, lines=lines)

    def script_extensions(self) -> UnicodeDataEntries:
        name = 'ScriptExtensions'
        lines = self.read_lines(name)
        return UnicodeScriptExtensionsDataEntries(name=name, lines=lines)

    def vertical_orientation(self) -> UnicodeDataEntries:
        name = 'VerticalOrientation'
        lines = self.read_lines(name)
        return UnicodeVerticalOrientationDataEntries(name=name, lines=lines)

    def read_lines(self, name: str) -> Iterable[str]:
        url = f'https://www.unicode.org/Public/UNIDATA/{name}.txt'
        _logger.debug('Downloading %s', url)
        with urllib.request.urlopen(url) as response:
            body = response.read().decode('utf-8')
        return body.splitlines(keepends=True)


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
        if UnicodeDataCachedReader.is_caching_allowed and cache.exists():
            _logger.debug('Reading cache %s', cache)
            return cache.read_text().splitlines(keepends=True)

        lines = self._reader.read_lines(name)

        cache.parent.mkdir(parents=True, exist_ok=True)
        with cache.open('w') as file:
            _logger.debug('Writing cache %s', cache)
            file.writelines(lines)

        return lines


UnicodeDataReader.default = UnicodeDataCachedReader()
