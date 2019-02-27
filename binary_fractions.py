"""
Utils for working with binary fractions.
Binary fractions are represented as tuples of integers. The first stores the binary fraction. The
second store the most significant bit. 
"""

import re

import numpy as np


class BinaryFraction:
    def __init__(self, i=0, msb=0):
        self.i = i
        self.msb = msb

    def __eq__(self, other):
        return (
            (type(self) == type(other))
            and (self.i == other.i)
            and (self.msb == other.msb)
        )

    def __repr__(self):
        return f"BinaryFraction({self.i}, {self.msb})"

    def __str__(self):
        print_str = f"""
        BinaryFraction
            base_10_int = {self.i}
            bin =         {bin(self.i)}
            msb =         {self.msb}
            bin_frac =    {'.' + bin(self.i)[2:].rjust(self.msb, '0')}
            """

        print(print_str)


def bin_frac_to_dec(bin_frac):
    bin_string = bin(bin_frac.i)[2:].rjust(bin_frac.msb + 1, "0")

    dec = 0.0

    for i, e in enumerate(bin_string):
        dec += int(e) * 1 / 2 ** (i + 1)

    return dec


def dec_to_bin_frac(dec):
    assert 0.0 < dec < 1.0

    bin_frac = BinaryFraction()

    i = 0
    while not (np.isclose(dec, 0.0)):
        i += 1

        power = 1 / 2 ** i
        bin_frac.i = bin_frac.i << 1

        if dec >= power:
            dec -= power
            bin_frac.i += 1

    bin_frac.msb = i - 1

    return bin_frac
