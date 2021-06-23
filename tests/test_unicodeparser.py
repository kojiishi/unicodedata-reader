from unicodedata_parser import UnicodeDataParser


def test_hex():
    def hex(value):
        return UnicodeDataParser.hex(value)

    assert hex(1) == '0001'
    assert hex(0xfeff) == 'FEFF'
    assert hex(0x12345) == '12345'
