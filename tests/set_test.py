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


def test_set_ior():
    s = ur.Set()
    s.add(1)
    s1 = ur.Set()
    s1.add(5)
    s |= s1
    assert list(s) == [1, 5]


def test_set_east_asian_width():
    f = ur.Set.east_asian_width('F')
    h = ur.Set.east_asian_width('H')
    assert 0x0041 not in f
    assert 0x0041 not in h
    assert 0xFF01 in f
    assert 0xFF01 not in h
    assert 0xFF61 not in f
    assert 0xFF61 in h

    f_or_h = ur.Set.east_asian_width('F', 'H')
    assert 0x0041 not in f_or_h
    assert 0xFF01 in f_or_h
    assert 0xFF61 in f_or_h


def test_set_general_category():
    l = ur.Set.general_category('L')
    lu = ur.Set.general_category('Lu')
    assert 0x0041 in l
    assert 0x0041 in lu
    assert 0x0061 in l
    assert 0x0061 not in lu

    lu_or_n = ur.Set.general_category('Lu', 'N')
    assert 0x002F not in lu_or_n
    assert 0x0030 in lu_or_n
    assert 0x0041 in lu_or_n
    assert 0x0061 not in lu_or_n


def test_set_scripts():
    han = ur.Set.scripts('Han')
    # https://github.com/unicode-org/unicodetools/issues/770#issuecomment-2041110463
    assert 0x41 not in han
    assert 0x2B739 in han  # Added in Unicode 15.0
    assert 0x323AF in han  # Added in Unicode 15.0
    assert 0x31350 in han  # Added in Unicode 15.0
    assert 0x2EBF0 in han  # Added in Unicode 15.1
    assert 0x2EE5D in han  # Added in Unicode 15.1

    hira = ur.Set.scripts('Hiragana')
    assert 0x3041 in hira
    assert 0x30A1 not in hira

    hira_or_kana = ur.Set.scripts('Hiragana', 'Katakana')
    assert 0x41 not in hira_or_kana
    assert 0x3041 in hira_or_kana
    assert 0x30A1 in hira_or_kana


def test_set_script_extensions():
    kana = ur.Set.script_extensions('Kana')
    hira = ur.Set.script_extensions('Hira')
    assert 0x20 not in kana
    assert 0x20 not in hira
    assert 0x3031 in kana
    assert 0x3031 in hira
    assert 0x3041 not in kana
    assert 0x3041 not in hira

    han_or_deva = ur.Set.script_extensions('Hani', 'Deva')
    assert 0x20 not in han_or_deva
    assert 0x1CD6 in han_or_deva
    assert 0x1CF7 not in han_or_deva
    assert 0x3002 in han_or_deva
