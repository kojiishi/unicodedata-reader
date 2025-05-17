#!/usr/bin/env python3
import unicodedata
from typing import Any
from typing import Callable
from typing import Dict

from unicodedata_reader import *


class UnicodeLineBreakDataCli(UnicodeDataCli):

    def __init__(self):
        super().__init__()
        self._entries = UnicodeDataReader.default.line_break()

    def _core_columns(self) -> Dict[str, Callable[[int, str], Any]]:
        return {
            'LB': lambda code, ch: self._entries.value(code),
            'GC': lambda code, ch: unicodedata.category(ch),
            'EAW': lambda code, ch: unicodedata.east_asian_width(ch),
        }


if __name__ == '__main__':
    UnicodeLineBreakDataCli().main()
