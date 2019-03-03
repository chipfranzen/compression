"""
The arithmetic coding compression algorithm.
"""
import numpy as np

from binary_fractions import BinaryFraction
from language_models import add_eof_to_freq_dist, get_frequency_distribution


def freq_dist_to_interval_dict(freq_dist):
    keys = [k for k in freq_dist]
    vals = np.array([v for v in freq_dist.values()])
    ends = np.cumsum(vals)
    starts = ends - vals
    return {keys[i]: (starts[i], ends[i]) for i in range(len(vals))}


def entropy(freq_dist):
    p = np.array(list(freq_dist.values()))
    return -np.sum(p * np.log2(p))


def main():
    src_file = "sample.txt"

    freq = get_frequency_distribution(src_file)
    ent = entropy(freq)
    print("entropy w no eof:", entropy(freq))
    freq = add_eof_to_freq_dist(freq)
    intervals = freq_dist_to_interval_dict(freq)

    lower_bound = BinaryFraction(0.0)
    upper_bound = BinaryFraction(1.0)

    encoded = ""
    len_src = 0

    with open(src_file) as f:
        while True:
            char = f.read(1)
            if char == "\n":
                continue
            len_src += 1
            lower_dec = lower_bound.decimal
            upper_dec = upper_bound.decimal
            current_range = upper_dec - lower_dec

            upper_dec = lower_dec + current_range * intervals[char][1]
            lower_dec = lower_dec + current_range * intervals[char][0]

            lower_bound = BinaryFraction(lower_dec)
            upper_bound = BinaryFraction(upper_dec)

            if lower_bound.msb_check(upper_bound):
                encoded += lower_bound.get_msb()
                lower_bound.pop_msb(upper=False)
                upper_bound.pop_msb(upper=True)

            if char == "":
                break

        encoded += BinaryFraction.shortest_bin_in_interval(lower_bound, upper_bound)
        print(encoded)

        print("entropy:", entropy(freq))
        print(freq)
        print("encoded length:", len(encoded))
        print("src length:", len_src)
        print("src length in bits:", len_src * 8)
        print("expected length:", ent * len_src)

        print(len(encoded) / len_src)


if __name__ == "__main__":
    main()
