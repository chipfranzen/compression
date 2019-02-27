'''
Utils for working with binary fractions.
Binary fractions are represented as strings of the form "0b.000"
'''

import re

import numpy as np


def bin_to_dec(bin_string):
    pattern = r"0b.[01]*"
    assert re.fullmatch(pattern, bin_string), f"Binary string {bin_string} does not match {pattern}."

    bin_string = bin_string[3:]

    dec = 0.

    for i, e in enumerate(bin_string):
        dec += int(e) * 1 / 2 ** (i + 1)

    return dec


def dec_to_bin(dec):
    assert 0. < dec < 1.

    bin_string = "0b."

    i = 1
    while not (np.isclose(dec, 0.)):

        power = 1/2**i
        if dec >= power:
            next_char = '1'
            dec -= power

        else:
            next_char = '0'

        bin_string += next_char
        i += 1

    return bin_string


def main():
    bin_to_dec("0b.10")
    dec_to_bin(1/2 + 1/64 + 1/1024)

if __name__ == "__main__":
    main()
