#!/usr/bin/env python3
import argparse
import base64
import logging
import pathlib
import string
import sys
from typing import Optional

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

    def __init__(self, entries: UnicodeDataEntries):
        self._entries = entries

    @property
    def _bitsize(self) -> int:
        values_for_int = self._entries.values_for_int()
        assert values_for_int
        return self._bitsize_for(len(values_for_int) - 1)

    @staticmethod
    def _bitsize_for(value: int) -> int:
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

    def compress(self) -> bytearray:
        entries = self._entries
        assert entries._is_contiguous()
        value_bits = self._bitsize
        bytes = bytearray()
        for entry in entries:
            assert isinstance(entry.value, int)
            assert entry.value < (1 << value_bits)
            assert entry.count > 0
            combined = ((entry.count - 1) << value_bits) | entry.value
            _logger.debug('%04X %s=%d: %d -> %X', entry.min,
                          entries.values_for_int()[entry.value], entry.value,
                          entry.count, combined)
            bytes.extend(self._to_bytes(combined))
        return bytes

    def substitute_template(self,
                            template: pathlib.Path,
                            output: Optional[pathlib.Path] = None,
                            name: Optional[str] = None) -> str:
        entries = self._entries
        bytes = self.compress()
        base64bytes = base64.b64encode(bytes)
        values_for_int = entries.values_for_int()
        value_bits = self._bitsize
        name = name or entries.name
        assert name
        _logger.info('%s: Bytes=%d, Base64=%d, #values=%d (%d bits)', name,
                     len(bytes), len(base64bytes), len(values_for_int),
                     value_bits)
        mapping = {
            'NAME': name,
            'BASE64BYTES': base64bytes.decode('ascii'),
            'VALUE_BITS': str(value_bits),
            'VALUE_MASK': str((1 << value_bits) - 1),
            'VALUE_LIST': ','.join(f'"{v}"' for v in values_for_int),
        }

        text = template.read_text()
        text = string.Template(text)
        text = text.substitute(mapping)

        if output:
            if str(output) == '-':
                sys.stdout.write(text)
            else:
                if output.is_dir():
                    output = output / f'{name}{template.suffix}'
                output.write_text(text)
                _logger.info('Saved to %s', output)

        return text


def main():
    this_dir = pathlib.Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', default='LineBreak')
    parser.add_argument('--template',
                        type=pathlib.Path,
                        default=this_dir.parent / 'js' / 'template.js')
    parser.add_argument('-o', '--output', type=pathlib.Path)
    parser.add_argument('-v',
                        '--verbose',
                        help='increase output verbosity',
                        action='count',
                        default=0)
    args = parser.parse_args()
    _init_logging(args.verbose)

    entries = UnicodeDataReader.default.line_break()
    entries.fill_missing_values()
    entries.map_values_to_int()

    template = args.template
    output = args.output
    compressor = UnicodeDataCompressor(entries)
    compressor.substitute_template(
        template, output=output if output else template.parent, name=args.name)


if __name__ == '__main__':
    main()
