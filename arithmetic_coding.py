"""
The arithmetic coding compression algorithm.
"""
import numpy as np

from binary_fractions import BinaryFraction, bin_frac_to_dec, dec_to_bin_frac
from language_models import get_frequency_distribution
from scipy.special import softmax


def add_eof_to_freq_dist(freq_dist):
    freq_dist[""] = min(freq_dist.values()) ** 2

    unnormalized_freq = np.array(list(freq_dist.values()))

    normalized_freq = softmax(unnormalized_freq)

    normalized_dist = {k: normalized_freq[i] for i, k in enumerate(freq_dist)}

    return normalized_dist


def freq_dist_to_interval_dict(freq_dist):
    keys = [k for k in freq_dist]
    vals = np.array([v for v in freq_dist.values()])
    ends = np.cumsum(vals)
    starts = ends - vals
    return {keys[i]: (starts[i], ends[i]) for i in range(len(vals))}


def main():
    src_file = "sample.txt"

    freq = get_frequency_distribution(src_file)
    freq = add_eof_to_freq_dist(freq)
    intervals = freq_dist_to_interval_dict(freq)

    lower_bound = BinaryFraction()
    upper_bound = BinaryFraction(1)

    encoded = ""

    with open(src_file) as f:
        while True:
            char = f.read(1)
            lower_dec = bin_frac_to_dec(lower_bound)
            upper_dec = bin_frac_to_dec(upper_bound)
            current_range = upper_dec - lower_dec

            upper_dec = lower_dec + current_range * intervals[char][1]
            lower_dec = lower_dec + current_range * intervals[char][0]

            lower_bound = dec_to_bin_frac(lower_dec)
            upper_bound = dec_to_bin_frac(upper_dec)

            print(upper_dec, lower_dec)
            print(dec_to_bin_frac(lower_dec))
            print(dec_to_bin_frac(upper_dec))
            print(encoded)

            if lower_bound.msb_check(upper_bound):
                encoded += lower_bound.get_msb()
                lower_bound.pop_msb(upper=False)
                upper_bound.pop_msb(upper=True)

            if char == "":
                break

        print(upper_dec, lower_dec)
        print(dec_to_bin_frac(lower_dec))
        print(dec_to_bin_frac(upper_dec))


if __name__ == "__main__":
    main()
