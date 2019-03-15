using Test

include("ArithmeticCoding.jl")

using Main.ArithmeticCoding: encode, BitVector

using Main.ArithmeticCoding.BinaryFractions: binaryfraction, tobitstring, nbits, tofloat, getbit, BinaryFractions, shortestbetween, bitvector

using Main.ArithmeticCoding.SymbolDistributions: SymbolDistribution, getp, getinterval

@testset "tobitstring" begin
    b = "1"
    expected = "10000000000000000000000000000000"
    actual = tobitstring(b)
    @test length(actual) == nbits
    @test expected == actual

    b = "010010"
    expected = "01001000000000000000000000000000"
    actual = tobitstring(b)
    @test length(actual) == nbits
    @test expected == actual
end

@testset "binaryfraction" begin
    d = .5
    expansion = "1"
    expected = tobitstring(expansion)
    actual = bitstring(binaryfraction(d))
    @test expected == actual

    d = 1/2 + 1/4
    expansion = "11"
    expected = tobitstring(expansion)
    actual = bitstring(binaryfraction(d))
    @test expected == actual

    d = 1/32 + 1/1024
    expansion = "0000100001"
    expected = tobitstring(expansion)
    actual = bitstring(binaryfraction(d))
    @test expected == actual

    d = 0.0
    expansion = "0"
    expected = tobitstring(expansion)
    actual = bitstring(binaryfraction(d))
    @test expected == actual

    d = 0
    expansion = "0"
    expected = tobitstring(expansion)
    actual = bitstring(binaryfraction(d))
    @test expected == actual

    d = 1
    expected = repeat("1", nbits)
    actual = bitstring(binaryfraction(d))
    @test expected == actual

    @test_throws ErrorException binaryfraction(-.1)
    @test_throws ErrorException binaryfraction(1.0)
    @test_throws ErrorException binaryfraction(-1)
    @test_throws ErrorException binaryfraction(2)
end

@testset "getbit" begin
    d = .5
    bf = binaryfraction(d)
    bit = 1
    expected = true
    actual = getbit(bf, bit)
    @test expected == actual

    bit = 2
    expected = false
    actual = getbit(bf, bit)
    @test expected == actual
end

@testset "tofloat" begin
    d = .5
    bf = binaryfraction(d)
    @test tofloat(bf) ≈ d

    d = 1
    bf = binaryfraction(d)
    @test tofloat(bf) ≈ d

    d = 0.0
    bf = binaryfraction(d)
    @test tofloat(bf) ≈ d

    d = 0.1
    bf = binaryfraction(d)
    @test tofloat(bf) ≈ d

    d = rand()
    bf = binaryfraction(d)
    @test tofloat(bf) ≈ d
end

@testset "bf_arithmetic" begin
    d1 = .1
    d2 = .2
    bf1 = binaryfraction(d1)
    bf2 = binaryfraction(d2)
    expected = d1 + d2
    actual = tofloat(bf1 + bf2)
    @test expected ≈ actual

    d1 = .1
    d2 = 1 - d1
    bf1 = binaryfraction(d1)
    bf2 = binaryfraction(d2)
    expected = d1 + d2
    actual = tofloat(bf1 + bf2)
    @test expected ≈ actual

    d1 = .1
    d2 = .2
    bf1 = binaryfraction(d1)
    bf2 = binaryfraction(d2)
    expected = d2 - d1
    actual = tofloat(bf2 - bf1)
    @test expected ≈ actual

    expected = d1 < d2
    actual = bf1 < bf2
    @test actual == expected
end

@testset "shortestbetween" begin
    x = UInt32(0b110)
    y = UInt32(0b010)
    z = UInt32(0b011)
    expected = bitvector(z)
    actual = shortestbetween(x, y)
    @test expected == actual

    x = UInt32(0b1100)
    y = UInt32(0b1010)
    z = UInt32(0b1011)
    expected = bitvector(z)
    actual = shortestbetween(x, y)
    @test expected == actual
end

@testset "SymbolDistribution" begin
    symbols = ['a', 'b', 'c']
    p = [.1, .2, .7]
    sd = SymbolDistribution(symbols, p)
    expected = [(0.0, .1), (.1, .3), (.3, 1.0)]
    actual = sd.intervals
    @test all([all(expected[i] .≈ actual[i]) for i=1:length(expected)])

    expected = .1
    actual = getp(sd, 'a')
    @test expected == actual

    expected = (0.1, 0.3)
    actual = getinterval(sd, 'b')
    @test all(expected .≈ actual)
end

@testset "encode" begin
    s = "ab"
    sd = SymbolDistribution(['a', 'b'], [.5, .5])
    expected = BitVector("011")
    actual = encode(s, sd)
    @test expected == actual
end
