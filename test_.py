from collections import OrderedDict
from copy import deepcopy
from tempfile import NamedTemporaryFile

import numpy as np

from arithmetic_coding import add_eof_to_freq_dist
from binary_fractions import BinaryFraction, bin_frac_to_dec, dec_to_bin_frac
from language_models import get_frequency_distribution


def test_bin_frac_to_dec():

    test_bin_frac = BinaryFraction(int("0b011", 2), 2)

    expected = 1 / 4 + 1 / 8

    assert bin_frac_to_dec(test_bin_frac) == expected

    test_bin_frac = BinaryFraction(int("0b1000010001", 2), 9)

    expected = 1 / 2 + 1 / 64 + 1 / 1024

    assert bin_frac_to_dec(test_bin_frac) == expected


def test_dec_to_bin_frac():

    test_float = 1 / 2 + 1 / 64 + 1 / 1024

    expected = BinaryFraction(int("0b1000010001", 2), 9)

    assert dec_to_bin_frac(test_float) == expected


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
    assert np.isclose(sum(updated.values()), 1.)

    original_sorted_items = sorted(freq_dist.items(), key=lambda x: x[1])
    original_sorted_keys = [x[0] for x in original_sorted_items]

    new_sorted_items = sorted(updated.items(), key=lambda x: x[1])
    new_sorted_keys = [x[0] for x in new_sorted_items]

    assert new_sorted_keys[0] == ''

    assert new_sorted_keys[1:] == original_sorted_keys
