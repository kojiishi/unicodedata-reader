import pytest

from unicodedata_reader import *


def test_entry_eq():
    assert UnicodeDataEntry(1, 3, 'A') == UnicodeDataEntry(1, 3, 'A')
    assert UnicodeDataEntry(1, 3, 'A') != UnicodeDataEntry(1, 3, 'B')
    assert UnicodeDataEntry(1, 3, 'A') != UnicodeDataEntry(2, 3, 'A')
    assert UnicodeDataEntry(1, 3, 'A') != UnicodeDataEntry(1, 2, 'A')


def test_from_pairs():
    entries = UnicodeDataEntry.from_pairs((
        (1, 'A'),
        (2, 'A'),
        (3, 'B'),
        (4, 'B'),
        (6, 'C'),
        (8, 'C'),
        (9, 'C'),
        (11, 'C'),
    ))
    entries = tuple(entries)
    expects = (UnicodeDataEntry(1, 2, 'A'), UnicodeDataEntry(3, 4, 'B'),
               UnicodeDataEntry(6, 6, 'C'), UnicodeDataEntry(8, 9, 'C'),
               UnicodeDataEntry(11, 11, 'C'))
    assert entries == expects


def test_from_pairs_unsorted():
    entries = UnicodeDataEntry.from_pairs((
        (1, 'A'),
        (3, 'A'),
        (2, 'A'),
    ))
    with pytest.raises(AssertionError):
        entries = tuple(entries)


def test_from_pairs_none():
    entries = UnicodeDataEntry.from_pairs((
        (1, None),
        (2, 'A'),
        (3, 'A'),
        (5, None),
        (7, 'A'),
        (9, None),
    ))
    entries = tuple(entries)
    expects = (UnicodeDataEntry(1, 1, None), UnicodeDataEntry(2, 3, 'A'),
               UnicodeDataEntry(5, 5, None), UnicodeDataEntry(7, 7, 'A'),
               UnicodeDataEntry(9, 9, None))
    assert entries == expects


def test_from_values_none():
    entries = UnicodeDataEntry.from_values((None, 'A', None, 'A', None, 'B'))
    entries = tuple(entries)
    expects = (UnicodeDataEntry(1, 1, 'A'), UnicodeDataEntry(3, 3, 'A'),
               UnicodeDataEntry(5, 5, 'B'))
    assert entries == expects


def test_value():
    entries = UnicodeDataEntries(entries=(
        UnicodeDataEntry(1, 3, 'A'),
        UnicodeDataEntry(5, 6, 'B'),
    ))
    expect = (None, 'A', 'A', 'A', None, 'B', 'B')
    for code, value in enumerate(expect):
        assert entries.value(code) == value
        assert entries[code] == value

    assert entries.value(code + 1) is None

    values_for_code = tuple(entries.values_for_code())
    assert values_for_code == expect


def test_missing_directive():
    lines = [
        '# test\n',
        '# @missing: 0000..10FFFF; R\n',
        '0000..001F     ; R\n',
        '3000           ; U\n',
    ]
    entries = UnicodeDataEntries(lines=lines)
    assert entries.value(0x001F) == 'R'
    assert entries.value(0x2FFF) == 'R'
    assert entries.value(0x3000) == 'U'
    assert entries.value(0x3001) == 'R'
    assert entries._missing_entries[0] == UnicodeDataEntry(0, 0x10FFFF, 'R')


def test_missing_directive_lb():
    lines = [
        '# test\n',
        '#  - The unassigned code points in the following blocks default to "ID":\n',
        '#         CJK Unified Ideographs Extension A: U+3400..U+4DBF\n',
        '#  - The unassigned code points in the following block default to "PR":\n',
        '#         Currency Symbols:                   U+20A0..U+20CF\n',
        '# @missing: 0000..10FFFF; XX\n',
    ]
    entries = UnicodeLineBreakDataEntries(lines=lines)
    assert entries.value(0x33FF) == 'XX'
    for code in range(0x3400, 0x4DC0):
        assert entries.value(code) == 'ID'
    assert entries.value(0x4DC0) == 'XX'
    assert entries.value(0x209F) == 'XX'
    for code in range(0x20A0, 0x20D0):
        assert entries.value(code) == 'PR'
    assert entries.value(0x20D0) == 'XX'


def test_missing_directive_vo():
    lines = [
        '# test\n',
        '#         Control Pictures & OCR              U+2400..U+245F\n',
        '# @missing: 0000..10FFFF; R\n',
    ]
    entries = UnicodeVerticalOrientationDataEntries(lines=lines)
    assert entries.value(0x23FF) == 'R'
    for code in range(0x2400, 0x2460):
        assert entries.value(code) == 'U'
    assert entries.value(0x2460) == 'R'


def test_normalie_no_changes():
    entries = UnicodeDataEntries(entries=(
        UnicodeDataEntry(1, 3, 'A'),
        UnicodeDataEntry(5, 6, 'B'),
    ))
    nomalized_entries = UnicodeDataEntries(entries=entries)
    nomalized_entries.fill_missing_values()
    assert tuple(entries) == tuple(nomalized_entries)


def test_fill_missing_values():

    class TestEntries(UnicodeDataEntries):

        def missing_value(self, code: int):
            return 'B'

    entries = TestEntries(entries=(
        UnicodeDataEntry(0, 10, 'A'),
        UnicodeDataEntry(12, 20, 'B'),
    ))
    entries.fill_missing_values()
    assert len(entries) == 2
    assert entries._entries == (UnicodeDataEntry(0, 10, 'A'),
                                UnicodeDataEntry(11, 20, 'B'))


def test_range_as_str():
    entry = UnicodeDataEntry(9, 9, 'A')
    assert entry.range_as_str() == '0009'

    entry = UnicodeDataEntry(9, 11, 'A')
    assert entry.range_as_str() == '0009..000B'
    assert entry.range_as_str(lambda c: str(c)) == '9..11'
    assert entry.range_as_str(lambda c: 'XYZ') == 'XYZ'

    entry = UnicodeDataEntry(0xFFFF, 0x10001, 'A')
    assert entry.range_as_str() == 'FFFF..10001'
