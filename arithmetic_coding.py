"""
The arithmetic coding compression algorithm.
"""
import numpy as np

from language_models import get_frequency_distribution
from scipy.special import softmax


def add_eof_to_freq_dist(freq_dist):
    freq_dist[""] = min(freq_dist.values()) ** 2

    unnormalized_freq = np.array(list(freq_dist.values()))

    normalized_freq = softmax(unnormalized_freq)

    normalized_dist = {k: normalized_freq[i] for i, k in enumerate(freq_dist)}

    return normalized_dist


def main():
    src_file = "moby10b.txt"

    freq = get_frequency_distribution(src_file)


if __name__ == "__main__":
    main()
