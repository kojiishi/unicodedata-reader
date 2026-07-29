import sys
from pathlib import Path

import pytest

from unicodedata_reader import UnicodeDataCachedReader, UnicodeDataReader

tests_dir = Path(__file__).parent
root_dir = tests_dir.parent
sys.path.append(str(root_dir / "unicodedata_parser"))

# Avoid making too many requests to `unicode.org`.
cache_dir = tests_dir / "cache"
_reader = UnicodeDataCachedReader(cache_dir=cache_dir)
UnicodeDataReader.default = _reader


@pytest.fixture
def reader() -> UnicodeDataReader:
    return _reader
