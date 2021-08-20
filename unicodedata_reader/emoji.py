#!/usr/bin/env python3
from unicodedata_reader import *


def dump_emoji():
    emoji = UnicodeDataReader.default.emoji().to_dict()
    columns = {'Emoji': lambda code, ch: str(emoji.get(code))}
    dump = UnicodeDataDump(columns)
    dump.print(default=emoji.keys())


if __name__ == '__main__':
    dump_emoji()
