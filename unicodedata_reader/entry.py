import enum
import itertools
import logging
import re
import types
from typing import Iterable
from typing import Sequence
from typing import Union

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
    def from_lines(lines: Iterable[str], converter=None):
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
                yield UnicodeDataEntry(code, code, value)
            elif len(codeRange) == 2:
                min = int(codeRange[0], 16)
                max = int(codeRange[1], 16)
                yield UnicodeDataEntry(min, max, value)
            else:
                assert False

    @staticmethod
    def from_values(values: Iterable[str]):
        last_value = None
        min = -1
        for code, value in enumerate(values):
            if value == last_value:
                continue
            if min >= 0 and last_value is not None:
                yield UnicodeDataEntry(min, code - 1, last_value)
            last_value = value
            min = code
        if min >= 0 and last_value is not None:
            yield UnicodeDataEntry(min, code, last_value)

    @staticmethod
    def to_values(entries, missing_value):
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
    def __init__(self, entries: Union[Iterable[UnicodeDataEntry],
                                      Sequence[UnicodeDataEntry]]):
        self._entries = entries
        self._value_list = None  # type: list

    @staticmethod
    def from_values(values: Iterable[str]):
        entries = UnicodeDataEntry.from_values(values)
        return UnicodeDataEntries(entries)

    def ensure_multi_iterable(self):
        if isinstance(self._entries, types.GeneratorType):
            self._entries = tuple(self._entries)

    def __iter__(self):
        self.ensure_multi_iterable()
        return self._entries.__iter__()

    def __len__(self):
        self.ensure_multi_iterable()
        return len(self._entries)

    def missing_value(self, code: int):
        return None

    def sort(self):
        self._entries = sorted(self._entries, key=lambda e: e.min)

    def normalize(self):
        values = UnicodeDataEntry.to_values(self._entries, self.missing_value)
        self._entries = UnicodeDataEntry.from_values(values)

    def value(self, code: int):
        self.ensure_multi_iterable()
        for entry in self._entries:
            if code < entry.min:
                return self.missing_value(code)
            if code <= entry.max:
                return entry.value
        return self.missing_value(code)

    def values(self):
        self.ensure_multi_iterable()
        return UnicodeDataEntry.to_values(self._entries, self.missing_value)

    @property
    def value_list(self):
        return self._value_list

    def map_values_to_int(self):
        """Map values to integer values.

        Useful when integers are easier to handle, or when the same values as
        the JavaScript API are needed because the `UnicodeDataCompressor` uses
        the integer values.

        Note that missing values are computed that they will not be mapped. Use
        `normalize()` to fill entries for missing values.

        The original values must be hashable.
        They are stored in `self.value_list`.
        """
        self.ensure_multi_iterable()
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
        self._value_list = value_list

    def to_dict(self):
        self.ensure_multi_iterable()
        dict = {}
        for entry in self._entries:
            for code in entry.range():
                dict[code] = entry.value
        return dict


class UnicodeEmojiDataEntries(UnicodeDataEntries):
    def to_dict(self):
        dict = {}
        for entry in self:
            for code in entry.range():
                value = dict.get(code, EmojiType(0))
                dict[code] = value | entry.value
        return dict


class UnicodeLineBreakDataEntries(UnicodeDataEntries):
    def missing_value(self, code: int):
        # See the comments in:
        # https://www.unicode.org/Public/UNIDATA/LineBreak.txt
        if ((code >= 0x3400 and code <= 0x4DBF)
                or (code >= 0x4E00 and code <= 0x9FFF)
                or (code >= 0xF900 and code <= 0xFAFF)):
            return 'ID'
        if ((code >= 0x20000 and code <= 0x2FFFD)
                or (code >= 0x30000 and code <= 0x3FFFD)):
            return 'ID'
        if ((code >= 0x1F000 and code <= 0x1FAFF)
                or (code >= 0x1FC00 and code <= 0x1FFFD)):
            return 'ID'
        if code >= 0x20A0 and code <= 0x20CF:
            return 'PR'
        return 'XX'
