from tempfile import NamedTemporaryFile

import numpy as np

from binary_fractions import bin_to_dec, dec_to_bin
from language_models import get_frequency_distribution


def test_bin_to_dec():

    test_string = "0b.011"
    assert 1 / 4 + 1 / 8 == bin_to_dec(test_string)


def test_dec_to_bin():

    test_float = 1 / 2 + 1 / 64 + 1 / 1024
    assert "0b.1000010001" == dec_to_bin(test_float)


def test_get_frequency_distribution():
    sample_text = "∂eath metal reigns supreme!\n"
    n_symbols = len(sample_text)

    with NamedTemporaryFile(mode="w+", buffering=1) as tmp:
        tmp.write(sample_text)

        freq_dist = get_frequency_distribution(tmp.name)

    expected = {
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

    assert freq_dist == expected

    assert np.isclose(1, sum(freq_dist.values()))
