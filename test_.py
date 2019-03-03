from collections import OrderedDict
from copy import deepcopy
from tempfile import NamedTemporaryFile

import numpy as np

from binary_fractions import BinaryFraction
from language_models import add_eof_to_freq_dist, get_frequency_distribution


def test_BinaryFraction__init__():
    test_float = 1 / 4 + 1 / 8
    test_bin_frac = BinaryFraction(test_float)
    assert test_bin_frac.i == int("0b011", 2)
    assert test_bin_frac.msb == 3

    test_float = 1 / 2 + 1 / 64 + 1 / 1024
    test_bin_frac = BinaryFraction(test_float)
    assert test_bin_frac.i == int("0b1000010001", 2)
    assert test_bin_frac.msb == 10

    test_float = 0.0
    test_bin_frac = BinaryFraction(test_float)
    assert test_bin_frac.i == int("0b0", 2)
    assert test_bin_frac.msb == 0

    test_float = 1.0
    test_bin_frac = BinaryFraction(test_float)
    assert test_bin_frac.i == int("0b1", 2)
    assert test_bin_frac.msb == 0


def test_BinaryFraction_to_float():
    expected = 1 / 4 + 1 / 8
    test_bin_frac = BinaryFraction(expected)
    assert np.isclose(test_bin_frac.to_float(), expected)

    expected = 1 / 2 + 1 / 64 + 1 / 1024
    test_bin_frac = BinaryFraction(expected)
    assert np.isclose(test_bin_frac.to_float(), expected)

    expected = 0.0
    test_bin_frac = BinaryFraction(expected)
    assert np.isclose(test_bin_frac.to_float(), expected)

    expected = 1.0
    test_bin_frac = BinaryFraction(expected)
    assert np.isclose(test_bin_frac.to_float(), expected)

    expected = 0.23874
    test_bin_frac = BinaryFraction(expected)
    assert np.isclose(test_bin_frac.to_float(), expected)


def test_BinaryFraction__eq__():
    x = BinaryFraction(0.123)
    y = BinaryFraction(0.123)
    z = BinaryFraction(0.234)

    assert x == y
    assert x != z
    assert x == 0.123
    assert x != 0.234
    assert x != 10


def test_BinaryFraction_get_bin_string():
    test_float = 1.0
    test_bin_frac = BinaryFraction(test_float)
    expected = "1"
    assert test_bin_frac.get_bin_string() == expected

    test_float = 0.0
    test_bin_frac = BinaryFraction(test_float)
    expected = "0"
    assert test_bin_frac.get_bin_string() == expected

    test_float = 1 / 2
    test_bin_frac = BinaryFraction(test_float)
    expected = "01"
    assert test_bin_frac.get_bin_string() == expected

    test_float = 1 / 4 + 1 / 16
    test_bin_frac = BinaryFraction(test_float)
    expected = "00101"
    assert test_bin_frac.get_bin_string() == expected


def test_BinaryFraction_get_msb():
    test_bin_frac = BinaryFraction(1.0)
    expected = "1"
    assert test_bin_frac.get_msb() == expected

    test_bin_frac = BinaryFraction(0.0)
    expected = "0"
    assert test_bin_frac.get_msb() == expected

    test_float = 1 / 2
    test_bin_frac = BinaryFraction(test_float)
    expected = "1"
    assert test_bin_frac.get_msb() == expected

    test_float = 1 / 4 + 1 / 8
    test_bin_frac = BinaryFraction(test_float)
    expected = "0"
    assert test_bin_frac.get_msb() == expected

    test_float = 1 / 2 + 1 / 64 + 1 / 1024
    test_bin_frac = BinaryFraction(test_float)
    expected = "1"
    assert test_bin_frac.get_msb() == expected


def test_BinaryFraction_msb_check():
    x = BinaryFraction(1.0)
    y = BinaryFraction(0.0)
    z = BinaryFraction(1 / 2)
    a = BinaryFraction(1 / 4)

    assert x.msb_check(z)
    assert y.msb_check(a)

    assert not x.msb_check(a)
    assert not y.msb_check(z)


def test_BinaryFraction_pop_msb():
    test_float = 1 / 2
    test_bin_frac = BinaryFraction(test_float)
    expected_msb = "1"
    expected_new_bin_frac = BinaryFraction(0.0)
    popped_msb, test_bin_frac = test_bin_frac.pop_msb(False)
    assert popped_msb == expected_msb
    assert test_bin_frac == expected_new_bin_frac

    test_float = 1 / 4
    test_bin_frac = BinaryFraction(test_float)
    expected_msb = "0"
    expected_new_bin_frac = BinaryFraction(1 / 2)
    popped_msb, test_bin_frac = test_bin_frac.pop_msb(False)
    assert popped_msb == expected_msb
    assert test_bin_frac == expected_new_bin_frac

    test_float = 1 / 4
    test_bin_frac = BinaryFraction(test_float)
    expected_msb = "0"
    expected_new_bin_frac = BinaryFraction(1 / 2 + 1 / 4)
    popped_msb, test_bin_frac = test_bin_frac.pop_msb(True)
    assert popped_msb == expected_msb
    assert test_bin_frac == expected_new_bin_frac

    test_float = 1 / 2 + 1 / 4 + 1 / 16
    test_bin_frac = BinaryFraction(test_float)
    expected_msb = "1"
    expected_new_bin_frac = BinaryFraction(1 / 2 + 1 / 8 + 1 / 16)
    popped_msb, test_bin_frac = test_bin_frac.pop_msb(True)
    assert popped_msb == expected_msb
    assert test_bin_frac == expected_new_bin_frac


def test_BinaryFraction_shorted_bin_in_interval():
    upper_float = BinaryFraction.bin_string_to_float("01101")
    lower_float = BinaryFraction.bin_string_to_float("011")
    u = BinaryFraction(upper_float)
    l = BinaryFraction(lower_float)
    expected = "11001"
    assert BinaryFraction.shortest_bin_in_interval(l, u) == expected

    upper_float = BinaryFraction.bin_string_to_float("01101")
    lower_float = BinaryFraction.bin_string_to_float("0110001")
    u = BinaryFraction(upper_float)
    l = BinaryFraction(lower_float)
    expected = "11001"
    assert BinaryFraction.shortest_bin_in_interval(l, u) == expected

    upper_float = BinaryFraction.bin_string_to_float("1")
    lower_float = BinaryFraction.bin_string_to_float("001")
    u = BinaryFraction(upper_float)
    l = BinaryFraction(lower_float)
    expected = "1"
    assert BinaryFraction.shortest_bin_in_interval(l, u) == expected

    upper_float = BinaryFraction.bin_string_to_float("011")
    lower_float = BinaryFraction.bin_string_to_float("0")
    u = BinaryFraction(upper_float)
    l = BinaryFraction(lower_float)
    expected = "01"
    assert BinaryFraction.shortest_bin_in_interval(l, u) == expected


def test_get_frequency_distribution():
    sample_text = "∂eath metal reigns supreme!\n"
    n_symbols = len(sample_text)

    with NamedTemporaryFile(mode="w+", buffering=1) as tmp:
        tmp.write(sample_text)

        freq_dist = get_frequency_distribution(tmp.name)

    expected = OrderedDict(
        {
            "∂": 1 / n_symbols,
            "e": 5 / n_symbols,
            "a": 2 / n_symbols,
            "t": 2 / n_symbols,
            "h": 1 / n_symbols,
            " ": 3 / n_symbols,
            "m": 2 / n_symbols,
            "l": 1 / n_symbols,
            "r": 2 / n_symbols,
            "i": 1 / n_symbols,
            "g": 1 / n_symbols,
            "n": 1 / n_symbols,
            "s": 2 / n_symbols,
            "u": 1 / n_symbols,
            "p": 1 / n_symbols,
            "!": 1 / n_symbols,
            "\n": 1 / n_symbols,
        }
    )

    assert freq_dist == expected

    assert np.isclose(1, sum(freq_dist.values()))


def test_add_eof_to_freq_dist():
    test_string = "aaab"

    with NamedTemporaryFile(mode="w+") as tmp:
        tmp.write(test_string)
        tmp.flush()

        freq_dist = get_frequency_distribution(tmp.name)

    updated = add_eof_to_freq_dist(deepcopy(freq_dist))
    assert np.isclose(sum(updated.values()), 1.0)

    original_sorted_items = sorted(freq_dist.items(), key=lambda x: x[1])
    original_sorted_keys = [x[0] for x in original_sorted_items]

    new_sorted_items = sorted(updated.items(), key=lambda x: x[1])
    new_sorted_keys = [x[0] for x in new_sorted_items]

    assert new_sorted_keys[0] == ""

    assert new_sorted_keys[1:] == original_sorted_keys
