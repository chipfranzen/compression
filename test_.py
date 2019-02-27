from binary_fractions import bin_to_dec, dec_to_bin

def test_bin_to_dec():

    test_string = "0b.011"
    assert 1/4 + 1/8 == bin_to_dec(test_string)

def test_dec_to_bin():

    test_float = 1/2 + 1/64 + 1/1024
    assert '0b.1000010001' == dec_to_bin(test_float)

