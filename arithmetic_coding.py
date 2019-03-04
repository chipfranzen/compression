"""
The arithmetic coding compression algorithm.
"""
import time

import numpy as np

from binary_fractions import BinaryFraction
from language_models import add_eof_to_freq_dist, get_frequency_distribution


def freq_dist_to_interval_dict(freq_dist):
    keys = [k for k in freq_dist]
    vals = np.array([v for v in freq_dist.values()])
    ends = np.cumsum(vals)
    starts = ends - vals
    return {keys[i]: (starts[i], ends[i]) for i in range(len(vals))}


def entropy(p):
    return -np.sum(p * np.log2(p))


def chunk_string(s, n, fill=None):
    if fill is None:
        assert len(s) % n == 0, f"{s}, len {len(s)}, must break evenly into {n} chunks"
    else:
        n_fill_chars = (n - (len(s) % n)) % n
        s += fill * n_fill_chars
    return [s[i : i + n] for i in range(0, len(s), n)]


def encode(src, freq_dist):
    intervals = freq_dist_to_interval_dict(freq_dist)

    lower_bound = BinaryFraction(0.0)
    upper_bound = BinaryFraction(1.0)

    encoded_out_buffer = 0
    n_buffer = 0
    dest = src.split(".")[0] + ".acz"
    src_len = 0
    time_exp = 1
    t1 = time.time()

    with open(src) as infile:
        src_txt = infile.read()
        with open(dest, "wb+") as outfile:
            for char in src_txt:
                src_len += 1
                if src_len == 10 ** time_exp:
                    t2 = time.time()
                    print(f"Step {src_len}: {t2 - t1}s")
                    time_exp += 1

                lower_dec = lower_bound.decimal
                upper_dec = upper_bound.decimal
                current_range = upper_dec - lower_dec

                upper_dec = lower_dec + current_range * intervals[char][1]
                lower_dec = lower_dec + current_range * intervals[char][0]

                lower_bound = BinaryFraction(lower_dec)
                upper_bound = BinaryFraction(upper_dec)

                if lower_bound.msb_check(upper_bound):
                    encoded_out_buffer = encoded_out_buffer << 1
                    encoded_out_buffer += lower_bound.get_msb()
                    lower_bound.pop_msb(upper=False)
                    upper_bound.pop_msb(upper=True)
                    n_buffer += 1

                if n_buffer % 8 == 0:
                    outfile.write(bytes([encoded_out_buffer]))
                    encoded_out_buffer = 0

            encoded_tail_bin_string = BinaryFraction.shortest_bin_in_interval(
                lower_bound, upper_bound
            )

            for b in encoded_tail_bin_string[: 8 - n_buffer]:
                encoded_out_buffer = encoded_out_buffer << 1
                encoded_out_buffer += int(b)

            chunked_tail = chunk_string(encoded_tail_bin_string, 8, "0")
            out_bytes = bytes(
                [encoded_out_buffer] + [int(chunk, 2) for chunk in chunked_tail]
            )

            outfile.write(out_bytes)


def main():
    src_file = "xaa"

    freq = get_frequency_distribution(src_file)
    ent = entropy(np.array(list(freq.values())))
    print("entropy w no eof:", ent)
    freq = add_eof_to_freq_dist(freq)

    encode(src_file, freq)


if __name__ == "__main__":
    main()
