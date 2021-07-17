from unicodedata_parser import *


def test_hex():
    assert u_hex(1) == '0001'
    assert u_hex(0xfeff) == 'FEFF'
    assert u_hex(0x12345) == '12345'
