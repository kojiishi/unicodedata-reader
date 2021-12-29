#!/usr/bin/env python3
from typing import Any
from typing import Callable
from typing import Dict

from unicodedata_reader import *


class UnicodeEmojiDataCli(UnicodeDataCli):

    def __init__(self):
        super().__init__()
        self._entries = UnicodeDataReader.default.emoji()

    def _emoji_flag_func(self, mask: EmojiType):
        return lambda code, ch: 1 if self._entries.value(code) & mask else 0

    def _core_columns(self) -> Dict[str, Callable[[int, str], Any]]:
        return {
            'Emoji':
            self._emoji_flag_func(EmojiType.Emoji),
            'Emoji_Presentation':
            self._emoji_flag_func(EmojiType.Emoji_Presentation),
            'Emoji_Modifier':
            self._emoji_flag_func(EmojiType.Emoji_Modifier),
            'Emoji_Modifier_Base':
            self._emoji_flag_func(EmojiType.Emoji_Modifier_Base),
            'Emoji_Component':
            self._emoji_flag_func(EmojiType.Emoji_Component),
            'Extended_Pictographic':
            self._emoji_flag_func(EmojiType.Extended_Pictographic),
            'EmojiCombined':
            lambda code, ch: self._entries.value(code),
        }


if __name__ == '__main__':
    UnicodeEmojiDataCli().main()
