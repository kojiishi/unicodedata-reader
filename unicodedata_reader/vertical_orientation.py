#!/usr/bin/env python3
import unicodedata
from typing import Any
from typing import Callable
from typing import Dict

from unicodedata_reader import *


class UnicodeVerticalOrientationDataCli(UnicodeDataCli):

    def __init__(self):
        super().__init__()
        self._entries = UnicodeDataReader.default.vertical_orientation()

    def _core_columns(self) -> Dict[str, Callable[[int, str], Any]]:
        return {
            'VO': lambda code, ch: self._entries.value(code),
            'GC': lambda code, ch: unicodedata.category(ch),
            'EAW': lambda code, ch: unicodedata.east_asian_width(ch),
            'cp932': lambda code, ch: u_enc(ch, 'cp932'),
            'sjis04': lambda code, ch: u_enc(ch, 'sjis_2004'),
            'cp936': lambda code, ch: u_enc(ch, 'cp936'),
            'cp949': lambda code, ch: u_enc(ch, 'cp949'),
            'cp950': lambda code, ch: u_enc(ch, 'cp950'),
        }


if __name__ == '__main__':
    UnicodeVerticalOrientationDataCli().main()
