import re
import urllib.request

class unidata(object):
  def __init__(self):
    pass

  @staticmethod
  def hex(value):
    hexstr = hex(value)[2:].upper()
    return ('000' + hexstr)[-4:]

  @staticmethod
  def loadBidiBrackets():
    def parseBidiBracketsValue(value):
      columns = re.split(r';\s*', value)
      assert len(columns) == 2
      return {"type": columns[1], "pair": int(columns[0], 16)}
    return unidata.dictFromUrl(
        'https://www.unicode.org/Public/UNIDATA/BidiBrackets.txt',
        parseBidiBracketsValue)

  @staticmethod
  def loadScripts():
    return unidata.dictFromUrl(
        'https://www.unicode.org/Public/UNIDATA/Scripts.txt')

  @staticmethod
  def loadScriptExtensions():
    return unidata.dictFromUrl(
        'https://www.unicode.org/Public/UNIDATA/ScriptExtensions.txt',
        lambda v: v.split())

  @staticmethod
  def dictFromUrl(url, valueConverter=None):
    return unidata.dictFromLines(unidata.linesFromUrl(url), valueConverter)

  @staticmethod
  def dictFromLines(lines, valueConverter=None):
    dict = {}
    for line in lines:
      line = re.sub(r'\s*#.*', '', line)
      if not line:
        continue
      columns = re.split(r';\s*', line, 1)
      assert len(columns) == 2
      code, value = columns
      if valueConverter:
        value = valueConverter(value)
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
  def linesFromUrl(url):
    with urllib.request.urlopen(url) as response:
      body = response.read().decode('utf-8')
    return body.splitlines()

bidiBrackets = unidata.loadBidiBrackets()
scripts = unidata.loadScripts()
scriptExtensions = unidata.loadScriptExtensions()
for code, bidiBracket in bidiBrackets.items():
  print(f'{unidata.hex(code)} {bidiBracket["type"]} {scripts.get(code)} {scriptExtensions.get(code)}')
