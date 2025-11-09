import logging
from pathlib import Path
from typing import Iterable
from typing import Optional
import shutil
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

    def __init__(
        self,
        url_template: str = 'https://www.unicode.org/Public/UNIDATA/{0}.txt'
    ) -> None:
        self.url_template = url_template

    class Context(object):
        """This class changes `UnicodeDataReader.default` while in the context,
        and restores when exit."""

        def __init__(self, reader: 'UnicodeDataReader') -> None:
            self.reader = reader

        def __enter__(self):
            self.saved_default = UnicodeDataReader.default
            UnicodeDataReader.default = self.reader
            return self.reader

        def __exit__(self, exc_type, exc_val, exc_tb):
            UnicodeDataReader.default = self.saved_default
            return None

    def bidi_brackets(self) -> UnicodeDataEntries:
        name = 'BidiBrackets'
        lines = self.read_lines(name)
        return UnicodeBidiBracketsDataEntries(name=name, lines=lines)

    def blocks(self) -> UnicodeDataEntries:
        name = 'Blocks'
        lines = self.read_lines(name)
        return UnicodeDataEntries(name=name, lines=lines)

    def east_asian_width(self) -> UnicodeDataEntries:
        name = 'EastAsianWidth'
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

    def name(self) -> UnicodeDataEntries:
        lines = self.read_lines('extracted/DerivedName')
        entries = UnicodeDataEntries(name='Name', lines=lines)
        return entries

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

    def get_url(self, name: str) -> str:
        return self.url_template.format(name)

    def read_lines(self, name: str) -> Iterable[str]:
        url = self.get_url(name)
        _logger.debug('Downloading %s', url)
        with urllib.request.urlopen(url) as response:
            body = response.read().decode('utf-8')
        return body.splitlines(keepends=True)


class UnicodeDataCachedReader(UnicodeDataReader):
    try:
        import platformdirs
        _default_cache_dir = Path(platformdirs.user_cache_dir('UNIDATA'))
        _logger.debug('cache_dir: %s', _default_cache_dir)
    except ModuleNotFoundError:
        _default_cache_dir = None

    def __init__(self,
                 reader: UnicodeDataReader = UnicodeDataReader(),
                 cache_dir: Optional[Path] = None):
        self._reader = reader
        self._cache_dir = cache_dir

    def read_lines(self, name: str) -> Iterable[str]:
        cache = self._cache_path(name)
        if cache and cache.exists():
            _logger.debug('Reading cache %s', cache)
            return cache.read_text(encoding='utf-8').splitlines(keepends=True)

        lines = self._reader.read_lines(name)

        if cache:
            cache.parent.mkdir(parents=True, exist_ok=True)
            with cache.open('w', encoding='utf-8') as file:
                _logger.debug('Writing cache %s', cache)
                file.writelines(lines)

        return lines

    def _cache_path(self, name: str) -> Optional[Path]:
        if not UnicodeDataCachedReader.is_caching_allowed:
            return None
        if self._cache_dir:
            return self._cache_dir / name
        cache_dir = UnicodeDataCachedReader._default_cache_dir
        if cache_dir:
            return cache_dir / name
        return None

    @staticmethod
    def clear_cache(ignore_errors: bool = False):
        cache_dir = UnicodeDataCachedReader._default_cache_dir
        if cache_dir and cache_dir.exists():
            _logger.debug('Deleting cache %s', cache_dir)
            shutil.rmtree(cache_dir, ignore_errors=ignore_errors)


UnicodeDataReader.default = UnicodeDataCachedReader()
