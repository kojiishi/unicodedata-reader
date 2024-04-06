from typing import Callable

from unicodedata_reader.entry import *
from unicodedata_reader.reader import *


class Set(object):
    """A simple set of Unicode code points."""

    def __init__(self) -> None:
        self.set = set()  # type: set[int]

    def __contains__(self, code_point: int) -> bool:
        return code_point in self.set

    def __iter__(self) -> Iterable[int]:
        return self.set.__iter__()

    def __isub__(self, other: 'Set') -> None:
        self.set -= other.set

    def __iand__(self, other: 'Set') -> None:
        self.set &= other.set

    def __ior__(self, other: 'Set') -> None:
        self.set |= other.set

    def add(self, code: int) -> None:
        self.set.add(code)

    def remove(self, code: int) -> None:
        self.set.discard(code)

    def add_entries(self, entries: UnicodeDataEntries, pred: Callable[[Any],
                                                                      bool]):
        for entry in entries:
            if pred(entry.value):
                for code in entry.range():
                    self.set.add(code)

    @staticmethod
    def east_asian_width(
            value: str,
            reader: UnicodeDataReader = UnicodeDataReader.default) -> 'Set':
        set = Set()
        set.add_entries(reader.east_asian_width(), lambda v: v == value)
        return set

    @staticmethod
    def general_category(
            value: str,
            reader: UnicodeDataReader = UnicodeDataReader.default) -> 'Set':
        set = Set()
        set.add_entries(reader.general_category(),
                        lambda v: v.startswith(value))
        return set

    @staticmethod
    def scripts(
            value: str,
            reader: UnicodeDataReader = UnicodeDataReader.default) -> 'Set':
        set = Set()
        set.add_entries(reader.scripts(), lambda v: v == value)
        return set

    @staticmethod
    def script_extensions(
            value: str,
            reader: UnicodeDataReader = UnicodeDataReader.default) -> 'Set':
        set = Set()
        set.add_entries(reader.script_extensions(), lambda v: value in v)
        return set
