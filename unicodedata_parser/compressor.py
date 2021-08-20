#!/usr/bin/env python3
import gzip
from typing import Iterable
from typing import Tuple

from unicodedata_parser import *


class UnicodeDataCompressor(object):
    def compress(self, code_and_values: Iterable[Tuple[int, str]]):
        buffer = bytearray()
        value_indices = {}
        next_value_index = 0
        last_value = None
        last_value_start = -1
        for code, value in code_and_values:
            assert value
            if value == last_value:
                continue

            if last_value is not None:
                value_index = value_indices.setdefault(value, next_value_index)
                if value_index == next_value_index:
                    next_value_index += 1
                count = code - last_value_start
                print(f'{code:04X} {value}={value_index}: {count}')
                self._add(value_index, count, buffer)

            last_value = value
            last_value_start = code

        print(next_value_index, len(buffer), len(gzip.compress(buffer)))

    def _add(self, value_index, count, buffer):
        buffer.append(value_index)
        while count >= 0x80:
            buffer.append((count & 0x7F) | 0x80)
            count >>= 7
        buffer.append(count)


def main():
    parser = UnicodeDataParser()
    lb = parser.line_break()
    compressor = UnicodeDataCompressor()
    compressor.compress(lb.items())


if __name__ == '__main__':
    main()
