from unicodedata_reader import *


def test_value():
    entries = UnicodeDataEntries((
        UnicodeDataEntry(1, 3, 'A'),
        UnicodeDataEntry(5, 6, 'B'),
    ))
    expect = (None, 'A', 'A', 'A', None, 'B', 'B')
    for code, value in enumerate(expect):
        assert entries.value(code) == value

    assert entries.value(code + 1) is None

    values = tuple(entries.values())
    assert values == expect


def test_normalize_fill_missing_entries_merge():
    class TestEntries(UnicodeDataEntries):
        def missing_value(self, code: int):
            return 'B'

    entries = TestEntries((
        UnicodeDataEntry(0, 10, 'A'),
        UnicodeDataEntry(12, 20, 'B'),
    ))
    entries.normalize()
    assert len(entries) == 2
    assert entries._entries == (UnicodeDataEntry(0, 10, 'A'),
                                UnicodeDataEntry(11, 20, 'B'))
