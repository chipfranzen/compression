"""
Binary fractions are represented as tuples of integers. The first stores the binary fraction. The
second store the most significant bit. 
"""

import numpy as np


class BinaryFraction:
    def __init__(self, x: float = 0.):
        self.decimal = x

        assert 0.0 <= x <= 1.0, "Input must be in (0, 1)."

        if np.isclose(x, 0.0):
            self.i = 0
            self.msb = 0

        elif np.isclose(x, 1.0):
            self.i = 1
            self.msb = 0

        else:
            exp = 0
            self.i = 0
            while not (np.isclose(x, 0.0)):

                power = 1 / 2 ** exp
                self.i = self.i << 1

                if x >= power:
                    x -= power
                    self.i += 1

                exp += 1

            self.msb = exp - 1

    def __eq__(self, other):
        if type(other) == BinaryFraction:
            return (self.i == other.i) and (self.msb == other.msb)
        else:
            try:
                other = float(other)
                return np.isclose(self.to_float(), other)
            except ValueError:
                raise ValueError(f"Could not convert {type(other)} to float for comparison with BinaryFraction: {repr(other)}")

    def __repr__(self):
        return f"BinaryFraction({self.decimal})"

    def __str__(self):
        return f"""
        BinaryFraction
            base_10_int = {self.i}
            bin =         {bin(self.i)}
            msb =         {self.msb}
            bin_frac =    {self.get_bin_string()}
            decimal  =    {self.decimal}
            """
    def get_bin_string(self):
        return bin(self.i)[2:].rjust(self.msb + 1, "0")

    def get_msb(self):
        if np.isclose(self.decimal, 1.):
            return '1'
        if np.isclose(self.decimal, 0.):
            return '0'
        else:
            bin_string = self.get_bin_string()
            return bin_string[1]

    def msb_check(self, other):
        return self.get_msb() == other.get_msb()

    def pop_msb(self, upper):
        if np.isclose(self.decimal, 1.0):
            return '1'

        elif np.isclose(self.decimal, 0.0):
            return '0'

        else:
            popped_msb = self.get_msb()

            if popped_msb == "1":
                self.i -= 2 ** (self.msb - 1)

            self.i = self.i << 1

            if upper:
                self.i += 1

            self.decimal = self.to_float()

            return popped_msb, BinaryFraction(self.decimal)

    def to_float(self):
        assert self.i >= 0
        bin_string = bin(self.i)[2:].rjust(self.msb + 1, "0")

        dec = 0.0

        for i, e in enumerate(bin_string):
            dec += int(e) * 1 / 2 ** (i)

        return dec
