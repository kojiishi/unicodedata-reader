#!/usr/bin/env python3
import argparse
import base64
import logging
import pathlib
import sys

from unicodedata_reader import *

_logger = logging.getLogger('UnicodeDataCompressor')


def _init_logging(verbose: int):
    if verbose <= 1:
        handler = logging.StreamHandler(sys.stdout)
        _logger.addHandler(handler)
        _logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        return
    logging.basicConfig(level=logging.DEBUG)


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

    def replace_variables(self, name: str, entries: UnicodeDataEntries,
                          text: str) -> str:
        bytes = self.compress(entries)
        base64bytes = base64.b64encode(bytes)
        value_list = entries.value_list
        value_bits = self._bitsize(len(value_list))

        text = text.replace('FUNC_NAME', name)
        text = text.replace('BASE64', base64bytes.decode('ascii'))
        text = text.replace('VALUE_BITS', str(value_bits))

        _logger.info('%s: Bytes=%d, Base64=%d, #values=%d (%d bits)', name,
                     len(bytes), len(base64bytes), len(value_list), value_bits)
        return text


def main():
    this_dir = pathlib.Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', default='u_line_break')
    parser.add_argument('--template',
                        type=pathlib.Path,
                        default=this_dir.parent / 'js' / 'template.js')
    parser.add_argument('-o', '--output')
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

    name = args.name
    template = args.template
    text = template.read_text()
    compressor = UnicodeDataCompressor()
    text = compressor.replace_variables(name, entries, text)

    output = args.output
    if output == '-':
        sys.stdout.write(text)
    else:
        if output:
            output = pathlib.Path(output)
        else:
            output = template.parent
        if output.is_dir():
            output = output / f'{name}{template.suffix}'
        output.write_text(text)
        _logger.info('Saved to %s', output)


if __name__ == '__main__':
    main()
