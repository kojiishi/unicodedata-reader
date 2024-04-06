import pytest

import unicodedata_reader as ur


def test_set_add_remove():
    s = ur.Set()
    s.add(1)
    s.add(3)
    s.add(5)
    assert 1 in s
    assert 3 in s
    assert 5 in s
    s.remove(3)
    assert 3 not in s
    s.remove(3)


def test_set_iter():
    s = ur.Set()
    s.add(1)
    s.add(5)
    assert list(s) == [1, 5]


def test_set_general_category():
    reader = ur.UnicodeDataReader()
    l = ur.Set.general_category('L', reader)
    lu = ur.Set.general_category('Lu', reader)
    assert 0x0041 in l
    assert 0x0041 in lu
    assert 0x0061 in l
    assert 0x0061 not in lu


def test_set_script_extensions():
    reader = ur.UnicodeDataReader()
    kana = ur.Set.script_extensions('Kana', reader)
    assert 0x20 not in kana
    assert 0x3031 in kana
