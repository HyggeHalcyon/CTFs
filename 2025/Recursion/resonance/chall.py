from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
from flag import FLAG

key = RSA.generate(1024)
n = key.n
e = key.e
d = key.d
p = key.p
q = key.q

dp = d % (p - 1)

m = bytes_to_long(FLAG)
c = pow(m, e, n)
ciphertext_hex = long_to_bytes(c).hex()

with open("output.txt", "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"e = {e}\n")
    f.write(f"dp = {dp}\n")
    f.write(f"ciphertext = {ciphertext_hex}\n")
