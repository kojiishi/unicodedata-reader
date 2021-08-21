#!/usr/bin/env python3
import argparse
import base64
import logging
import pathlib
import sys

from unicodedata_reader import *

_logger = logging.getLogger('UnicodeDataCompressor')


class UnicodeDataCompressor(object):
    @staticmethod
    def _bitsize(value: int) -> int:
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
        value_bits = self._bitsize(len(entries.value_list))
        bytes = bytearray()
        for entry in entries:
            assert isinstance(entry.value, int)
            assert entry.value < (1 << value_bits)
            assert entry.count > 0
            combined = ((entry.count - 1) << value_bits) | entry.value
            _logger.debug('%04X %s=%d: %d -> %X', entry.min,
                          entries.value_list[entry.value], entry.value,
                          entry.count, combined)
            bytes.extend(self._to_bytes(combined))
        return bytes

    def write_javascript(self, name: str, entries: UnicodeDataEntries):
        bytes = self.compress(entries)
        base64bytes = base64.b64encode(bytes)
        value_list = entries.value_list
        value_bits = self._bitsize(len(value_list))
        _logger.info('Bytes=%d, Base64=%d, #values=%d (%d bits)', len(bytes),
                     len(base64bytes), len(value_list), value_bits)

        this_dir = pathlib.Path(__file__).resolve().parent
        js_dir = this_dir.parent / 'js'
        text = (js_dir / 'template.js').read_text()
        text = text.replace('FUNC_NAME', name)
        text = text.replace('BASE64', base64bytes.decode('ascii'))
        text = text.replace('VALUE_BITS', str(value_bits))
        output = js_dir / f'{name}.js'
        output.write_text(text)


def _init_logging(verbose: int):
    if verbose <= 1:
        handler = logging.StreamHandler(sys.stdout)
        _logger.addHandler(handler)
        _logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        return
    logging.basicConfig(level=logging.DEBUG)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v',
                        '--verbose',
                        help='increase output verbosity',
                        action='count',
                        default=0)
    args = parser.parse_args()
    _init_logging(args.verbose)

    entries = UnicodeDataReader.default.line_break()
    entries.normalize()
    entries.map_values_to_int()
    compressor = UnicodeDataCompressor()
    compressor.write_javascript('u_line_break', entries)


if __name__ == '__main__':
    main()
