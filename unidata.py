import re
import unicodedata
import urllib.request

class Loader(object):
  def loadBidiBrackets(self):
    def parseBidiBracketsValue(value):
      columns = re.split(r';\s*', value)
      assert len(columns) == 2
      return {"type": columns[1], "pair": int(columns[0], 16)}
    return self.dictFromUrl('BidiBrackets.txt', parseBidiBracketsValue)

  def loadScripts(self):
    return self.dictFromUrl('Scripts.txt')

  def loadScriptExtensions(self):
    return self.dictFromUrl('ScriptExtensions.txt', lambda v: v.split())

  def dictFromUrl(self, url, converter=None):
    lines = self.linesFromUrl(url)
    return Loader.dictFromLines(lines, converter)

  def linesFromUrl(self, name):
    url = 'https://www.unicode.org/Public/UNIDATA/' + name
    with urllib.request.urlopen(url) as response:
      body = response.read().decode('utf-8')
    return body.splitlines()

  @staticmethod
  def dictFromLines(lines, converter=None):
    dict = {}
    for line in lines:
      line = re.sub(r'\s*#.*', '', line)
      if not line:
        continue
      columns = re.split(r';\s*', line, 1)
      assert len(columns) == 2
      code, value = columns
      if converter:
        value = converter(value)
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

class UniData(object):
  def __init__(self):
    loader = Loader()
    self.bidiBrackets = loader.loadBidiBrackets()
    self.scripts = loader.loadScripts()
    self.scriptExtensions = loader.loadScriptExtensions()

  def row(self, code):
    return [
      UniData.hex(code),
      self.bidiBrackets[code]["type"],
      unicodedata.east_asian_width(chr(code)),
      self.scripts.get(code),
      str(self.scriptExtensions.get(code, [])),
    ]

  @staticmethod
  def hex(value):
    hexstr = hex(value)[2:].upper()
    return ('000' + hexstr)[-4:]

udata = UniData()
codes = udata.bidiBrackets.keys()
for code in codes:
  row = udata.row(code)
  print(f'{" ".join(row)} # {unicodedata.name(chr(code))}')
