"""
Language models to use as predictive distributions for text encoding.
"""
from collections import Counter, OrderedDict

import numpy as np
from scipy.special import softmax


def add_eof_to_freq_dist(freq_dist):
    freq_dist[""] = min(freq_dist.values()) ** 2

    unnormalized_freq = np.array(list(freq_dist.values()))

    normalized_freq = softmax(unnormalized_freq)

    normalized_dist = {k: normalized_freq[i] for i, k in enumerate(freq_dist)}

    return normalized_dist


def get_frequency_distribution(filepath):
    with open(filepath, "r") as f:

        freq_dict = OrderedDict(Counter(f.read()))

    n_symbols = sum(freq_dict.values())
    freq_dist = {k: v / n_symbols for k, v in freq_dict.items()}

    return freq_dist
