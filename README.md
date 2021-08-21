[![PyPI](https://img.shields.io/pypi/v/unicodedata-reader.svg)](https://pypi.org/project/unicodedata-reader/)

# unicodedata-reader

This package reads and parses the [Unicode Character Database] files
at <https://www.unicode.org/Public/UNIDATA/>.

Many of them are already in the [unicodedata] module,
or in other 3rd party modules.
When the desired data is not in any existing modules,
this package can read the original data files.

[Unicode Character Database]: https://unicode.org/reports/tr44/
[unicodedata]: https://docs.python.org/3/library/unicodedata.html

## Install

```sh
pip install unicodedata-reader
```

## Python Usages

```python
from unicodedata_reader import UnicodeDataReader

lb = UnicodeDataReader.default.line_break()
print(lb.value(0x41))
```
The above example prints `AL`.
Please also see [line_break_test.py] for more usages.

[line_break_test.py]: https://github.com/kojiishi/unicodedata-reader/blob/main/tests/line_break_test.py

## JavaScript

The [`UnicodeDataCompressor` class] in this package
can generate JavaScript functions that can read the property values
of the [Unicode Character Database] in the browsers.

Please see [u_line_break.js] for an example of the generated functions
and [u_line_break.html] for an example usage.

[`UnicodeDataCompressor` class]: https://github.com/kojiishi/unicodedata-reader/blob/main/unicodedata_reader/compressor.py
[u_line_break.html]: https://github.com/kojiishi/unicodedata-reader/blob/main/js/u_line_break.html
[u_line_break.js]: https://github.com/kojiishi/unicodedata-reader/blob/main/js/u_line_break.js
