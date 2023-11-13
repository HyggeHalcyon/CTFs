from Crypto.Util.number import getPrime, bytes_to_long

p = getPrime(2048)
q = getPrime(2048)
n = p * q
e1 = 65537
e2 = 10 ** 9 + 7


m = bytes_to_long(open('flag.txt', 'rb').read())

c1 = pow(m, e1, n)
c2 = pow(m, e2, n)

with open('pesan.txt', 'w') as f:
    f.write('e:%d\nn:%d\nc:%d\n\n' % (e1, n, c1))
    f.write('e:%d\nn:%d\nc:%d\n' % (e2, n, c2))
