from unicodedata_reader import *


def test_entry_eq():
    assert UnicodeDataEntry(1, 3, 'A') == UnicodeDataEntry(1, 3, 'A')
    assert UnicodeDataEntry(1, 3, 'A') != UnicodeDataEntry(1, 3, 'B')
    assert UnicodeDataEntry(1, 3, 'A') != UnicodeDataEntry(2, 3, 'A')
    assert UnicodeDataEntry(1, 3, 'A') != UnicodeDataEntry(1, 2, 'A')


def test_value():
    entries = UnicodeDataEntries((
        UnicodeDataEntry(1, 3, 'A'),
        UnicodeDataEntry(5, 6, 'B'),
    ))
    expect = (None, 'A', 'A', 'A', None, 'B', 'B')
    for code, value in enumerate(expect):
        assert entries.value(code) == value

    assert entries.value(code + 1) is None

    values_for_code = tuple(entries.values_for_code())
    assert values_for_code == expect


def test_normalie_no_changes():
    entries = UnicodeDataEntries((
        UnicodeDataEntry(1, 3, 'A'),
        UnicodeDataEntry(5, 6, 'B'),
    ))
    nomalized_entries = UnicodeDataEntries(entries)
    nomalized_entries.normalize()
    assert tuple(entries) == tuple(nomalized_entries)


def test_normalize_fill_missing_entries_override():
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
