from unicodedata_reader import *


# This function tests reading property values using the actual data.
# Please see `entry_test.py` for tests using test data.
def test_line_break():
    # Some entries to test from:
    # https://www.unicode.org/Public/UNIDATA/LineBreak.txt
    expects = {
        0x22: 'QU',
        0x39: 'NU',
        0x3A: 'IS',
        0x3B: 'IS',
        0x3C: 'AL',
        0x378: 'XX',  # missing value.
    }

    lb = UnicodeDataReader.default.line_break()

    # `value(code)` returns the value for the code point.
    # This is the the most memory-friendly, but slower to read values than other
    # methods.
    for code, value_expected in expects.items():
        assert lb.value(code) == value_expected

    # `values()` returns a list of values in the code point order.
    # This creates an item for each Unicode code point (~1M items,) but the
    # fastest way to read values once the tuple was created.
    values = tuple(lb.values())
    for code, value_expected in expects.items():
        assert values[code] == value_expected

    # `to_dict()` creates a dict of values, keyed by code points.
    dict = lb.to_dict()
    for code, value_expected in expects.items():
        value = dict.get(code, lb.missing_value(code))
        assert value == value_expected

    # Map values to integer values.
    lb.map_values_to_int()
    for code, value_expected in expects.items():
        value = lb.value(code)
        if value == 'XX':
            # Missing values are computed that they are not mapped.
            assert value == value_expected
        else:
            assert isinstance(value, int)
            assert lb.value_list[value] == value_expected

    # Use `normalize()` to fill entries for missing values.
    lb = UnicodeDataReader.default.line_break()
    lb.normalize()
    lb.map_values_to_int()
    for code, value_expected in expects.items():
        value = lb.value(code)
        assert isinstance(value, int)
        assert lb.value_list[value] == value_expected
