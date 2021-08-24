from unicodedata_reader import *


def _to_unicodes(text):
    return tuple(to_unicodes(text))


def test_to_unicodes():
    assert _to_unicodes('1234') == (0x1234, )
    assert _to_unicodes('12FE') == (0x12FE, )
    assert _to_unicodes('ABCD') == (0xABCD, )

    assert _to_unicodes('12345') == (0x12345, )

    assert _to_unicodes('u0009') == (0x9, )
    assert _to_unicodes('u1234') == (0x1234, )
    assert _to_unicodes('U+1234') == (0x1234, )

    assert _to_unicodes('1234 5678') == (0x1234, 0x5678)
    assert _to_unicodes('1234,5678') == (0x1234, 0x5678)
    assert _to_unicodes('1234, 5678') == (0x1234, 0x5678)

    assert _to_unicodes('xy') == (ord('x'), ord('y'))


def test_to_unicodes_range():
    assert _to_unicodes('1234-1236') == (0x1234, 0x1235, 0x1236)


def test_to_unicodes_array():
    assert _to_unicodes(['1234', '5678']) == (0x1234, 0x5678)
