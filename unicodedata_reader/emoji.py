#!/usr/bin/env python3
from typing import Any
from typing import Callable
from typing import Dict

from unicodedata_reader import *


class UnicodeEmojiDataCli(UnicodeDataCli):
    def __init__(self):
        super().__init__()
        self._entries = UnicodeDataReader.default.emoji()

    def _core_columns(self) -> Dict[str, Callable[[int, str], Any]]:
        return {
            'Emoji': lambda code, ch: self._entries.value(code),
        }


if __name__ == '__main__':
    UnicodeEmojiDataCli().main()
