from unicodedata_reader import *


# This function tests reading property values using the actual data.
# Please see `entry_test.py` for tests using test data.
def test_line_break():
    lb = UnicodeDataReader.default.line_break()

    # Some entries to test from:
    # https://www.unicode.org/Public/UNIDATA/LineBreak.txt
    expects = {
        0x22: 'QU',
        0x39: 'NU',
        0x3A: 'IS',
        0x3B: 'IS',
        0x3C: 'AL',
    }

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
        assert dict[code] == value_expected

    # Map values to integer values, when doing so is useful, or when using the
    # same value as JavaScript API.
    # The `UnicodeDataCompressor` uses the integer values.
    lb.map_values_to_int()
    for code, value_expected in expects.items():
        value = lb.value(code)
        assert isinstance(value, int)
        assert lb.value_list[value] == value_expected
