from typing import Any
from typing import Callable
from typing import Iterable
from typing import Optional

from unicodedata_reader.entry import *
from unicodedata_reader.reader import *


class Set(object):
    """A simple wrapper of a `set` of Unicode code points."""

    def __init__(self,
                 entries: Optional[UnicodeDataEntries] = None,
                 predicate: Optional[Callable[[Any], bool]] = None) -> None:
        self.set = set()
        if entries:
            entries.add_to_set(predicate, self.set)

    @staticmethod
    def east_asian_width(*values: str) -> 'Set':
        entries = UnicodeDataReader.default.east_asian_width()
        if len(values) == 1:
            value = values[0]
            return Set(entries, lambda v: v == value)
        s = set(values)
        return Set(entries, lambda v: v in s)

    @staticmethod
    def general_category(*values: str) -> 'Set':
        entries = UnicodeDataReader.default.general_category()
        if len(values) == 1:
            value = values[0]
            return Set(entries, lambda v: v.startswith(value))

        def predicate(v: str) -> bool:
            for value in values:
                if v.startswith(value):
                    return True
            return False

        return Set(entries, predicate)

    @staticmethod
    def scripts(*values: str) -> 'Set':
        entries = UnicodeDataReader.default.scripts()
        if len(values) == 1:
            value = values[0]
            return Set(entries, lambda v: v == value)
        s = set(values)
        return Set(entries, lambda v: v in s)

    @staticmethod
    def script_extensions(*values: str) -> 'Set':
        entries = UnicodeDataReader.default.script_extensions()
        if len(values) == 1:
            value = values[0]
            return Set(entries, lambda v: value in v)
        s = set(values)
        return Set(entries, lambda v: len(set(v) & s))

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
