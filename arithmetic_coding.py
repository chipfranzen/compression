"""
The arithmetic coding compression algorithm.
"""
import numpy as np

from language_models import get_frequency_distribution


def add_eof_to_freq_dist(freq_dist):
    freq_dist[""] = min(freq_dist.values()) ** 0.5
    unnormalized_freq = np.array(dist.values)
    normalized_freq = softmax(unnormalized_freq)
    return freq_dist


def softmax(v):
    z = np.sum(np.exp(v))
    return np.exp(v) / z


def main():
    src_file = "moby10b.txt"

    freq = get_frequency_distribution(src_file)


if __name__ == "__main__":
    main()
