# Rotate left: 0b1001 --> 0b0011
rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
 
# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

# encrypt a function pointer
def encrypt(v, key):
    return rol(v ^ key, 0x11, 64)


print("KEY")
key = ror(0xf67f9d66436bb92a, 0x11, 64) ^ 0x7fdb5bba48f0
print(hex(key))

print("ENCRYPTED")
encrypted = encrypt(0x7fdb5bb98000 + 0x159f, key)
print(hex(encrypted))