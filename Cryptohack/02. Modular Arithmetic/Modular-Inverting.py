# Fp is defined as Fields : {0, 1, .... , p - 1}
# for all g in Fp
# exist d such g * d ≡ 1 (mod p)
# this is said the multiplicative inverse of g
# Example: 7 * 8 = 56 ≡ 1 mod 11

def modular_inverting(g, p):
    for d in range(100):
        if ( g * d % p == 1):
            return d

print(modular_inverting(3, 13))