module ArithmeticCoding

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

function shortestbetween(lower::BinaryFraction, upper::BinaryFraction)
    if lower == upper
        return bitvector(lower)
    end

    lower_bv = bitvector(lower)
    upper_bv = bitvector(upper)

    result = BitVector(zeros(Bool, nbits))

    i = 1

    while lower_bv[i] == upper_bv[i]
        result[i] = lower_bv[i]
        i += 1
    end

    result[i] = 0
    i += 1

    while lower_bv[i] == 1
        result[i] = 1
        i += 1
    end
    result[i] = 1
    result
end

end

module SymbolDistributions

CharMap = Dict{Char, Integer}
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

        intervals = intervals[2:length(intervals)] # remove init

        new(symbols, p, intervals)
    end
end

function SymbolDistribution(symbols::Vector{Char}, p::PVector)
    nsymbols = length(symbols)
    charmap = Dict(zip(symbols, 1:nsymbols))
    SymbolDistribution(charmap, p)
end

function getp(sd::SymbolDistribution, k::Char)
    # Gets the probability of a character.
    ix = sd.symbols[k]
    sd.p[ix]
end

function getinterval(sd::SymbolDistribution, k::Char)
    # Gets the interval for a character.
    ix = sd.symbols[k]
    sd.intervals[ix]
end

end

using .BinaryFractions: tofloat, binaryfraction, shortestbetween, zero_bf, one_bf
using .SymbolDistributions: SymbolDistribution, getinterval

function BitVector(s::String)
    charmap = Dict([('0', false), ('1', true)])
    BitVector = [charmap[c] for c in s]
end

function encode(s::String, sd::SymbolDistribution)
    upper = one_bf
    lower = zero_bf
    i = 1

    for c in s
        println(i)
        interval = getinterval(sd, c)
        current_range = upper - lower

        upper_f = tofloat(upper)
        lower_f = tofloat(lower)
        current_range_f = tofloat(current_range)
        println(lower_f)
        println(upper_f)
        println(current_range_f)

        upper_f = lower_f + current_range_f * interval[2]
        lower_f = lower_f + current_range_f * interval[1]

        upper = binaryfraction(upper_f)
        lower = binaryfraction(lower_f)
        i += 1
    end

    println(tofloat(upper))
    println(tofloat(lower))

    shortestbetween(lower, upper)
end

end
