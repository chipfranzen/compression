module BinaryFractions

export binaryfraction, tobitstring, nbits, tofloat, getbit, BinaryFraction

const nbits = 32
BinaryFraction = UInt32
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

function getmsb(bf::BinaryFraction)
    getbit(bf, 1)
end

end
