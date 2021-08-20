#!/usr/bin/env python3
import base64
import gzip
import pathlib
from typing import Iterable

from unicodedata_reader import *


class UnicodeDataCompressor(object):
    def __init__(self):
        self._value_indices = {}

    def _value_index(self, value: str) -> int:
        return self._value_indices.setdefault(value, len(self._value_indices))

    @property
    def _value_bits(self) -> int:
        value = len(self._value_indices)
        bits = 0
        while value:
            bits += 1
            value >>= 1
        return bits

    @staticmethod
    def _to_bytes(value: int) -> bytearray:
        bytes = bytearray()
        while value >= 0x80:
            bytes.append(value & 0x7F)
            value >>= 7
        bytes.append(value)
        bytes.reverse()
        for i in range(0, len(bytes) - 1):
            bytes[i] |= 0x80
        return bytes

    def compress(self, entries: UnicodeDataEntries) -> bytearray:
        # Add all values to `_value_indices` to compute the final `value_bits`.
        entry_value_list = ((entry, self._value_index(entry.value))
                            for entry in entries)
        entry_value_list = tuple(entry_value_list)
        value_bits = self._value_bits

        bytes = bytearray()
        for entry, value in entry_value_list:
            assert value < 64
            assert entry.count > 0
            combined = ((entry.count - 1) << value_bits) | value
            print(f'{entry.min:04X} {entry.value}={value}'
                  f': {entry.count} -> {combined:X}')
            bytes.extend(self._to_bytes(combined))
        return bytes

    def write_code(self, name: str, base64bytes: bytes):
        this_dir = pathlib.Path(__file__).resolve().parent
        js_dir = this_dir.parent / 'js'
        text = (js_dir / 'template.js').read_text()
        text = text.replace('FUNC_NAME', name)
        text = text.replace('BASE64', base64bytes.decode('ascii'))
        text = text.replace('VALUE_BITS', str(self._value_bits))
        output = js_dir / f'{name}.js'
        output.write_text(text)


def main():
    lb = UnicodeDataReader.default.line_break()
    lb.normalize()
    compressor = UnicodeDataCompressor()
    bytes = compressor.compress(lb)
    base64bytes = base64.b64encode(bytes)
    print(len(compressor._value_indices), compressor._value_bits, len(bytes),
          len(gzip.compress(bytes)), len(base64bytes))

    compressor.write_code('u_line_break', base64bytes)


if __name__ == '__main__':
    main()
