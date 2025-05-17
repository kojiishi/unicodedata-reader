#!/usr/bin/env python3
import unicodedata
from typing import Any
from typing import Callable
from typing import Dict

from unicodedata_reader import *


class UnicodeGeneralCategoryDataCli(UnicodeDataCli):

    def __init__(self):
        super().__init__()
        self._entries = UnicodeDataReader.default.general_category()

    def _core_columns(self) -> Dict[str, Callable[[int, str], Any]]:
        return {
            'GC': lambda code, ch: self._entries.value(code),
        }


if __name__ == '__main__':
    UnicodeGeneralCategoryDataCli().main()
