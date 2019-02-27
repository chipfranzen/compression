"""
Language models to use as predictive distributions for text encoding.
"""
from collections import Counter


def get_frequency_distribution(filepath):
    with open(filepath, "r") as f:

        freq_dict = dict(Counter(f.read()))

    n_symbols = sum(freq_dict.values())
    freq_dist = {k: v / n_symbols for k, v in freq_dict.items()}

    return freq_dist
