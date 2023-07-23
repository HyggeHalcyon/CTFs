p = 65537

# >>> pow(3, 17, 17)
# 3                     |
# >>> pow(5, 17, 17)    |--> any number with the same power
# 5                     |    and modulus equals to its number
# >>> pow(7, 16, 17)
# 1                     | --> fermat's little theorem
#                             a ^ (p-1) ≡ 1 (mod p)
#                               p need to be prime

print(f'Flag: {pow(273246787654, 65536, 65537)}')