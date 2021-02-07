#!/usr/bin/env python3
import re
import unicodedata
import urllib.request

class UnicodeDataParser(object):

  def parse_blocks(self):
    return self.dict_from_name('Blocks.txt')

  def parse_bidi_brackets(self):
    def parse_bidi_brackets_value(value):
      assert len(value) == 2
      return {"type": value[1], "pair": int(value[0], 16)}
    return self.dict_from_name('BidiBrackets.txt', parse_bidi_brackets_value)

  def parse_scripts(self):
    return self.dict_from_name('Scripts.txt')

  def parse_script_extensions(self):
    return self.dict_from_name('ScriptExtensions.txt', lambda v: v.split())

  def dict_from_name(self, name, converter=None):
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
      line = re.sub(r'\s*#.*', '', line)
      if not line:
        continue
      columns = re.split(r';\s*', line)
      assert len(columns) >= 2
      value = columns[1] if len(columns) == 2 else columns[1:]
      if converter:
        value = converter(value)
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
    parser = UnicodeDataParser()
    blocks = parser.parse_blocks()
    bidi_brackets = parser.parse_bidi_brackets()
    scripts = parser.parse_scripts()
    script_extensions = parser.parse_script_extensions()
    last_block = None
    for code in bidi_brackets.keys():
      block = blocks[code]
      if block != last_block:
        print(f'# {block}')
        last_block = block
      row = [
        UnicodeDataParser.hex(code),
        bidi_brackets[code]["type"],
        unicodedata.east_asian_width(chr(code)),
        scripts.get(code),
        str(script_extensions.get(code, [])),
      ]
      print(f'{" ".join(row)} # {unicodedata.name(chr(code))}')

if __name__ == '__main__':
  UnicodeDataParser.dump_bidi_brackets()
