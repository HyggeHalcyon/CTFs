ciphertext = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"

ordinal = [ i for i in bytes.fromhex(ciphertext)]
print(ordinal)

for byte in range(0, 256):
    rev_xor = [ o ^ byte for o in ordinal ]
    plaintext = "".join(chr(p) for p in rev_xor)
    if "crypto" in plaintext:
        print(plaintext)

#Combined way of the previous one
for byte in range(0, 256):
    plaintext = "".join([ chr(o ^ byte) for o in ordinal])
    if "crypto" in plaintext:
        print(plaintext)