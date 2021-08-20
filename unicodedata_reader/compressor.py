#!/usr/bin/env python3
import gzip
from typing import Iterable

from unicodedata_reader import *


class UnicodeDataCompressor(object):
    def __init__(self):
        self._value_indices = {}

    def compress(self, entries: Iterable[UnicodeDataEntry]):
        buffer = bytearray()
        for entry in entries:
            self._add(entry, buffer)
        print(len(self._value_indices), len(buffer),
              len(gzip.compress(buffer)))

    def _value_index(self, value: str) -> int:
        return self._value_indices.setdefault(value, len(self._value_indices))

    def _add(self, entry: UnicodeDataEntry, buffer: bytearray):
        value_index = self._value_index(entry.value)
        print(f'{entry.min:04X} {entry.value}={value_index}: {entry.count}')
        assert value_index < 64
        assert entry.count > 0
        combined = ((entry.count - 1) << 6) | value_index
        while combined >= 0x80:
            buffer.append((combined & 0x7F) | 0x80)
            combined >>= 7
        buffer.append(combined)


def main():
    lb = UnicodeDataReader.default.line_break()
    lb.fill_missing_entries()
    compressor = UnicodeDataCompressor()
    compressor.compress(lb)


if __name__ == '__main__':
    main()
