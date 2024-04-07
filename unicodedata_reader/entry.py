import enum
import itertools
import logging
import re
import types
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Union
from typing import Tuple

_logger = logging.getLogger('UnicodeDataEntry')


def u_hex(value):
    return f'{value:04X}'


def u_enc(c, encoding):
    code = 0
    for byte in c.encode(encoding, 'ignore'):
        code = code * 256 + byte
    return u_hex(code) if code else ''


class BidiBrackets(object):

    def __init__(self, pair: int, type: str):
        self.pair = pair
        self.type = type

    @staticmethod
    def from_values(value):
        assert len(value) == 2
        return BidiBrackets(int(value[0], 16), value[1])


class EmojiType(enum.Flag):
    Emoji = enum.auto()
    Emoji_Presentation = enum.auto()
    Emoji_Modifier = enum.auto()
    Emoji_Modifier_Base = enum.auto()
    Emoji_Component = enum.auto()
    Extended_Pictographic = enum.auto()


class UnicodeDataEntry(object):
    """Represents a line in a [Unicode character database] file.

    This class consists of:
    * A range (min and max, inclusive) of Unicode code points.
    * A value for the range.

    [Unicode character database]: https://unicode.org/reports/tr44/
    """

    max_code_point = 0x10FFFF

    def __init__(self, min: int, max: int, value):
        self.min = min
        self.max = max
        self.value = value
        self.assert_range()

    def __eq__(self, other):
        return (self.min == other.min and self.max == other.max
                and self.value == other.value)

    def assert_range(self):
        assert self.max >= self.min

    def range(self):
        return range(self.min, self.max + 1)

    def is_in_range(self, code: int) -> bool:
        return code >= self.min and code <= self.max

    @property
    def count(self):
        self.assert_range()
        return self.max - self.min + 1

    def range_as_str(self):
        self.assert_range()
        if self.min == self.max:
            return u_hex(self.min)
        return f'{u_hex(self.min)}..{u_hex(self.max)}'

    def to_str(self, separator: str = ';'):
        return separator.join((self.range_as_str(), str(self.value)))

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return f'UnicodeDataEntry({self.to_str()})'

    @staticmethod
    def from_lines(lines: Iterable[str], converter=None, comment=None):
        for line in lines:
            # Skip comments.
            line = line.rstrip()
            match = re.search(r'\s*#\s*(.*)', line)
            if match:
                start_index = match.start()
                if comment:
                    comment(match.group(1), start_index)
                line = line[0:start_index]
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
                yield UnicodeDataEntry(code, code, value)
            elif len(codeRange) == 2:
                min = int(codeRange[0], 16)
                max = int(codeRange[1], 16)
                yield UnicodeDataEntry(min, max, value)
            else:
                assert False

    @staticmethod
    def from_pairs(values: Iterable[Tuple[int, Any]]):
        last_value = None
        min = -1
        last_code = -1
        for code, value in values:
            assert code > last_code
            if value == last_value and code == last_code + 1:
                last_code = code
                continue
            if min >= 0:
                yield UnicodeDataEntry(min, last_code, last_value)
            last_value = value
            min = last_code = code
        if min >= 0:
            yield UnicodeDataEntry(min, code, last_value)

    @staticmethod
    def from_values(values: Iterable[Any]):
        pairs = enumerate(values)
        pairs = (p for p in pairs if p[1] is not None)
        return UnicodeDataEntry.from_pairs(pairs)

    @staticmethod
    def values_for_code(entries, missing_value) -> Iterable[Any]:
        next = 0
        for entry in entries:
            if entry.min > next:
                yield from (missing_value(c) for c in range(next, entry.min))
            yield from itertools.repeat(entry.value, entry.count)
            next = entry.max + 1


class UnicodeDataEntries(object):
    """Represents a [Unicode character database] file,
    or a list of `UnicodeDataEntry`.
    [Unicode character database]: https://unicode.org/reports/tr44/
    """

    def __init__(self,
                 entries: Optional[Union[Iterable[UnicodeDataEntry],
                                         Sequence[UnicodeDataEntry]]] = None,
                 name: Optional[str] = None,
                 lines: Optional[Iterable[str]] = None,
                 converter=None):
        self._missing_entries = self._default_missing_entries()
        self.name = name
        self._values_for_int = None  # type: list

        if entries is not None:
            assert lines is None
            assert converter is None
            self._entries = entries
        else:
            assert lines is not None
            self._load_lines(lines, converter=converter)

    def _default_missing_entries(self) -> List[UnicodeDataEntry]:
        return []

    def _load_lines(self, lines: Iterable[str], converter=None):
        self._entries = UnicodeDataEntry.from_lines(lines,
                                                    converter=converter,
                                                    comment=self._load_comment)

    def _load_comment(self, comment: str, start_index: int):
        if start_index == 0 and comment.startswith('@missing:'):
            _logger.debug('Missing entry: %s', comment)
            entries = UnicodeDataEntry.from_lines((comment[9:].strip(), ))
            self._missing_entries.extend(entries)
            assert self._missing_entries

    def _ensure_multi_iterable(self):
        if isinstance(self._entries, types.GeneratorType):
            self._entries = tuple(self._entries)

    def __iter__(self):
        self._ensure_multi_iterable()
        return self._entries.__iter__()

    def __len__(self):
        self._ensure_multi_iterable()
        return len(self._entries)

    def __getitem__(self, code: int) -> Any:
        return self.value(code)

    def missing_value(self, code: int):
        if self._missing_entries:
            # `_missing_entries` can overlap, iterate all entries.
            for entry in self._missing_entries:
                if entry.is_in_range(code):
                    return entry.value
        return None

    def _is_contiguous(self):
        l = self._entries
        return all(l[i].max + 1 == l[i + 1].min for i in range(len(l) - 1))

    def _is_distinct(self):
        l = self._entries
        return all(l[i].max < l[i + 1].min for i in range(len(l) - 1))

    def _is_sorted(self):
        l = self._entries
        return all(l[i].min <= l[i + 1].min for i in range(len(l) - 1))

    def sort(self):
        self._entries = sorted(self._entries, key=lambda e: e.min)

    def fill_missing_values(self):
        values = UnicodeDataEntry.values_for_code(self._entries,
                                                  self.missing_value)
        self._entries = UnicodeDataEntry.from_values(values)

    def unicodes(self) -> Iterable[int]:
        """Returns a list of Unicode code points defined in this entries."""
        self._ensure_multi_iterable()
        return itertools.chain(*(e.range() for e in self._entries))

    def value(self, code: int) -> Any:
        """Returns the value for the given code point."""
        self._ensure_multi_iterable()
        for entry in self._entries:
            if code < entry.min:
                return self.missing_value(code)
            if code <= entry.max:
                return entry.value
        return self.missing_value(code)

    def filter(self, pred: Callable[[Any],
                                    bool]) -> Iterable[UnicodeDataEntry]:
        """Returns an `Iterable` of `UnicodeDataEntry` for the given `pred`."""
        return (entry for entry in self if pred(entry.value))

    def codes_for(self, pred: Callable[[Any], bool]) -> Iterable[int]:
        """Returns an `Iterable` of Unicode code points for the given `pred`."""
        return itertools.chain(*(e.range() for e in self.filter(pred)))

    def add_to_set(self, pred: Callable[[Any], bool], set: Set[int]) -> None:
        """Add values `pred` returns `True` to `set[int]`."""
        for code in self.codes_for(pred):
            set.add(code)

    def remove_from_set(self, pred: Callable[[Any], bool],
                        set: Set[int]) -> None:
        """Remove values `pred` returns `True` from `set[int]`."""
        for code in self.codes_for(pred):
            set.discard(code)

    def to_set(self, pred: Callable[[Any], bool]) -> Set[int]:
        """Returns a `set[int]` of values `pred` returns `True`."""
        s = set()  # type: set[int]
        self.add_to_set(pred, s)
        return s

    def values_for_code(self) -> Iterable[Any]:
        """Returns a list of values whose index is the Unicode code point.

        The list includes missing values,
        so that `tuple(values_for_code())[code]` is equal to `value(code)`.
        """
        self._ensure_multi_iterable()
        return UnicodeDataEntry.values_for_code(self._entries,
                                                self.missing_value)

    def values_for_int(self):
        """Returns a list of values whose index is the _integer value_.

        Returns `None` if values are not mapped to _integer values_
        by `map_values_to_int()`.
        """
        return self._values_for_int

    def map_values_to_int(self):
        """Map values to integer values.

        Useful when integers are easier to handle, or when the same values as
        the JavaScript API are needed because the `UnicodeDataCompressor` uses
        the integer values.

        Note that missing values are computed that they will not be mapped. To
        map them, `fill_missing_values()` to fill entries for missing values.

        On return, the original values are stored in `self.value_list`.
        """
        assert self._values_for_int is None
        self._ensure_multi_iterable()
        value_map = {}
        for entry in self._entries:
            assert not isinstance(entry.value, int)
            entry.value = value_map.setdefault(entry.value, len(value_map))

        value_count = len(value_map)
        value_list = [None] * value_count
        for value, index in value_map.items():
            assert index < value_count
            assert value_list[index] is None
            value_list[index] = value
        self._values_for_int = value_list

    def to_dict(self) -> Dict[int, Any]:
        """Returns a `dict` of values with a Unicode code point as the key."""
        self._ensure_multi_iterable()
        dict = {}
        for entry in self._entries:
            for code in entry.range():
                dict[code] = entry.value
        return dict


class UnicodeBidiBracketsDataEntries(UnicodeDataEntries):

    def _load_lines(self, lines: Iterable[str], converter=None):
        converter = converter or BidiBrackets.from_values
        super()._load_lines(lines, converter=converter)


class UnicodeEmojiDataEntries(UnicodeDataEntries):

    def _load_lines(self, lines: Iterable[str], converter=None):
        converter = converter or (lambda v: EmojiType[v])
        super()._load_lines(lines, converter=converter)

        # `emoji-data.txt` has multiple Emoji properties as separate lists.
        # Unite them to `EmojiType` flags.
        dict = {}
        for entry in self._entries:
            for code in entry.range():
                value = dict.get(code, EmojiType(0))
                dict[code] = value | entry.value
        items = sorted(dict.items(), key=lambda i: i[0])
        self._entries = UnicodeDataEntry.from_pairs(items)

    def _load_comment(self, comment: str, start_index: int):
        # Ignore the special `@missing` line in `emoji-data.txt`:
        # @missing: 0000..10FFFF  ; Emoji ; No
        pass

    def missing_value(self, code: int):
        return EmojiType(0)


class UnicodeLineBreakDataEntries(UnicodeDataEntries):

    def _load_comment(self, comment: str, start_index: int):
        # Load missing value entries. See the comments in:
        # https://www.unicode.org/Public/UNIDATA/LineBreak.txt
        if start_index == 0:
            m = re.search(r'\sdefault to "([A-Z]{2})":', comment)
            if m:
                self._current_missing_value = m.group(1)
                return
            m = re.search(r':\s+U\+([0-9A-F]+)\.\.U\+([0-9A-F]+)$', comment)
            if m:
                _logger.debug('Missing entry: %s; %s', comment,
                              self._current_missing_value)
                min = int(m.group(1), 16)
                max = int(m.group(2), 16)
                assert self._current_missing_value
                self._missing_entries.append(
                    UnicodeDataEntry(min, max, self._current_missing_value))
                return
        super()._load_comment(comment, start_index)


class UnicodeScriptExtensionsDataEntries(UnicodeDataEntries):

    def _load_lines(self, lines: Iterable[str], converter=None):
        converter = converter or (lambda v: v.split())
        super()._load_lines(lines, converter=converter)


class UnicodeVerticalOrientationDataEntries(UnicodeDataEntries):

    def _load_comment(self, comment: str, start_index: int):
        # Load missing value entries. See the comments in:
        # https://www.unicode.org/Public/UNIDATA/VerticalOrientation.txt
        if start_index == 0:
            m = re.search(r'\sU\+([0-9A-F]+)(\.\.U\+([0-9A-F]+))?$', comment)
            if m:
                _logger.debug('Missing entry: %s', comment)
                min = int(m.group(1), 16)
                max = m.group(3)
                max = int(max, 16) if max else min
                self._missing_entries.append(UnicodeDataEntry(min, max, 'U'))
                return
        super()._load_comment(comment, start_index)
