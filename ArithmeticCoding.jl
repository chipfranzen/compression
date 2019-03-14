module BinaryFractions

BinaryFraction = UInt32
const nbits = 32
const one_bf = ~BinaryFraction(0)
const zero_bf = BinaryFraction(0)

function binaryfraction(d::Float64)
    1.0 > d >= 0.0 || error("d::Float64 must be in (1, 0].")
    res = BinaryFraction(0)
    for i in 1:nbits
        d *= 2.
        res += BinaryFraction(floor(d)) << (nbits - i)
        d %= 1
    end
    res
end

function binaryfraction(d::Int)
    d in [1, 0] || error("d::Int must be 1 or 0.")
    isone(d) ? one_bf : zero_bf
end

function tobitstring(x::String)
    x * repeat('0', nbits - length(x))
end

function getbit(bf::BinaryFraction, bit::Int)
    bf & (BinaryFraction(1) << (nbits - bit)) != 0
end

function tofloat(bf::BinaryFraction)
    decimal = 0.0
    for i in 1:nbits
        if getbit(bf, i)
            decimal += .5^i
        end
    end
    decimal
end

function bitvector(bf::BinaryFraction)
    BitVector([getbit(bf, i) for i = 1:nbits])
end

function getmsb(bf::BinaryFraction)
    getbit(bf, 1)
end

function msbcheck(bf1::BinaryFraction, bf2::BinaryFraction)
    getmsb(bf1) == getmsb(bf2)
end

function popmsb(bf::BinaryFraction, isupper::Bool=false)
    msb = getmsb(bf)
    bf = bf << 1
    if isupper
        bf += 1
    end
    msb, bf
end

function shortestbetween(bf1::BinaryFraction, bf2::BinaryFraction)
    if bf1 == bf2
        return bitvector(bf1)

    bv1 = bitvector(bf1)
    bv2 = bitvector(bf2)

    result = BitVector(zeros(Bool, nbits))

    i = 1

    while bv1[i] == bv2[i]
        result[i] = bv1[i]
        i += 1
    end

    result[i: i+1] = [0, 1]
    result
end

end

module FrequencyDistributions
using Distributions

StringOrChar = Union{String, Char}
CharMap = Dict{StringOrChar, Integer}
PVector = Vector{T} where T <: AbstractFloat
Interval = Tuple{T, T} where T <: AbstractFloat
IntervalVector = Vector{Interval}

struct SymbolDistribution
    symbols::CharMap
    p::PVector
    intervals::IntervalVector

    function SymbolDistribution(symbols, p, intervals)
        all(0 .>= p) || error("Elements of p must be positive.")
        0 <= sum(p) <= 1 || error("Sum of p must be in (0, 1).")
        new(vaues, p, intervals)
    end

    function SymbolDistribution(symbols, p)
        cumsums = cumsum(p)

        intervals = reduce(cumsums, init=[(0., 0.)]) do x, y
            lower = last(last(x))
            next_interval = (lower, y)
            append!(x, [next_interval])
        end

        intervals = intervals[2:] # remove init

        new(symbols, p, intervals)
    end

function symboldistribution(symbols::Vector{StringOrChar}, p::PVector)
    charmap = Dict(enumerate(symbols))
    SymbolDistribution(charmap, p)
end
