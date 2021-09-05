[![CI](https://github.com/kojiishi/unicodedata-reader/actions/workflows/ci.yml/badge.svg)](https://github.com/kojiishi/unicodedata-reader/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/unicodedata-reader.svg)](https://pypi.org/project/unicodedata-reader/)
[![Dependencies](https://badgen.net/github/dependabot/kojiishi/unicodedata-reader)](https://github.com/kojiishi/unicodedata-reader/network/updates)


# unicodedata-reader

This package reads and parses the [Unicode Character Database] files.

Many of them are available in the [unicodedata] module,
or in other 3rd party modules.
When the desired data is not in any existing modules,
such as the [Line_Break property] or the [Vertical_Orientation property],
this package can read the data files
at <https://www.unicode.org/Public/UNIDATA/>.

This package can also generate JavaScript functions
that can read the property values of the [Unicode Character Database]
in browsers.
Please see the [JavaScript] section below.

[General_Category property]: http://unicode.org/reports/tr44/#General_Category
[Line_Break property]: http://unicode.org/reports/tr44/#Line_Break
[Unicode Character Database]: https://unicode.org/reports/tr44/
[unicodedata]: https://docs.python.org/3/library/unicodedata.html
[Vertical_Orientation property]: http://unicode.org/reports/tr44/#Vertical_Orientation

## Install

```sh
pip install unicodedata-reader
```
If you want to clone and install using [poetry]:
```sh
git clone https://github.com/kojiishi/unicodedata-reader
cd unicodedata-reader
poetry install
poetry shell
```

[poetry]: https://github.com/python-poetry/poetry


## Python

```python
import unicodedata_reader

reader = unicodedata_reader.UnicodeDataReader.default
lb = reader.line_break()
print(lb.value(0x41))
```
The example above prints `AL`,
the [Line_Break property] value for U+0041.
Please also see [line_break_test.py] for more usages.

[line_break_test.py]: https://github.com/kojiishi/unicodedata-reader/blob/main/tests/line_break_test.py

## JavaScript
[JavaScript]: #javascript

The [`UnicodeDataCompressor` class] in this package
can generate JavaScript functions that can read the property values
of the [Unicode Character Database] in browsers.

Following examples are available in the "`js`" directory:
* [GeneralCategory.js] is a generated JavaScript file
  for the Unicode [General_Category property].
* [LineBreak.js] is a generated JavaScript file
  for the Unicode [Line_Break property].
* [LineBreak.html] for an example usage of [LineBreak.js].

The following command generates a JavaScript file for the [Line_Break property]
using `js/template.js` as the template file:
```sh
unicodedata-reader lb -t js/template.js
```

[`UnicodeDataCompressor` class]: https://github.com/kojiishi/unicodedata-reader/blob/main/unicodedata_reader/compressor.py
[GeneralCategory.js]: https://github.com/kojiishi/unicodedata-reader/blob/main/js/GeneralCategory.js
[LineBreak.html]: https://github.com/kojiishi/unicodedata-reader/blob/main/js/LineBreak.html
[LineBreak.js]: https://github.com/kojiishi/unicodedata-reader/blob/main/js/LineBreak.js
