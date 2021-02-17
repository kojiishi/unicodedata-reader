#!/usr/bin/env python3
import re
import unicodedata
import urllib.request

class UnicodeDataLoader(object):
  """Load [Unicode character database] data files.

  This class provides data in the [Unicode character database], similar to the
  `unicodedata`, but with more coverage and is up-to-date by loading the
  original data files from <https://www.unicode.org/Public/UNIDATA/>.
  
  [Unicode character database]: https://unicode.org/reports/tr44/
  """

  def load_bidi_brackets(self):
    def convert_bidi_brackets_value(value):
      assert len(value) == 2
      return {"type": value[1], "pair": int(value[0], 16)}
    return self.load('BidiBrackets.txt', convert_bidi_brackets_value)

  def load_blocks(self):
    return self.load('Blocks.txt')

  def load_scripts(self):
    return self.load('Scripts.txt')

  def load_script_extensions(self):
    return self.load('ScriptExtensions.txt', lambda v: v.split())

  def load(self, name, converter=None):
    lines = self.lines_from_name(name)
    return self.dict_from_lines(lines, converter)

  def lines_from_name(self, name):
    url = 'https://www.unicode.org/Public/UNIDATA/' + name
    with urllib.request.urlopen(url) as response:
      body = response.read().decode('utf-8')
    return body.splitlines()

  @staticmethod
  def dict_from_lines(lines, converter=None):
    dict = {}
    for line in lines:
      # Skip comments.
      line = re.sub(r'\s*#.*', '', line)
      if not line:
        continue
      # Data columns are separated by ';'.
      columns = re.split(r'\s*;\s*', line)
      assert len(columns) >= 2
      value = columns[1] if len(columns) == 2 else columns[1:]
      if converter:
        value = converter(value)
      # `columns[0]` is a code point or a range of code points.
      code = columns[0]
      codeRange = code.split('..')
      if len(codeRange) == 1:
        dict[int(code, 16)] = value
      elif len(codeRange) == 2:
        min = int(codeRange[0], 16)
        max = int(codeRange[1], 16)
        for code in range(min, max + 1):
          dict[code] = value
      else:
        assert False
    return dict

  @staticmethod
  def hex(value):
    hexstr = hex(value)[2:].upper()
    return ('000' + hexstr)[-4:]

  @staticmethod
  def dump_bidi_brackets():
    parser = UnicodeDataLoader()
    blocks = parser.load_blocks()
    bidi_brackets = parser.load_bidi_brackets()
    scripts = parser.load_scripts()
    script_extensions = parser.load_script_extensions()
    last_block = None
    for code in bidi_brackets.keys():
      block = blocks[code]
      if block != last_block:
        print(f'# {block}')
        last_block = block
      row = [
        UnicodeDataLoader.hex(code),
        bidi_brackets[code]["type"],
        unicodedata.east_asian_width(chr(code)),
        scripts.get(code),
        str(script_extensions.get(code, [])),
      ]
      print(f'{" ".join(row)} # {unicodedata.name(chr(code))}')

if __name__ == '__main__':
  UnicodeDataLoader.dump_bidi_brackets()
