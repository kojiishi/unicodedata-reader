#!/usr/bin/env python3
from typing import Any
from typing import Callable
from typing import Dict

from unicodedata_reader import *


class UnicodeEmojiDataCli(UnicodeDataCli):
    def __init__(self):
        super().__init__()
        self.emoji_dict = UnicodeDataReader.default.emoji().to_dict()

    def _core_columns(self) -> Dict[str, Callable[[int, str], Any]]:
        return {
            'Emoji': lambda code, ch: self.emoji_dict.get(code),
        }

    def _default_unicodes(self):
        return self.emoji_dict.keys()


if __name__ == '__main__':
    UnicodeEmojiDataCli().main()
