from typing import Any
from typing import Callable
from typing import Iterable
from typing import Set

from unicodedata_reader.entry import *
from unicodedata_reader.reader import *


class Set(object):
    """A simple wrapper of a `set` of Unicode code points."""

    def __init__(self,
                 entries: UnicodeDataEntries = None,
                 pred: Callable[[Any], bool] = None) -> None:
        self.set = set()  # type: Set[int]
        if entries:
            self.add_entries(entries, pred)

    def __contains__(self, code_point: int) -> bool:
        return code_point in self.set

    def __iter__(self) -> Iterable[int]:
        return self.set.__iter__()

    def __isub__(self, other: 'Set') -> 'Set':
        self.set -= other.set
        return self

    def __iand__(self, other: 'Set') -> 'Set':
        self.set &= other.set
        return self

    def __ior__(self, other: 'Set') -> 'Set':
        self.set |= other.set
        return self

    def add(self, code: int) -> None:
        self.set.add(code)

    def remove(self, code: int) -> None:
        self.set.discard(code)

    def add_entries(self, entries: UnicodeDataEntries, pred: Callable[[Any],
                                                                      bool]):
        entries.add_to_set(pred, self.set)

    @staticmethod
    def east_asian_width(
            value: str,
            reader: UnicodeDataReader = UnicodeDataReader.default) -> 'Set':
        return Set(reader.east_asian_width(), lambda v: v == value)

    @staticmethod
    def general_category(
            value: str,
            reader: UnicodeDataReader = UnicodeDataReader.default) -> 'Set':
        return Set(reader.general_category(), lambda v: v.startswith(value))

    @staticmethod
    def scripts(
            value: str,
            reader: UnicodeDataReader = UnicodeDataReader.default) -> 'Set':
        return Set(reader.scripts(), lambda v: v == value)

    @staticmethod
    def script_extensions(
            value: str,
            reader: UnicodeDataReader = UnicodeDataReader.default) -> 'Set':
        return Set(reader.script_extensions(), lambda v: value in v)
