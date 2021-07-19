from unicodedata_parser import *


def test_hex():
    assert u_hex(1) == '0001'
    assert u_hex(0xfeff) == 'FEFF'
    assert u_hex(0x12345) == '12345'


def test_parse_unicode_list():
    def run(text):
        return tuple(to_unicodes(text))

    assert run('1234') == (0x1234, )
    assert run('12FE') == (0x12FE, )
    assert run('ABCD') == (0xABCD, )

    assert run('u9') == (0x9, )
    assert run('u1234') == (0x1234, )
    assert run('U+1234') == (0x1234, )


    assert run('1234 5678') == (0x1234, 0x5678)
    assert run('1234,5678') == (0x1234, 0x5678)
    assert run('1234, 5678') == (0x1234, 0x5678)

    assert run('xy') == (ord('x'), ord('y'))
