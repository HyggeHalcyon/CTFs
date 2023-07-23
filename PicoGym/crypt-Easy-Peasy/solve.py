from Crypto.Util.number import *
from pwn import *

KEY_LEN = 50000

context.log_level = "info"
host, port = "mercury.picoctf.net", 41934
io = remote(host, port)

info('---------------RECEIVING AND FORMATTING FLAG---------------')
io.recvlines(2)
ct1 = io.recvline()[:-1].decode()
ct1 = [i for i in bytes.fromhex(ct1)]
info('ct1 length: %d', len(ct1))

info('-----------------------OVERRIDING KEY----------------------')
remaining_key = KEY_LEN - len(ct1)
while remaining_key >= 10000:  
    io.sendlineafter(b'encrypt?', b'a'*10000)
    remaining_key -= 10000
    info('current key index: %d', remaining_key)

io.sendlineafter(b'encrypt?', b'a'*remaining_key)
info('current key index: %d', 0)

info('----------------------DECRYPTING FLAG----------------------')
m2 = [ord(i) for i in 'a'*32]
info('m2 length: %d', len(m2))
io.sendlineafter(b'encrypt?', b'a'*len(ct1))

io.recvline()
ct2 = io.recvline()[:-1].decode()
ct2 = [i for i in bytes.fromhex(ct2)]
info('ct2 length: %d', len(ct2))

m1_xored_m2 = list(map(lambda x,y: x ^ y, ct1, ct2))
m1 = list(map(lambda x,y: chr(x ^ y), m1_xored_m2, m2))

info('flag = picoCTF{%s}', ''.join(m1))
io.close()

# explanations: https://ctf.zeyu2001.com/2021/picoctf/easy-peasy-40
# picoCTF{abf2f7d5edf082028076bfd7a4cfe9a9}