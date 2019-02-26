'''
Utils for working with binary fractions

Binary fractions are represented as strings of the form "0b000.000"
'''

import re

def bin_to_dec(x):
    pattern = r"0b[01]*\.[01]*"
    assert(re.fullmatch(pattern, "0b010101.10101", f"Binary string `{x}` does not match `{pattern}`."))

