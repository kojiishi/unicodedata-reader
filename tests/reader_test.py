from unicodedata_reader import *


def test_hex():
    assert u_hex(1) == '0001'
    assert u_hex(0xfeff) == 'FEFF'
    assert u_hex(0x12345) == '12345'


def test_east_asian_width():
    entries = UnicodeDataReader().east_asian_width()
    assert entries.value(0x20) == 'Na'
    assert entries.value(0xB7) == 'A'
    assert entries.value(0x3000) == 'F'
    assert entries.value(0x3001) == 'W'
    assert entries.value(0x2A700) == 'W'


def test_name():
    entries = UnicodeDataReader().name()
    assert entries.value(0x20) == 'SPACE'
    assert entries.value(0xE0100) == 'VARIATION SELECTOR-17'


def test_context():
    original_default = UnicodeDataReader.default
    with UnicodeDataReader.Context(UnicodeDataReader()) as in_context:
        assert original_default != in_context
        assert UnicodeDataReader.default == in_context
    assert UnicodeDataReader.default == original_default
